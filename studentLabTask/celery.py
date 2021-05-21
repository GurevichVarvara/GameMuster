import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studentLabTask.settings')

app = Celery('studentLabTask')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'add_new_games': {
        'task': 'gameMuster.tasks.refresh_games',
        'schedule': 100.0
    }
}
