import logging
import os
import asyncio

from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.utils.exceptions import RetryAfter
from dotenv import load_dotenv

from app.start import register_handlers
from app.config import settings
from app.core.database import init_db

load_dotenv()

# --- Logging ---
logging.basicConfig(level=logging.INFO)

# --- Init ---
bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher(bot)
WEBHOOK_URL = f"{settings.WEBHOOK_BASE}/{settings.BOT_TOKEN}"


async def on_startup(app: web.Application):
    logging.info("Running on_startup...")

    # Set current context
    Bot.set_current(bot)
    Dispatcher.set_current(dp)

    await init_db(settings.DATABASE_PATH)

    try:
        current = await bot.get_webhook_info()
        if current.url != WEBHOOK_URL:
            logging.info(f"Current webhook: {current.url} → updating to {WEBHOOK_URL}")
            await bot.set_webhook(WEBHOOK_URL)
        else:
            logging.info("Webhook is already set correctly. Skipping.")
    except RetryAfter as e:
        logging.warning(f"Flood control triggered. Retry after {e.timeout} seconds.")
        await asyncio.sleep(e.timeout)
        try:
            await bot.set_webhook(WEBHOOK_URL)
            logging.info(f"Webhook set after retry.")
        except Exception as inner_e:
            logging.error(f"Retry failed: {inner_e}")
    except Exception as e:
        logging.error(f"Webhook setup error: {e}")


async def handle_webhook(request: web.Request):
    try:
        body = await request.read()
        update = types.Update(**types.json.loads(body.decode("utf-8")))
        await dp.process_update(update)
    except Exception as e:
        logging.error(f"Error in webhook handler: {e}")
    return web.Response(status=200)


async def on_shutdown(app: web.Application):
    logging.info("Shutting down...")


def create_app() -> web.Application:
    app = web.Application()
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    app.router.add_post(f"/webhook/{settings.BOT_TOKEN}", handle_webhook)

    register_handlers(dp)
    logging.info(f"main.py dp id: {id(dp)}")

    return app


if __name__ == "__main__":
    web.run_app(
        create_app(),
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )