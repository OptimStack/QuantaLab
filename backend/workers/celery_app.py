import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from celery import Celery
    from config import settings
    
    celery_app = Celery(
        "quantalab",
        broker=settings.redis_url,
        backend=settings.redis_url
    )
    celery_app.autodiscover_tasks(["app.simulation.tasks", "app.assessments.tasks"])
except ImportError:
    celery_app = None
