import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN")
    CHANNEL_ID: int = int(os.getenv("CHANNEL_ID"))
    DATABASE_PATH: str = os.getenv("DATABASE_PATH", "./rezon.db")

settings = Settings()