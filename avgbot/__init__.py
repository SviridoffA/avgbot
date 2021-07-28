# импортируем из  celery.py объект(экземпляр класса) celery (app)
from .celery import app as celery_app
# Подключаем объект
__all__ = ('celery_app',)
