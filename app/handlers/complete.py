from aiogram import types, Dispatcher
from app.storage.repository import get_active_session, complete_session

async def handle_done_command(message: types.Message):
    user_id = message.from_user.id
    session = await get_active_session(user_id)

    if not session:
        await message.answer("⚠️ У тебя нет активной сессии.")
        return

    await complete_session(user_id)
    await message.answer("✅ Кейс зафиксирован. Спасибо за доверие.")

async def handle_done_button(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    session = await get_active_session(user_id)

    if not session:
        await callback.answer("Нет активной сессии.")
        return

    await complete_session(user_id)
    await callback.message.edit_text("✅ Кейс зафиксирован. Спасибо за доверие.")
    await callback.answer()

def register(dp: Dispatcher):
    dp.register_message_handler(handle_done_command, commands=["done"])
    dp.register_callback_query_handler(handle_done_button, lambda c: c.data == "complete_session")