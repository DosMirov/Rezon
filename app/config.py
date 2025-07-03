from pydantic import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str
    WEBHOOK_URL: str = ""  # можно задать пустую строку как fallback

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()