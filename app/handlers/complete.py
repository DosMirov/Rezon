from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

router = Router()

@router.message(F.text == "/done")
async def handle_done_command(message: Message):
    await message.answer("✅ Кейс зафиксирован. Спасибо за доверие!")

@router.callback_query(F.data == "complete_session")
async def handle_done_button(callback: CallbackQuery):
    try:
        await callback.message.edit_text("✅ Кейс зафиксирован. Спасибо за доверие!")
    except Exception:
        pass
    await callback.answer("Сессия завершена.", show_alert=False)
