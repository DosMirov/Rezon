from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from app.storage.repository import get_active_session, complete_session

router = Router()

@router.message(F.text == "/done")
async def handle_done_command(message: Message):
    user_id = message.from_user.id
    session = await get_active_session(user_id)

    if not session:
        await message.answer("⚠️ У тебя нет активной сессии.")
        return

    await complete_session(user_id)
    await message.answer("✅ Кейс зафиксирован. Спасибо за доверие.")

@router.callback_query(F.data == "complete_session")
async def handle_done_button(callback: CallbackQuery):
    user_id = callback.from_user.id
    session = await get_active_session(user_id)

    if not session:
        await callback.answer("Нет активной сессии.")
        return

    await complete_session(user_id)
    await callback.message.edit_text("✅ Кейс зафиксирован. Спасибо за доверие.")
    await callback.answer()