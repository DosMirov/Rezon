from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    BOT_TOKEN: str
    WEBHOOK_URL: str = Field(default="", env="WEBHOOK_URL")
    WEBHOOK_PATH: str = Field(default="/webhook", env="WEBHOOK_PATH")
    BASE_WEBHOOK_URL: str = Field(default="", env="BASE_WEBHOOK_URL")
    CHANNEL_ID: int
    DATABASE_PATH: str = Field(default="./rezon.db", env="DATABASE_PATH")  # ← this was missing

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()