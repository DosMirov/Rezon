from aiogram import Dispatcher
from app.handlers.start import router as start_router
from app.handlers.complete import router as complete_router
from app.handlers.universal import router as universal_router

def register_routers(dp: Dispatcher):
    dp.include_router(start_router)
    dp.include_router(complete_router)
    dp.include_router(universal_router)   # всегда последним!
