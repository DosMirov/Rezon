import json
import logging
from aiohttp import web
from aiogram import types, Dispatcher

logger = logging.getLogger(__name__)

def setup_webhook(app, dp: Dispatcher, webhook_path: str):
    async def handle_webhook(request):
        request_body = await request.text()
        try:
            data = json.loads(request_body)
            update = types.Update(**data)
            await dp.process_update(update)
        except Exception as e:
            logger.exception(f"Webhook error: {e}")
        return web.Response(text="OK")

    app.router.add_post(webhook_path, handle_webhook)
