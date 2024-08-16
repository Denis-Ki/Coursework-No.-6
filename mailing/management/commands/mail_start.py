import smtplib
from config import settings
from django.core.management import BaseCommand
from django.core.mail import send_mail

from mailing.models import Mailing, MailingLog


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        mailings = Mailing.objects.filter(status="Запущена")
        for mailing in mailings:
            clients = mailing.clients.all()
            try:
                server_response = send_mail(
                    subject=mailing.message.subject,
                    message=mailing.message.message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[client.email for client in clients],
                    fail_silently=False,
                )
                MailingLog.objects.create(
                    status=MailingLog.SUCCESS,
                    server_response=server_response,
                    mailing=mailing,
                )
            except smtplib.SMTPException as e:
                MailingLog.objects.create(
                    status=MailingLog.FAIL,
                    server_response=str(e),
                    mailing=mailing,
                )
                print(f"Ошибка при отправке письма: {str(e)}")
