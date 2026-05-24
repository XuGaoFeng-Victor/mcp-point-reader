"""MCP plugin TTS - 独立于点读助手的文字朗读功能。"""

import os
import tempfile
from .config import get


def speak_offline(text: str, voice_id: str = "", speed: float = 1.0) -> str:
    """使用系统离线 TTS（pyttsx3）朗读文本。返回朗读结果摘要。"""
    try:
        import pyttsx3
        engine = pyttsx3.init()
        if voice_id:
            engine.setProperty("voice", voice_id)
        engine.setProperty("rate", int(speed * 200))
        engine.say(text)
        engine.runAndWait()
        engine.stop()
        return f"已朗读 ({len(text)} 字符)"
    except Exception as e:
        return f"离线朗读失败: {e}"


def speak_online(text: str, voice_id: str = "", speed: float = 1.0) -> str:
    """使用在线 TTS（edge-tts）朗读文本，返回音频文件路径。"""
    try:
        import asyncio
        import edge_tts

        voice = voice_id or get("voice_en", "en-US-AriaNeural")
        rate_pct = int((speed - 1.0) * 100)
        rate_str = f"{rate_pct:+d}%"

        tmp = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
        tmp.close()

        async def _run():
            communicate = edge_tts.Communicate(text, voice, rate=rate_str)
            await communicate.save(tmp.name)

        asyncio.run(_run())
        return f"音频已保存: {tmp.name}"
    except Exception as e:
        return f"在线朗读失败: {e}"


def speak(text: str) -> str:
    """根据配置自动选择引擎朗读。"""
    engine = get("tts_engine", "offline")
    speed = get("speed", 1.0)

    has_chinese = any("一" <= c <= "鿿" for c in text)
    has_english = any(c.isalpha() and ord(c) < 128 for c in text)

    if engine == "offline":
        voice_zh = get("voice_zh", "")
        voice_en = get("voice_en", "")
        if has_chinese and voice_zh:
            return speak_offline(text, voice_zh, speed)
        elif has_english and voice_en:
            return speak_offline(text, voice_en, speed)
        return speak_offline(text, speed=speed)
    else:
        return speak_online(text, speed=speed)
