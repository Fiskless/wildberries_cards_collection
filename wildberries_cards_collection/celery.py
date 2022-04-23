import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wildberries_cards_collection.settings')

app = Celery('wildberries_cards_collection')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'update-wb-data-every-1-hour': {
        'task': 'cards.tasks.update_beat_product_data_every_1_hour',
        'schedule': crontab(minute=0, hour='*/1'),
    },
    'update-wb-data-every-12-hours': {
        'task': 'cards.tasks.update_beat_product_data_every_12_hours',
        'schedule': crontab(minute=0, hour='*/12'),
    },
    'update-wb-data-every-24-hours': {
        'task': 'cards.tasks.update_beat_product_data_every_24_hours',
        'schedule': crontab(minute=0, hour='*/24'),
    },
}
