"""
app/main.py
-----------
aiohttp-based entrypoint that exposes the Telegram webhook and health checks,
initialises the database, registers handlers and shuts everything down cleanly.

Run with:
    python -m app.main
(Used as CMD in Dockerfile)
"""

import asyncio
import logging
import os

from aiohttp import web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler

from app.bot import bot, dp
from app.config import settings
from app.handlers.register import register_routers
from app.storage.db import init_db

# --------------------------------------------------------------------------- #
# Logging
# --------------------------------------------------------------------------- #
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------- #
# Startup / Shutdown hooks
# --------------------------------------------------------------------------- #
async def on_startup(app: web.Application) -> None:
    """Initialises DB, registers routers and sets the Telegram webhook."""
    logger.info("🚀 Starting Rezon Voice Bot…")

    # 1. Init DB (fail-fast on error)
    try:
        await init_db(settings.DATABASE_PATH)
        logger.info("🗄  Database initialised")
    except Exception:
        logger.exception("❌ DB init failed — shutting down")
        raise SystemExit(1)

    # 2. Register routers
    register_routers(dp)
    logger.info("🔌 Routers registered")

    # 3. Refresh webhook
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(url=settings.WEBHOOK_URL, drop_pending_updates=True)

    info = await bot.get_webhook_info()
    me = await bot.get_me()
    logger.info("✅ Webhook set to: %s", info.url)
    logger.info("📨 Pending updates: %s", info.pending_update_count)
    logger.info("🤖 Bot username: @%s", me.username)


async def on_shutdown(app: web.Application) -> None:
    """Gracefully closes bot session and storage."""
    logger.warning("🛑 Shutting down…")

    await bot.delete_webhook()
    await bot.session.close()

    await dp.storage.close()
    await dp.storage.wait_closed()

    logger.info("✅ Shutdown complete")


# --------------------------------------------------------------------------- #
# aiohttp application factory
# --------------------------------------------------------------------------- #
def create_app() -> web.Application:
    app = web.Application()

    # Telegram webhook handler
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(
        app, path=settings.WEBHOOK_PATH
    )

    # Liveness & readiness probes
    app.router.add_get("/", lambda _: web.Response(text="🤖 Bot is up."))
    app.router.add_get("/health", lambda _: web.Response(text="OK"))

    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    return app


# --------------------------------------------------------------------------- #
# Entrypoint
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    logger.info("🌐 Listening on 0.0.0.0:%s", port)

    # Prevent "Task was destroyed but it is pending" errors on Ctrl-C in asyncio
    try:
        web.run_app(create_app(), host="0.0.0.0", port=port)
    except (KeyboardInterrupt, SystemExit):
        logger.info("👋 Bye-bye")
        asyncio.get_event_loop().stop()
