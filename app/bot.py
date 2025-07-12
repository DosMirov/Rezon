from aiogram import Bot
from app.config import settings

bot = Bot(token=settings.BOT_TOKEN, parse_mode="HTML")
