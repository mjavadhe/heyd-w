from celery import shared_task
from django.core.mail import send_mail
from apps.notifications.models import Notification
from django.conf import settings

@shared_task
def send_email_notification(user_email, subject, message):
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        fail_silently=False,
    )

def create_notification(user, title, message, send_email=False):
    # ایجاد اعلان داخلی
    Notification.objects.create(user=user, title=title, message=message)

    # ارسال ایمیل در صورت نیاز
    if send_email:
        send_email_notification.delay(user.email, title, message)
