from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    BOT_TOKEN: str
    BASE_WEBHOOK_URL: str = Field(..., env="BASE_WEBHOOK_URL")
    WEBHOOK_PATH: str = Field(default="/webhook", env="WEBHOOK_PATH")
    CHANNEL_ID: int
    DATABASE_PATH: str = Field(default="./rezon.db", env="DATABASE_PATH")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def WEBHOOK_URL(self) -> str:
        return f"{self.BASE_WEBHOOK_URL.rstrip('/')}{self.WEBHOOK_PATH}"

settings = Settings()