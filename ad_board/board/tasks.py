import datetime

from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from ad_board import settings
from .models import Ad, User


@shared_task
def send_weekly_email():
    today = datetime.datetime.now()
    week = today - datetime.timedelta(days=7)
    ads = Ad.objects.filter(date__gte=week)
    users = User.objects.values_list('email', flat=True)

    html_content = render_to_string(
        'weekly_email.html',
        {
            'link': settings.SITE_URL,
            'ads': ads
        }
    )

    msg = EmailMultiAlternatives(
        subject='Еженедельная рассылка объявлений',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=users
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()
