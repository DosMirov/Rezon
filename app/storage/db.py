"""
app/storage/db.py
-----------------
Schema initialization for SQLite.
Defines `session` and `voice_log` tables with proper constraints, now including text support.

Usage:
    from app.storage.db import init_db
    await init_db(settings.DATABASE_PATH)
"""

import aiosqlite
from app.config import settings

# Schema DDLs
CREATE_SESSION_TABLE = """
CREATE TABLE IF NOT EXISTS session (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    brief_id TEXT NOT NULL,
    last_fragment_index INTEGER NOT NULL DEFAULT 0,
    started_at TEXT NOT NULL,
    status TEXT NOT NULL,
    UNIQUE(user_id, status)
);
"""

CREATE_VOICE_LOG_TABLE = """
CREATE TABLE IF NOT EXISTS voice_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    username TEXT,
    first_name TEXT,
    brief_id TEXT NOT NULL,
    fragment_index INTEGER NOT NULL,
    content_type TEXT NOT NULL,          -- 'voice', 'text', 'photo', 'video', etc.
    file_id TEXT,
    text TEXT,
    thumb_file_id TEXT,
    mime_type TEXT,
    file_name TEXT,
    duration INTEGER,
    width INTEGER,
    height INTEGER,
    timestamp TEXT NOT NULL
);
"""

async def init_db(db_path: str) -> None:
    """
    Create missing tables in the SQLite database.
    """
    async with aiosqlite.connect(db_path) as db:
        await db.execute(CREATE_SESSION_TABLE)
        await db.execute(CREATE_VOICE_LOG_TABLE)
        await db.commit()
