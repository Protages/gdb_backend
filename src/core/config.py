from functools import lru_cache

from pydantic import BaseSettings, EmailStr, HttpUrl

TESTS_RUNNING: bool = False


class Settings(BaseSettings):
    # CORS
    ALLOW_ORIGINS: list[str] = ['*']
    ALLOW_METHODS: list[str] = ['*']
    ALLOW_HEADERS: list[str] = ['*']
    ALLOW_CREDENTIALS: bool = True

    # Authenfication
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    TOKEN_TYPE: str = 'baerer'

    # Celery config
    BROKER_URL: str
    RESULT_BACKEND_URL: str

    # Service email
    EMAIL_URL: HttpUrl = 'https://api.sendinblue.com/v3/smtp/email'
    EMAIL_API_KEY: str
    EMAIL_FROM: EmailStr = 'game.database@play.com'
    EMAIL_NAME: str = 'Game DataBase'

    # Tests
    TESTS_RUNNING: bool = TESTS_RUNNING

    class Config:
        env_file = '.env.dev'


@lru_cache
def get_settigns() -> Settings:
    return Settings()


settings = get_settigns()
