# app/handlers/universal.py

from aiogram import Router
from aiogram.types import Message

from app.storage.repository import get_active_session, log_fragment
from app.services.send_to_channel import send_media_to_channel
from app.utils.time import format_human_time

router = Router()

@router.message()
async def handle_any_content(message: Message):
    user = message.from_user
    user_id = user.id
    username = user.username or "-"
    first_name = user.first_name or "-"
    session = await get_active_session(user_id)
    if not session:
        await message.answer("⚠️ У тебя ещё нет активной сессии. Напиши /start.")
        return
    brief_id = session["brief_id"]
    timestamp = format_human_time()

    # Универсальный парсер Telegram ContentType
    ct, file_id, text, thumb_file_id, mime_type, file_name, duration, width, height = None, None, None, None, None, None, None, None, None

    if message.voice:
        ct = "voice"
        file_id = message.voice.file_id
        duration = message.voice.duration
    elif message.audio:
        ct = "audio"
        file_id = message.audio.file_id
        duration = message.audio.duration
        mime_type = message.audio.mime_type
        file_name = message.audio.file_name
    elif message.document:
        ct = "document"
        file_id = message.document.file_id
        mime_type = message.document.mime_type
        file_name = message.document.file_name
        thumb = getattr(message.document, 'thumbnail', None) or getattr(message.document, 'thumb', None)
        if thumb:
            thumb_file_id = thumb.file_id
        text = message.caption
    elif message.photo:
        ct = "photo"
        photo_obj = message.photo[-1]  # Самое большое
        file_id = photo_obj.file_id
        width = photo_obj.width
        height = photo_obj.height
        text = message.caption
    elif message.video:
        ct = "video"
        file_id = message.video.file_id
        duration = message.video.duration
        width = message.video.width
        height = message.video.height
        thumb = getattr(message.video, 'thumbnail', None) or getattr(message.video, 'thumb', None)
        if thumb:
            thumb_file_id = thumb.file_id
        mime_type = message.video.mime_type
        text = message.caption
    elif message.video_note:
        ct = "video_note"
        file_id = message.video_note.file_id
        duration = message.video_note.duration
        width = message.video_note.length
        height = message.video_note.length
    elif message.text:
        ct = "text"
        text = message.text

    if not ct:
        await message.answer("❔ Не могу обработать этот тип файла.")
        return

    fragment_index = await log_fragment(
        user_id=user_id,
        username=username,
        first_name=first_name,
        brief_id=brief_id,
        content_type=ct,
        file_id=file_id,
        text=text,
        thumb_file_id=thumb_file_id,
        mime_type=mime_type,
        file_name=file_name,
        duration=duration,
        width=width,
        height=height
    )

    await send_media_to_channel(
        user_id=user_id,
        username=username,
        brief_id=brief_id,
        fragment_index=fragment_index,
        content_type=ct,
        file_id=file_id,
        text=text,
        timestamp=timestamp
    )

    await message.answer(f"✅ {ct.capitalize()} №{fragment_index} принят. Добавишь ещё?")
