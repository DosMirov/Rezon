from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
from app.config import settings
from app.bot import dp, bot

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "ok"}

@app.post("/webhook")
async def telegram_webhook(req: Request):
    body = await req.body()
    update = types.Update.parse_raw(body)
    await dp.process_update(update)
    return {"ok": True}