import os
from functools import lru_cache

from pydantic import BaseSettings, EmailStr, HttpUrl


class Settings(BaseSettings):
    # CORS
    ALLOW_ORIGINS: list[str] = ['*']
    ALLOW_METHODS: list[str] = ['*']
    ALLOW_HEADERS: list[str] = ['*']
    ALLOW_CREDENTIALS: bool = True

    # Authenfication
    SECRET_KEY: str = ''
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    TOKEN_TYPE: str = 'baerer'

    # Celery config
    BROKER_URL: str = ''
    RESULT_BACKEND_URL: str = ''

    # Service email
    EMAIL_URL: HttpUrl = 'https://api.sendinblue.com/v3/smtp/email'
    EMAIL_API_KEY: str = ''
    EMAIL_FROM: EmailStr = 'game.database@play.com'
    EMAIL_NAME: str = 'Game DataBase'

    # Static path
    STATIC_URL: str = os.path.join('src', 'static')

    # Tests
    TEST_RUNNING: bool = False

    # Logger
    QUERY_LOGGER: bool = False

    class Config:
        env_file = os.environ.get('ENV_FILE', '.env.dev')


@lru_cache
def get_settigns() -> Settings:
    return Settings()


settings = get_settigns()
