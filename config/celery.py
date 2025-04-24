import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('eshop')
app.conf.beat_schedule = {
    'expire_and_deactivate_carts_every_5_minutes': {
        'task': 'cart.tasks.expire_and_deactivate_carts',
        'schedule': crontab(minute='*/5'),
    },
}
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
