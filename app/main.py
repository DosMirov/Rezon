import os
import sys
import logging

from aiohttp import web
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler

from app.bot import bot
from app.handlers.register import register_routers

print(">>> BOT CONTAINER STARTED <<<")
print("BOT_TOKEN:", os.environ.get("BOT_TOKEN"))
print("CHANNEL_ID:", os.environ.get("CHANNEL_ID"))
print("WEBHOOK_URL:", os.environ.get("WEBHOOK_URL"))
print("WEBHOOK_PATH:", os.environ.get("WEBHOOK_PATH"))
print("Current directory:", os.getcwd())
print("Dirlist:", os.listdir("."))
print("### BOOT ### env:", {k: os.getenv(k) for k in ("BOT_TOKEN", "CHANNEL_ID", "WEBHOOK_URL", "WEBHOOK_PATH")}, file=sys.stderr, flush=True)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

dp = Dispatcher(storage=MemoryStorage())
register_routers(dp)  # <-- Весь import/регистрация — ТОЛЬКО тут!

async def on_startup(app: web.Application):
    logger.info("🚀 Starting Rezon Stateless Bot…")
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(
        url=os.environ["WEBHOOK_URL"],
        drop_pending_updates=True,
    )
    info = await bot.get_webhook_info()
    logger.info(f"✅ Webhook set to: {info.url}")
    logger.info(f"🤖 Bot username: @{(await bot.get_me()).username}")

async def on_shutdown(app: web.Application):
    logger.warning("🛑 Shutting down…")
    await bot.delete_webhook()
    await bot.session.close()
    await dp.storage.close()

def create_app() -> web.Application:
    app = web.Application()
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=os.environ["WEBHOOK_PATH"])
    app.router.add_get("/", lambda _: web.Response(text="🤖 Bot is up."))
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    return app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print(">>> Ready to run aiohttp web app <<<")
    web.run_app(create_app(), host="0.0.0.0", port=port)

# ⛔️ Ничего ниже!  
