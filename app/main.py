import logging
import os
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from app.config import settings
from app.handlers import start, voice, complete
from app.storage.db import init_db

WEBHOOK_PATH = f"/webhook/{settings.BOT_TOKEN}"
WEBHOOK_URL = f"{settings.WEBHOOK_URL}{WEBHOOK_PATH}"

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


async def on_startup(app):
    info = await bot.get_webhook_info()
    if info.url:
        logging.info(f"Deleting old webhook: {info.url}")
        await bot.delete_webhook(drop_pending_updates=True)

    await bot.set_webhook(url=WEBHOOK_URL)
    await init_db()
    logging.info(f"Webhook set to: {WEBHOOK_URL}")

async def on_shutdown(app):
    logging.warning("Shutting down. Removing webhook.")
    await bot.delete_webhook()

def register_handlers():
    start.register(dp)
    voice.register(dp)
    complete.register(dp)

async def handle_webhook(request):
    request_body = await request.text()
    update = types.Update.de_json(request_body)
    await dp.process_update(update)
    return web.Response(text="OK")

def create_app():
    register_handlers()
    app = web.Application()
    app.router.add_post(WEBHOOK_PATH, handle_webhook)  # FIX: use a function, not dp.router
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    return app

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    web.run_app(create_app(), host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
