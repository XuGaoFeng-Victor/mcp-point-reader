"""读取点读助手的配置文件。"""

import json
import os
from pathlib import Path

# 点读助手项目路径
READER_DIR = Path(os.getenv("POINT_READER_DIR", r"D:\English"))
CONFIG_PATH = READER_DIR / "config.json"

DEFAULT_CONFIG = {
    "hotkey": "ctrl+alt+x",
    "screenshot_hotkey": "ctrl+alt+z",
    "tts_engine": "offline",
    "voice_zh": "zh-CN-XiaoxiaoNeural",
    "voice_en": "en-US-AriaNeural",
    "speed": 1.0,
    "ai_provider": "qwen",
    "ai_model": "qwen-turbo",
    "ai_api_key": "",
}


def load_config() -> dict:
    """读取点读助手的配置，缺失字段用默认值补全。"""
    cfg = dict(DEFAULT_CONFIG)
    try:
        if CONFIG_PATH.exists():
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                stored = json.load(f)
                cfg.update(stored)
    except (json.JSONDecodeError, IOError):
        pass
    return cfg


def get(key: str, default=None):
    return load_config().get(key, default)


def get_db_path() -> Path:
    return READER_DIR / "data.db"
