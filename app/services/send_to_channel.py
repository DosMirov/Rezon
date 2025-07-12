"""
app/services/send_to_channel.py
-------------------------------
Send voice fragments along with metadata to the configured channel.
Reuses the singleton `bot` instance to avoid extra connections and rate-limit issues.
"""

import logging
from aiogram import TelegramBadRequest

from app.bot import bot
from app.config import settings

logger = logging.getLogger(__name__)


async def send_voice_to_channel(
    user_id: int,
    username: str,
    brief_id: str,
    fragment_index: int,
    file_id: str,
    timestamp: str
) -> None:
    """
    Dispatch a text summary and the voice fragment to the ADMIN channel.
    """
    mention = f"@{username}" if username and username != "-" else f"ID:{user_id}"
    brief_tag = f"#brief_{brief_id}"
    user_tag = f"#user_{user_id}"
    version_tag = f"#v{fragment_index}"

    message_text = (
        f"🧷 Новый фрагмент:\n"
        f"────────────\n"
        f"👤 {mention}\n"
        f"🗓 {timestamp}\n"
        f"📁 Brief-ID: <code>{brief_id}</code>\n"
        f"🎤 Сообщение №{fragment_index}\n\n"
        f"{brief_tag} {user_tag} {version_tag}"
    )

    try:
        # Send metadata message
        await bot.send_message(
            chat_id=settings.CHANNEL_ID,
            text=message_text,
            parse_mode="HTML",
        )
        # Send the actual voice fragment
        await bot.send_voice(
            chat_id=settings.CHANNEL_ID,
            voice=file_id,
        )
    except TelegramBadRequest as e:
        logger.error(
            "Failed to send fragment %s for brief %s: %s",
            fragment_index, brief_id, e
        )
    except Exception as e:
        logger.exception(
            "Unexpected error sending fragment %s for brief %s",
            fragment_index, brief_id
        )
