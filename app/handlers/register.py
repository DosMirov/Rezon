"""
app/handlers/register.py
------------------------
Attach all module routers to the shared Dispatcher.
Import and call `register_routers(dp)` exactly once in main.py.
"""

from aiogram import Dispatcher

from app.handlers.start import router as start_router
from app.handlers.complete import router as complete_router
from app.handlers.universal import router as universal_router


def register_routers(dp: Dispatcher) -> None:
    """
    Register all handler routers on the given Dispatcher.
    """
    dp.include_router(start_router)
    dp.include_router(complete_router)
    dp.include_router(universal_router)
