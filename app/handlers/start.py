from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from app.core.brief_manager import get_or_create_brief
from app.storage.repository import get_active_session, create_session
from app.utils.time import get_daystamp
from app.config import settings

router = Router()

@router.message(F.text == "/start")
async def handle_start(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username or "-"
    first_name = message.from_user.first_name or "-"

    # Проверяем или создаём сессию
    existing_session = await get_active_session(user_id)
    if existing_session:
        brief_id = existing_session["brief_id"]
        step = existing_session["last_fragment_index"] + 1
    else:
        daystamp = get_daystamp()
        brief_id = get_or_create_brief(user_id, daystamp)
        await create_session(user_id, brief_id)
        step = 1

    text = (
        "👋 Привет. Я регистрирую твой кейс.\n\n"
        "Отправь голосовое сообщение — каждый фрагмент будет сохранён.\n"
        f"<b>Brief-ID:</b> <code>{brief_id}</code>\n\n"
        "🗣 Готов говорить?"
    )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎤 Отправить голос", switch_inline_query_current_chat="")],
        [InlineKeyboardButton(text="✅ Завершить", callback_data="complete_session")]
    ])

    await message.answer(text, reply_markup=kb)