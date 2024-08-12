import smtplib
from config import settings
from email_massages.models import EmailMessage
from django.core.management import BaseCommand
from django.core.mail import send_mail

from logi.models import Logi


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        emailmessages = EmailMessage.objects.filter(status="Запущена")
        for email_message in emailmessages:
            clients = email_message.clients.all()
            try:
                server_response = send_mail(
                    subject=email_message.message.subject,
                    message=email_message.message.message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[client.email for client in clients],
                    fail_silently=False,
                )
                Logi.objects.create(
                    status=Logi.SUCCESS,
                    server_response=server_response,
                    email_message=email_message,
                )
            except smtplib.SMTPException as e:
                Logi.objects.create(
                    status=Logi.FAIL,
                    server_response=str(e),
                    email_message=email_message,
                )
                print(f"Ошибка при отправке письма: {str(e)}")
