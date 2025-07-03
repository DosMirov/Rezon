from aiogram import Dispatcher
from aiogram import Router

from app.handlers import start, voice, complete

def register_routers(dp: Dispatcher):
    main_router = Router()
    
    # Регистрируем все хендлеры
    main_router.include_router(start.router)
    main_router.include_router(voice.router)
    main_router.include_router(complete.router)

    dp.include_router(main_router)