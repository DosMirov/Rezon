# app/main.py

import os
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from app.config import settings
from app.handlers.register import register_routers

# === Логгер ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === Инициализация бота и диспетчера ===
bot = Bot(token=settings.BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(storage=MemoryStorage())
register_routers(dp)

# === Хуки ===
async def on_startup(app: web.Application):
    logger.info("⚙️ on_startup triggered")

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(
        url=settings.WEBHOOK_URL,
        drop_pending_updates=True,
    )

    info = await bot.get_webhook_info()
    logger.info(f"✅ Webhook set: {info.url}")
    logger.info(f"📨 Pending updates: {info.pending_update_count}")
    logger.info(f"🔧 Bot: @{(await bot.get_me()).username}")
    logger.info(f"🧠 Dispatcher ID: {id(dp)}")

async def on_shutdown(app: web.Application):
    logger.warning("🛑 Shutting down...")
    await bot.delete_webhook()
    await bot.session.close()
    await dp.storage.close()
    await dp.storage.wait_closed()
    logger.info("✅ Shutdown complete.")

# === Приложение aiohttp ===
def create_app() -> web.Application:
    app = web.Application()
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=settings.WEBHOOK_PATH)
    app.router.add_get("/", lambda _: web.Response(text="🤖 Bot is up."))
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    return app

# === Entrypoint ===
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    web.run_app(create_app(), host="0.0.0.0", port=port)