"""
app/bot.py
-----------
Single-source initialization of the Telegram Bot and Dispatcher.
Import `bot` and `dp` from this module **everywhere** (handlers, services, main.py)
to guarantee one shared connection pool and one FSM storage.

Change‐log (production ready):
• Centralised Bot/Dispatcher creation
• MemoryStorage kept for simplicity; swap to RedisStorage when scaling horizontally
• No side effects beyond object creation — safe to import anywhere
"""

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from app.config import settings

# --- Singleton instances ---------------------------------------------------- #
bot = Bot(token=settings.BOT_TOKEN, parse_mode="HTML")          # re-use only!
dp = Dispatcher(storage=MemoryStorage())

__all__ = ["bot", "dp"]
