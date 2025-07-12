import logging
from aiogram.exceptions import TelegramBadRequest

from app.bot import bot
from app.config import settings

logger = logging.getLogger(__name__)

async def send_media_to_channel(
    user_id: int,
    username: str,
    brief_id: str,
    fragment_index: int,
    content_type: str,
    file_id: str = None,
    text: str = None,
    timestamp: str = None
) -> None:
    mention = f"@{username}" if username and username != "-" else f"ID:{user_id}"
    tags = f"#brief_{brief_id} #user_{user_id} #v{fragment_index}"

    meta_text = (
        f"🧷 Новый фрагмент (<b>{content_type}</b>):\n"
        f"────────────\n"
        f"👤 {mention}\n"
        f"🗓 {timestamp}\n"
        f"📁 Brief-ID: <code>{brief_id}</code>\n"
        f"🔢 №{fragment_index}\n"
        f"{tags}\n"
    )

    try:
        if content_type == "text":
            await bot.send_message(settings.CHANNEL_ID, meta_text + (text or ""), parse_mode="HTML")
        elif content_type == "voice":
            await bot.send_message(settings.CHANNEL_ID, meta_text, parse_mode="HTML")
            await bot.send_voice(settings.CHANNEL_ID, file_id)
        elif content_type == "photo":
            await bot.send_message(settings.CHANNEL_ID, meta_text, parse_mode="HTML")
            await bot.send_photo(settings.CHANNEL_ID, file_id, caption=text or None)
        elif content_type == "video":
            await bot.send_message(settings.CHANNEL_ID, meta_text, parse_mode="HTML")
            await bot.send_video(settings.CHANNEL_ID, file_id, caption=text or None)
        elif content_type == "audio":
            await bot.send_message(settings.CHANNEL_ID, meta_text, parse_mode="HTML")
            await bot.send_audio(settings.CHANNEL_ID, file_id, caption=text or None)
        elif content_type == "document":
            await bot.send_message(settings.CHANNEL_ID, meta_text, parse_mode="HTML")
            await bot.send_document(settings.CHANNEL_ID, file_id, caption=text or None)
        elif content_type == "video_note":
            await bot.send_message(settings.CHANNEL_ID, meta_text, parse_mode="HTML")
            await bot.send_video_note(settings.CHANNEL_ID, file_id)
        else:
            await bot.send_message(settings.CHANNEL_ID, meta_text + "\n❔ Неизвестный тип.", parse_mode="HTML")
    except TelegramBadRequest as e:
        logger.error("Failed to send fragment %s for brief %s: %s", fragment_index, brief_id, e)
    except Exception:
        logger.exception("Unexpected error while sending fragment %s for brief %s", fragment_index, brief_id)
