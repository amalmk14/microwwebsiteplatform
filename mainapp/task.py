# tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from datetime import timedelta
from .models import Orders, PaymentSuccess
from django.utils import timezone

@shared_task
def send_expiry_notification():
    last_7_days = timezone.now() + timedelta(days=7)
    last_1_day = timezone.now() + timedelta(days=1)

    # Orders expiring in the last 7 days
    expiring_soon = PaymentSuccess.objects.filter(expiry_date__lte=last_7_days, expiry_date__gt=timezone.now())

    for payment_success in expiring_soon:
        send_expiry_email(payment_success.order.email, payment_success.order)

    # Orders expiring in the last 1 day
    expiring_today = PaymentSuccess.objects.filter(expiry_date__lte=last_1_day, expiry_date__gt=timezone.now())

    for payment_success in expiring_today:
        send_expiry_email(payment_success.order.email, payment_success.order)

    # Orders that have already expired
    expired_orders = PaymentSuccess.objects.filter(expiry_date__lte=timezone.now())

    for payment_success in expired_orders:
        send_expiry_email(payment_success.order.email, payment_success.order)

def send_expiry_email(email, order):
    subject = 'Template Expiry Notification'
    message = render_to_string('email/expiry_notification_email.html', {'order': order})
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [email]

    send_mail(subject, message, from_email, to_email, fail_silently=False)


