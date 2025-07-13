from aiogram import Router, F, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.utils.time import get_daystamp
from app.session import get_session, set_state  # 👈 RAM FSM API

router = Router()  # экспортируем router

def make_brief_id(user_id: int, day: str) -> str:
    return f"BRF-{user_id}_{day}"

@router.message(F.text, F.text.startswith("/start"))
async def cmd_start(message: types.Message):
    print("HANDLER /start TRIGGERED", flush=True)

    # 1. RAM-сессия, инициализация + state
    user_id = message.from_user.id
    get_session(user_id)
    set_state(user_id, "WELCOME")

    brief_id = make_brief_id(user_id, get_daystamp())

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Завершить", callback_data="complete_session")]
        ]
    )
    await message.answer(
        (
            "🧭 REZON_X — архитектурный навигатор\n\n"
            f"<b>Brief-ID:</b> <code>{brief_id}</code>\n"
            "Отправляй сообщения-фрагменты. Когда закончишь — жми кнопку."
        ),
        reply_markup=kb,
        parse_mode="HTML",
    )
