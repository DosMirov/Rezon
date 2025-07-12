from aiogram import Router
from aiogram.types import Message
from app.services.send_to_channel import send_media_to_channel
from app.utils.time import get_daystamp, format_human_time

router = Router()

def make_brief_id(user_id: int, daystamp: str) -> str:
    return f"BRF-{user_id}_{daystamp}"

@router.message()
async def handle_any_content(message: Message):
    user = message.from_user
    user_id = user.id
    username = user.username or "-"
    daystamp = get_daystamp()
    brief_id = make_brief_id(user_id, daystamp)
    timestamp = format_human_time()

    # Универсальный парсер
    ct, file_id, text = None, None, None
    if message.voice:
        ct, file_id = "voice", message.voice.file_id
    elif message.audio:
        ct, file_id = "audio", message.audio.file_id
    elif message.document:
        ct, file_id, text = "document", message.document.file_id, message.caption
    elif message.photo:
        ct, file_id, text = "photo", message.photo[-1].file_id, message.caption
    elif message.video:
        ct, file_id, text = "video", message.video.file_id, message.caption
    elif message.video_note:
        ct, file_id = "video_note", message.video_note.file_id
    elif message.text:
        ct, text = "text", message.text

    if not ct:
        await message.answer("❔ Не могу обработать этот тип файла.")
        return

    await send_media_to_channel(
        user_id=user_id,
        username=username,
        brief_id=brief_id,
        content_type=ct,
        file_id=file_id,
        text=text,
        timestamp=timestamp
    )

    await message.answer(f"✅ {ct.capitalize()} зафиксирован. Добавишь ещё?")
