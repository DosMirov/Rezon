from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    BOT_TOKEN: str
    CHANNEL_ID: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
