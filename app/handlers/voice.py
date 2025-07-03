from aiogram import Router, F
from aiogram.types import Message
from app.storage.repository import (
    get_active_session,
    increment_fragment_index,
    log_voice_fragment,
)
from app.services.send_to_channel import send_voice_to_channel
from app.utils.time import format_human_time

router = Router()

@router.message(F.voice)
async def handle_voice(message: Message):
    user = message.from_user
    user_id = user.id
    username = user.username or "-"
    first_name = user.first_name or "-"

    voice = message.voice
    file_id = voice.file_id

    session = await get_active_session(user_id)
    if not session:
        await message.answer("⚠️ У тебя ещё нет активной сессии. Напиши /start.")
        return

    brief_id = session["brief_id"]
    fragment_index = session["last_fragment_index"] + 1

    # Логирование во внутреннюю БД
    await log_voice_fragment(
        user_id=user_id,
        username=username,
        first_name=first_name,
        brief_id=brief_id,
        fragment_index=fragment_index,
        file_id=file_id
    )

    await increment_fragment_index(user_id)

    # Отправка в канал
    await send_voice_to_channel(
        user_id=user_id,
        username=username,
        brief_id=brief_id,
        fragment_index=fragment_index,
        file_id=file_id,
        timestamp=format_human_time()
    )

    # Подтверждение пользователю
    await message.answer(f"🎧 Фрагмент №{fragment_index} принят. Добавишь ещё?")