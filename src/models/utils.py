from src.core.config import settings


def get_static_url() -> str:
    return settings.STATIC_URL
