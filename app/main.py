import logging
import os
from aiohttp import web
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from app.config import settings
from app.storage.db import init_db
from app.handlers import start, voice, complete

load_dotenv()
logging.basicConfig(level=logging.INFO)

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Регистрируем хендлеры (ручной стиль aiogram 2.x)
start.register(dp)
voice.register(dp)
complete.register(dp)

# 📡 Aiohttp webhook handler
async def handle_webhook(request):
    try:
        data = await request.json()
        update = types.Update.to_object(data)
        await dp.process_update(update)
    except Exception as e:
        logging.exception("Webhook handling failed.")
    return web.Response()

# 📦 Приложение aiohttp
def create_app():
    app = web.Application()
    app.router.add_post(f'/webhook/{settings.BOT_TOKEN}', handle_webhook)

    async def on_startup(app):
        await init_db(settings.DATABASE_PATH)
        await bot.set_webhook(f"{settings.BASE_WEBHOOK_URL}/webhook/{settings.BOT_TOKEN}")
        logging.info("✅ Webhook set.")

    async def on_shutdown(app):
        await bot.delete_webhook()
        logging.info("🔌 Webhook deleted.")

    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    return app

# 🔧 Запуск на Render (PORT будет задан в env)
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    web.run_app(create_app(), host='0.0.0.0', port=port)