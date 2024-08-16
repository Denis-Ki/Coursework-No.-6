import logging
import smtplib
from datetime import datetime, timedelta
import pytz
from django.core.mail import send_mail
from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.management.base import BaseCommand

from mailing.models import Mailing, MailingLog

logger = logging.getLogger(__name__)


def my_job():
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)
    mailing = Mailing.objects.filter(status__in=[Mailing.STARTED, Mailing.CREATED])
    for email_message in emailmessages:
        # Если достигли end_date, завершить рассылку
        if mailing.end_date and current_datetime >= mailing.end_date:
            mailing.status = Mailing.COMPLETED
            mailing.save()
            continue  # Пропустить отправку, если end_date достигнут
        if mailing.next_send_time and current_datetime >= mailing.next_send_time:
            mailing.status = Mailing.STARTED
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
                    status=Logi.SUCCESS,
                    server_response=server_response,
                    mailing=mailing,
                )
            except smtplib.SMTPException as e:
                MailingLog.objects.create(
                    status=Logi.FAIL,
                    server_response=str(e),
                    mailing=mailing,
                )
            if mailing.periodicity == Mailing.DAILY:
                mailing.next_send_time += timedelta(days=1)
            elif mailing.periodicity == Mailing.WEEKLY:
                mailing.next_send_time += timedelta(weeks=1)
            elif mailing.periodicity == Mailing.MONTHLY:
                mailing.next_send_time += timedelta(days=30)

            mailing.save()


def start_scheduler():
    scheduler = BlockingScheduler()

    if not scheduler.get_jobs():
        scheduler.add_job(my_job, "interval", seconds=30)

    if not scheduler.running:
        scheduler.start()


class Command(BaseCommand):
    help = "Запускает APScheduler для отправки рассылок"

    def handle(self, *args, **options):
        logger.info("Starting scheduler...")
        start_scheduler()
        logger.info("Scheduler started. Press Ctrl+C to exit.")
        try:
            while True:
                pass
        except (KeyboardInterrupt, SystemExit):
            logger.info("Scheduler stopped.")
