from aiogram import Dispatcher
from .start import router as start_router
from .complete import router as complete_router
from .universal import router as universal_router  # если он есть
from .fallback import router as fallback_router

def register_routers(dp: Dispatcher):
    dp.include_router(start_router)
    dp.include_router(complete_router)
    dp.include_router(universal_router)
    dp.include_router(fallback_router)  # 👉 ВСЕГДА последним!
