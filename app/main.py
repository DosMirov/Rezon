import os
import logging
from dotenv import load_dotenv

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from app.bot import register_routers
from app.config import settings
from app.storage.db import init_db

load_dotenv()

# Вебхук: путь и публичный URL
WEBHOOK_PATH = f"/webhook/{settings.BOT_TOKEN}"
WEBHOOK_URL = f"{settings.BASE_WEBHOOK_URL}{WEBHOOK_PATH}"

# Логирование
logging.basicConfig(level=logging.INFO)

async def on_startup(app: web.Application):
    bot: Bot = app["bot"]
    logging.info(f"📡 Setting webhook to: {WEBHOOK_URL}")
    await bot.set_webhook(WEBHOOK_URL)

    logging.info("🗃 Initializing SQLite...")
    await init_db(settings.DATABASE_PATH)
    logging.info("✅ DB ready.")

async def on_shutdown(app: web.Application):
    bot: Bot = app["bot"]
    logging.info("❌ Removing webhook...")
    await bot.delete_webhook()

def create_app() -> web.Application:
    # Инициализация бота и диспетчера
    bot = Bot(token=settings.BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    register_routers(dp)

    # HTTP-приложение
    app = web.Application()
    app["bot"] = bot

    # Регистрируем webhook endpoint
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)

    # Хуки запуска и остановки
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    return app

if __name__ == "__main__":
    # Render слушает порт через переменную окружения $PORT
    port = int(os.environ.get("PORT", 8000))
    web.run_app(create_app(), host="0.0.0.0", port=port)