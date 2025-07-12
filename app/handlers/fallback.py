from aiogram import Router, types

router = Router()

@router.message()                # без фильтров = перехват всего остального
async def fallback(message: types.Message):
    print("FALLBACK:", message.text, flush=True)
    await message.answer("Бот услышал: " + (message.text or "файл/медиа"))
