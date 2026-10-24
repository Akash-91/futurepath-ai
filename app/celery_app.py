from celery import Celery

from .config import settings

celery_app = Celery("futurepath_ai", broker=settings.redis_url, backend=settings.redis_url)
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    task_track_started=True,
    timezone="UTC",
    broker_connection_retry_on_startup=True,
)

celery_app.autodiscover_tasks(["app"])
