import os
import logging
from aiohttp import web
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from app.bot import bot
from app.handlers.register import register_routers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

dp = Dispatcher(storage=MemoryStorage())
register_routers(dp)

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
    await dp.storage.wait_closed()

def create_app() -> web.Application:
    app = web.Application()
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=os.environ["WEBHOOK_PATH"])
    app.router.add_get("/", lambda _: web.Response(text="🤖 Bot is up."))
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    return app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    web.run_app(create_app(), host="0.0.0.0", port=port)
