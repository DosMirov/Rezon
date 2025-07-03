from aiogram import Bot
from app.config import settings

async def send_voice_to_channel(
    user_id: int,
    username: str,
    brief_id: str,
    fragment_index: int,
    file_id: str,
    timestamp: str
):
    bot = Bot(token=settings.BOT_TOKEN)

    # Формируем текстовое сообщение
    mention = f"@{username}" if username != "-" else f"ID:{user_id}"
    brief_tag = f"#brief_{brief_id}"
    user_tag = f"#user_{user_id}"
    version_tag = f"#v{fragment_index}"

    message_text = (
        f"🧷 Новый фрагмент:\n"
        f"────────────\n"
        f"👤 {mention}\n"
        f"🗓 {timestamp}\n"
        f"📁 Brief-ID: <code>{brief_id}</code>\n"
        f"🎤 Сообщение №{fragment_index}\n\n"
        f"{brief_tag} {user_tag} {version_tag}"
    )

    # Отправляем текст
    await bot.send_message(settings.CHANNEL_ID, message_text)

    # Отправляем голосовое
    await bot.send_voice(settings.CHANNEL_ID, file_id)