"""与点读助手共享 data.db 的数据库操作。"""

import sqlite3
from typing import Optional
from .config import get_db_path


def connect():
    path = str(get_db_path())
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def add_vocab(word: str, source_sentence: str = "", notes: str = "") -> bool:
    try:
        conn = connect()
        conn.execute(
            "INSERT OR IGNORE INTO vocabulary (word, source_sentence, notes) VALUES (?, ?, ?)",
            (word.strip().lower(), source_sentence, notes),
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error:
        return False


def list_vocab(learned: Optional[bool] = None, keyword: str = "", limit: int = 50) -> list[dict]:
    conn = connect()
    if keyword:
        rows = conn.execute(
            "SELECT * FROM vocabulary WHERE word LIKE ? ORDER BY added_at DESC LIMIT ?",
            (f"%{keyword}%", limit),
        ).fetchall()
    elif learned is not None:
        rows = conn.execute(
            "SELECT * FROM vocabulary WHERE learned = ? ORDER BY added_at DESC LIMIT ?",
            (1 if learned else 0, limit),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM vocabulary ORDER BY added_at DESC LIMIT ?", (limit,)
        ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def mark_learned(word_id: int, learned: bool = True) -> bool:
    try:
        conn = connect()
        conn.execute("UPDATE vocabulary SET learned = ? WHERE id = ?", (1 if learned else 0, word_id))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error:
        return False


def delete_vocab(word_id: int) -> bool:
    try:
        conn = connect()
        conn.execute("DELETE FROM vocabulary WHERE id = ?", (word_id,))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error:
        return False


def add_history(text: str, source_app: str = "", engine_used: str = "") -> bool:
    try:
        conn = connect()
        conn.execute(
            "INSERT INTO history (text, source_app, engine_used) VALUES (?, ?, ?)",
            (text[:500], source_app, engine_used),
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error:
        return False


def list_history(limit: int = 50, keyword: str = "") -> list[dict]:
    conn = connect()
    if keyword:
        rows = conn.execute(
            "SELECT * FROM history WHERE text LIKE ? ORDER BY read_at DESC LIMIT ?",
            (f"%{keyword}%", limit),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM history ORDER BY read_at DESC LIMIT ?", (limit,)
        ).fetchall()
    conn.close()
    return [dict(r) for r in rows]
