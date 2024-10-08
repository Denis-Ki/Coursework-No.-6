# Generated by Django 4.2.2 on 2024-08-10 15:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Client",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        help_text="введите email",
                        max_length=254,
                        unique=True,
                        verbose_name="Email",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="введите ФИО", max_length=150, verbose_name="ФИО"
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="clients",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Клиент",
                "verbose_name_plural": "Клиенты",
            },
        ),
        migrations.CreateModel(
            name="Mailing",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="введите название рассылки",
                        max_length=150,
                        verbose_name="Название",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="введите описание рассылки (необязательное поле)",
                        null=True,
                        verbose_name="Описание",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Завершена", "Завершена"),
                            ("Создана", "Создана"),
                            ("Запущена", "Запущена"),
                        ],
                        default="Создана",
                        max_length=150,
                        verbose_name="Статус рассылки",
                    ),
                ),
                (
                    "periodicity",
                    models.CharField(
                        choices=[
                            ("Раз в день", "Раз в день"),
                            ("Раз в неделю", "Раз в неделю"),
                            ("Раз в месяц", "Раз в месяц"),
                        ],
                        default="Раз в день",
                        max_length=150,
                        verbose_name="Периодичность",
                    ),
                ),
                (
                    "start_date",
                    models.DateTimeField(
                        blank=True,
                        help_text="(формат дд.мм.гггг) не обязательное поле",
                        null=True,
                        verbose_name="Дата начала",
                    ),
                ),
                (
                    "end_date",
                    models.DateTimeField(
                        blank=True,
                        help_text="не обязательное поле",
                        null=True,
                        verbose_name="Дата окончания",
                    ),
                ),
                (
                    "next_send_time",
                    models.DateTimeField(
                        blank=True,
                        help_text="(формат дд.мм.гггг чч:мм:сс) обязательное поле",
                        null=True,
                        verbose_name="Время следующей отправки",
                    ),
                ),
                (
                    "clients",
                    models.ManyToManyField(
                        related_name="mailing",
                        to="mailing.client",
                        verbose_name="Клиенты для рассылки",
                    ),
                ),
            ],
            options={
                "verbose_name": "Рассылка",
                "verbose_name_plural": "Рассылки",
                "ordering": ("name",),
                "permissions": [
                    ("deactivate_emailmessage", "Can deactivate mailing"),
                    ("view_all_emailmessage", "Can view all mailings"),
                ],
            },
        ),
        migrations.CreateModel(
            name="Message",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "subject",
                    models.CharField(
                        help_text="введите тему сообщения",
                        max_length=255,
                        verbose_name="Тема",
                    ),
                ),
                (
                    "message",
                    models.TextField(
                        help_text="введите текст сообщения", verbose_name="Сообщение"
                    ),
                ),
            ],
            options={
                "verbose_name": "Сообщение",
                "verbose_name_plural": "Сообщения",
            },
        ),
        migrations.CreateModel(
            name="MailingLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "time",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата и время попытки отправки"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("Успешно", "Успешно"), ("Неуспешно", "Неуспешно")],
                        max_length=50,
                        verbose_name="Cтатус рассылки",
                    ),
                ),
                (
                    "server_response",
                    models.CharField(
                        blank=True,
                        max_length=150,
                        null=True,
                        verbose_name="Ответ сервера почтового сервиса",
                    ),
                ),
                (
                    "mailing",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="mailing.mailing",
                        verbose_name="Рассылка",
                    ),
                ),
            ],
            options={
                "verbose_name": "Попытка рассылки",
                "verbose_name_plural": "Попытки рассылок",
            },
        ),
        migrations.AddField(
            model_name="mailing",
            name="message",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="mailing.message",
                verbose_name="Cообщение",
            ),
        ),
        migrations.AddField(
            model_name="mailing",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Владелец",
            ),
        ),
    ]
