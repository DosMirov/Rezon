from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.core.brief_manager import get_or_create_brief
from app.storage.repository import get_active_session, create_session
from app.utils.time import get_daystamp

async def handle_start(message: types.Message):
    print("handle_start TRIGGERED")  # LOG
    user_id = message.from_user.id
    username = message.from_user.username or "-"
    first_name = message.from_user.first_name or "-"

    # Проверяем сессию
    session = await get_active_session(user_id)
    if session:
        brief_id = session["brief_id"]
        step = session["last_fragment_index"] + 1
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

    await message.answer(text, reply_markup=kb, parse_mode="HTML")

def register(dp: Dispatcher):
    print("start.py dp id:", id(dp))  # LOG
    dp.register_message_handler(handle_start, commands=["start"])
