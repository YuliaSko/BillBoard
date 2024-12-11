import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ad_board.settings')

app = Celery('ad_board')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'send_email_every_monday_8am': {
        'task': 'board.tasks.send_weekly_email',
        'schedule': crontab(),
        'args': (),
    }
}

app.conf.timezone = 'UTC'

# hour=8, minute=0, day_of_week='monday'