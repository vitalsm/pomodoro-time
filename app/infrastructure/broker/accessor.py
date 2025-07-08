import aio_pika

from app.settings import settings


async def get_broker_connection():
    return await aio_pika.connect_robust(settings.celery_broker_url)