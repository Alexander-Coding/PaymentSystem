"""
    Файл инициализирует класс Settings, хранящий основные настройки приложения.
"""

from dotenv import load_dotenv
from pydantic.v1 import BaseSettings


load_dotenv()


class Settings(BaseSettings):
    # Параметры подключения к базе данных Postgres
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    # Секретный ключ для шифрования токенов
    SECRET_KEY: str

    class Config:
        env_file = '../.env'
        env_file_encoding = "utf-8"

    @property
    def DATABASE_URL_asyncpg(self):
        """Получение ссылки на подключение к базе данных PostgreSQL через asyncpg"""
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DATABASE_URL_psycopg(self):
        """Получение ссылки на подключение к базе данных PostgreSQL через psycopg"""
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @classmethod
    def create(cls):
        return cls()


settings = Settings.create()


__all__ = [
    'settings'
]
