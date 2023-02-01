from src.core.config import settings


broker_url = settings.BROKER_URL
result_backend = settings.RESULT_BACKEND_URL

imports = ['src.core.celery.tasks']
