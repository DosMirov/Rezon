import asyncio
import logging
import uvicorn

from app.bot import bot
from app.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def setup_webhook():
    await bot.delete_webhook()  # чистим предыдущий (опционально)
    await bot.set_webhook(url=settings.WEBHOOK_URL)
    logger.info(f"Webhook set to: {settings.WEBHOOK_URL}")


def start():
    # Render запускает этот файл: запуск FastAPI-сервера на app/webhook:app
    uvicorn.run(
        "app.webhook:app",
        host="0.0.0.0",
        port=10000,
        reload=False
    )


if __name__ == "__main__":
    asyncio.run(setup_webhook())
    start()