from aiogram import Router
from app.handlers import start, voice, complete

def register_routers() -> Router:
    router = Router()
    router.include_router(start.router)
    router.include_router(voice.router)
    router.include_router(complete.router)
    return router