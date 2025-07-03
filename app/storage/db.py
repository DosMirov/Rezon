import aiosqlite
from app.config import settings

CREATE_SESSION_TABLE = """
CREATE TABLE IF NOT EXISTS session (
    user_id INTEGER PRIMARY KEY,
    brief_id TEXT,
    last_fragment_index INTEGER,
    started_at TEXT,
    status TEXT
);
"""

CREATE_VOICE_LOG_TABLE = """
CREATE TABLE IF NOT EXISTS voice_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    username TEXT,
    first_name TEXT,
    brief_id TEXT,
    fragment_index INTEGER,
    file_id TEXT,
    timestamp TEXT
);
"""

async def init_db(path: str):
    async with aiosqlite.connect(path) as db:
        await db.execute(CREATE_SESSION_TABLE)
        await db.execute(CREATE_VOICE_LOG_TABLE)
        await db.commit()