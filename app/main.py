import logging
import os
import json
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

def register_handlers():
    print("Registering handlers...")
    start.register(dp)
    voice.register(dp)
    complete.register(dp)

async def on_startup(app):
    info = await bot.get_webhook_info()
    if info.url:
        logging.info(f"Deleting old webhook: {info.url}")
        await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(url=WEBHOOK_URL)
    await init_db(settings.DATABASE_PATH)
    logging.info(f"Webhook set to: {WEBHOOK_URL}")

async def on_shutdown(app):
    logging.warning("Shutting down. Removing webhook.")
    await bot.delete_webhook()

async def handle_webhook(request):
    try:
        request_body = await request.text()
        data = json.loads(request_body)
        update = types.Update(**data)
        # 🧩 Aiogram 2.x context injection
        bot.set_current(bot)
        dp.bot.set_current(dp.bot)
        await dp.process_update(update)
    except Exception as e:
        logging.error(f"Error in webhook handler: {e}")
    return web.Response(text="OK")

def create_app():
    register_handlers()
    print("main.py dp id:", id(dp))
    app = web.Application()
    app.router.add_post(WEBHOOK_PATH, handle_webhook)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    return app

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    web.run_app(create_app(), host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
