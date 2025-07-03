import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from dotenv import load_dotenv
import os

from app.bot import register_routers
from app.config import settings
from app.storage.db import init_db

logging.basicConfig(level=logging.INFO)
load_dotenv()  # Загрузка переменных из .env

async def main():
    # Инициализация бота и диспетчера
    bot = Bot(token=settings.BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    # Инициализация SQLite-хранилища
    await init_db(settings.DATABASE_PATH)

    # Регистрация маршрутов
    register_routers(dp)

    # Запуск polling
    logging.info("🚀 Bot is running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())