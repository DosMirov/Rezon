# app/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    BOT_TOKEN: str
    CHANNEL_ID: str
    WEBHOOK_URL: str = "http://localhost:10000/webhook"
    WEBHOOK_PATH: str = "/webhook"

    model_config = SettingsConfigDict(
        env_file='.env.local',
        extra='allow',  # Разрешает любые дополнительные env, чтобы не падало из-за них
    )

settings = Settings()
