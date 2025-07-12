from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from app.utils.time import get_daystamp

router = Router()

def make_brief_id(user_id: int, daystamp: str) -> str:
    return f"BRF-{user_id}_{daystamp}"

@router.message(F.text, F.text.startswith("/start"))
async def handle_start(message: Message):
    user_id = message.from_user.id
    daystamp = get_daystamp()
    brief_id = make_brief_id(user_id, daystamp)

    text = (
        "👋 Привет! Я помогу зафиксировать твой кейс/обратную связь.\n\n"
        "Просто отправляй любые сообщения — голос, текст, фото, файл, кружок.\n"
        f"<b>Brief-ID:</b> <code>{brief_id}</code>\n\n"
        "Когда закончишь — нажми «Завершить»."
    )

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Завершить", callback_data="complete_session")]
        ]
    )
    await message.answer(text, reply_markup=kb, parse_mode="HTML")
