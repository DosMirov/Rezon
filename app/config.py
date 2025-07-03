from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    BOT_TOKEN: str
    WEBHOOK_URL: str = Field(default="", env="WEBHOOK_URL")  # ⬅ fallback

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()