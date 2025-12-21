import logging
from pydantic_settings import BaseSettings, SettingsConfigDict


# Модель настроек для приложения
class Settings(BaseSettings):
    postgres_db: str
    postgres_user: str
    postgres_password: str
    secret_key: str
    algorithm: str
    access_token_expire_seconds: int

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding="utf8",
        extra="ignore"
    )


settings = Settings()


# Настройки логирования
logging.basicConfig(
    level=logging.DEBUG,
    # filename='bot_log.log',
    format="%(asctime)s - %(name)s - %(filename)s - %(funcName)s - %(levelname)s: %(message)s"
)
logger = logging.getLogger(__name__)
