"""
app/storage/repository.py
-------------------------
Atomic data operations for session lifecycle and fragment logging (voice/text/media).
All writes related to a single fragment happen in one transaction to guarantee
correct sequencing between voice_log and session.last_fragment_index.
"""

import aiosqlite
from typing import Optional, Dict

from app.config import settings
from app.utils.time import get_timestamp

DB_PATH = settings.DATABASE_PATH


async def create_session(user_id: int, brief_id: str) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT OR REPLACE INTO session (user_id, brief_id, last_fragment_index, started_at, status)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, brief_id, 0, get_timestamp(), 'active'))
        await db.commit()


async def get_active_session(user_id: int) -> Optional[Dict[str, int]]:
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
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            UPDATE session
               SET status = 'done'
             WHERE user_id = ? AND status = 'active'
        """, (user_id,))
        await db.commit()


# --- Legacy: Voice fragment logging (можно оставить для старого flow) ---
async def log_voice_fragment(
    user_id: int,
    username: str,
    first_name: str,
    brief_id: str,
    file_id: str
) -> int:
    """
    Atomically insert a voice_log row (voice) and increment the session's fragment index.
    Returns the new fragment_index.
    """
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("BEGIN")
        await db.execute("""
            UPDATE session
               SET last_fragment_index = last_fragment_index + 1
             WHERE user_id = ? AND status = 'active'
        """, (user_id,))
        cursor = await db.execute("""
            SELECT last_fragment_index 
              FROM session
             WHERE user_id = ? AND status = 'active'
        """, (user_id,))
        row = await cursor.fetchone()
        fragment_index = row[0] if row else 1

        await db.execute("""
            INSERT INTO voice_log (
                user_id, username, first_name, brief_id, fragment_index, 
                content_type, file_id, text, thumb_file_id, mime_type, 
                file_name, duration, width, height, timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id, username, first_name, brief_id,
            fragment_index, "voice", file_id, None, None, None, None, None, None, None, get_timestamp()
        ))
        await db.commit()

    return fragment_index


# --- Legacy: Text fragment logging (можно оставить для старого flow) ---
async def log_text_fragment(
    user_id: int,
    username: str,
    first_name: str,
    brief_id: str,
    text: str
) -> int:
    """
    Atomically insert a text fragment and increment the session's fragment index.
    Returns the new fragment_index.
    """
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("BEGIN")
        await db.execute("""
            UPDATE session
               SET last_fragment_index = last_fragment_index + 1
             WHERE user_id = ? AND status = 'active'
        """, (user_id,))
        cursor = await db.execute("""
            SELECT last_fragment_index FROM session
             WHERE user_id = ? AND status = 'active'
        """, (user_id,))
        row = await cursor.fetchone()
        fragment_index = row[0] if row else 1

        await db.execute("""
            INSERT INTO voice_log (
                user_id, username, first_name, brief_id, fragment_index, 
                content_type, file_id, text, thumb_file_id, mime_type, 
                file_name, duration, width, height, timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id, username, first_name, brief_id,
            fragment_index, "text", None, text, None, None, None, None, None, None, get_timestamp()
        ))
        await db.commit()
    return fragment_index


# --- UNIVERSAL fragment logging ---
async def log_fragment(
    user_id: int,
    username: str,
    first_name: str,
    brief_id: str,
    content_type: str,
    file_id: str = None,
    text: str = None,
    thumb_file_id: str = None,
    mime_type: str = None,
    file_name: str = None,
    duration: int = None,
    width: int = None,
    height: int = None
) -> int:
    """
    Atomically log any message/media type and increment fragment_index.
    Returns new fragment_index.
    """
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("BEGIN")
        await db.execute("""
            UPDATE session
               SET last_fragment_index = last_fragment_index + 1
             WHERE user_id = ? AND status = 'active'
        """, (user_id,))
        cursor = await db.execute("""
            SELECT last_fragment_index FROM session
             WHERE user_id = ? AND status = 'active'
        """, (user_id,))
        row = await cursor.fetchone()
        fragment_index = row[0] if row else 1

        await db.execute("""
            INSERT INTO voice_log (
                user_id, username, first_name, brief_id, fragment_index,
                content_type, file_id, text, thumb_file_id,
                mime_type, file_name, duration, width, height, timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id, username, first_name, brief_id, fragment_index,
            content_type, file_id, text, thumb_file_id,
            mime_type, file_name, duration, width, height, get_timestamp()
        ))
        await db.commit()
    return fragment_index
