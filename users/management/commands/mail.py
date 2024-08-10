from django.core.mail import send_mail
from django.conf import settings
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        subject = 'text message'
        message = 'Это тестовое письмо, отправленное с помощью Django и Яндекс SMTP-сервера.'
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = 'www.wolk94@gmail.com'

        send_mail(
            subject,
            message,
            from_email,
            [to_email],
            fail_silently=False,
        )

        self.stdout.write(self.style.SUCCESS('Email sent successfully!'))
