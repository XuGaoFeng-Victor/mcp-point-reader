"""截图 OCR 和剪贴板取词。"""

import os
from .config import get


def capture_clipboard() -> str | None:
    """读取当前剪贴板文本。"""
    try:
        import pyperclip
        text = pyperclip.paste()
        if text and text.strip():
            return text.strip()
        return None
    except Exception:
        return None


def screenshot_ocr() -> str | None:
    """全屏截图 + OCR 识别。"""
    try:
        import pytesseract
        from PIL import Image
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtCore import QBuffer, QIODevice
        import io

        # Configure tesseract path
        bundled = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "resources", "tesseract", "tesseract.exe"
        )
        if os.path.exists(bundled):
            pytesseract.pytesseract.tesseract_cmd = bundled
        else:
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

        # Need a QApplication instance
        app = QApplication.instance()
        if app is None:
            app = QApplication([])

        screen = QApplication.primaryScreen()
        pixmap = screen.grabWindow(0)

        buf = QBuffer()
        buf.open(QIODevice.ReadWrite)
        pixmap.save(buf, 'PNG')
        buf.seek(0)
        pil_img = Image.open(io.BytesIO(buf.data()))
        buf.close()

        text = pytesseract.image_to_string(pil_img, lang='chi_sim+eng')
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        return ' '.join(lines) if lines else None

    except ImportError as e:
        return f"[需要安装依赖: {e}]"
    except Exception as e:
        return f"[截图识别失败: {e}]"
