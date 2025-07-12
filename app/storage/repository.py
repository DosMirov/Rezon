"""
app/storage/repository.py
-------------------------
Atomic data operations for session lifecycle and voice fragment logging.
All writes related to a single fragment happen in one transaction to guarantee
correct sequencing between voice_log and session.last_fragment_index.
"""

import aiosqlite
from typing import Optional, Dict

from app.config import settings
from app.utils.time import get_timestamp

DB_PATH = settings.DATABASE_PATH


async def create_session(user_id: int, brief_id: str) -> None:
    """
    Start or reset a session for the given user.
    """
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT OR REPLACE INTO session (user_id, brief_id, last_fragment_index, started_at, status)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, brief_id, 0, get_timestamp(), 'active'))
        await db.commit()


async def get_active_session(user_id: int) -> Optional[Dict[str, int]]:
    """
    Return the active session for a user, or None if not exists.
    """
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("""
            SELECT brief_id, last_fragment_index 
              FROM session
             WHERE user_id = ? AND status = 'active'
        """, (user_id,))
        row = await cursor.fetchone()
    if row:
        return {"brief_id": row[0], "last_fragment_index": row[1]}
    return None


async def complete_session(user_id: int) -> None:
    """
    Mark the user's session as done.
    """
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            UPDATE session
               SET status = 'done'
             WHERE user_id = ? AND status = 'active'
        """, (user_id,))
        await db.commit()


async def log_voice_fragment(
    user_id: int,
    username: str,
    first_name: str,
    brief_id: str,
    file_id: str
) -> int:
    """
    Atomically insert a voice_log row and increment the session's fragment index.
    Returns the new fragment_index.
    """
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("BEGIN")
        # increment index first to derive next fragment number
        await db.execute("""
            UPDATE session
               SET last_fragment_index = last_fragment_index + 1
             WHERE user_id = ? AND status = 'active'
        """, (user_id,))
        # fetch the updated index
        cursor = await db.execute("""
            SELECT last_fragment_index 
              FROM session
             WHERE user_id = ? AND status = 'active'
        """, (user_id,))
        row = await cursor.fetchone()
        fragment_index = row[0] if row else 1

        # insert voice log
        await db.execute("""
            INSERT INTO voice_log (
                user_id, username, first_name, brief_id, fragment_index, file_id, timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id, username, first_name, brief_id,
            fragment_index, file_id, get_timestamp()
        ))
        await db.commit()

    return fragment_index
