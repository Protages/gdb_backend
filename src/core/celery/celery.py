from celery import Celery


celery = Celery('celery-app')

celery.config_from_object('src.core.celery.celeryconfig')
