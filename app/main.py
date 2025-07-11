import os
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from app.config import settings
from app.handlers.register import register_routers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === Инициализация бота и диспетчера ===
bot = Bot(token=settings.BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(storage=MemoryStorage())
register_routers(dp)


# === on_startup ===
async def on_startup(app: web.Application):
    logger.info("⚙️ on_startup triggered")

    # Настройка webhook
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(
        url=settings.WEBHOOK_URL,
        drop_pending_updates=True,
    )
    webhook_info = await bot.get_webhook_info()
    logger.info(f"✅ Webhook set: {webhook_info.url}")
    logger.info(f"📨 Pending updates: {webhook_info.pending_update_count}")

    logger.info("🔧 Dispatcher ID: %s", id(dp))
    logger.info("🔧 Bot username: %s", (await bot.get_me()).username)


# === on_shutdown ===
async def on_shutdown(app: web.Application):
    logger.warning("🛑 Shutting down...")
    await bot.delete_webhook()
    await bot.session.close()
    await dp.storage.close()
    await dp.storage.wait_closed()
    logger.info("✅ Shutdown complete.")


# === create_app ===
def create_app() -> web.Application:
    app = web.Application()

    # Регистрируем webhook route
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=settings.WEBHOOK_PATH)

    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    # Debug route
    app.router.add_get("/", lambda _: web.Response(text="✅ Bot is running."))

    return app


# === entrypoint ===
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Zeabur использует $PORT
    web.run_app(create_app(), host="0.0.0.0", port=port)