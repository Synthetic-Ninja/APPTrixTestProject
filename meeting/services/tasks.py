from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_email_with_match(subject, message_text, from_email, recipient_list):
    send_mail(subject=subject,
              message=message_text,
              from_email=from_email,
              recipient_list=recipient_list,
              fail_silently=False
              )
