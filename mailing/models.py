from django.db import models
from users.models import User


NULLABLE = {"blank": True, "null": True}


class Client(models.Model):
    """
    Модель клиента
    """

    email = models.EmailField(
        verbose_name="Email", unique=True, help_text="введите email"
    )
    name = models.CharField(max_length=150, verbose_name="ФИО", help_text="введите ФИО")
    comments = models.TextField(
        verbose_name="Comments", **NULLABLE, help_text="коментарии"
    )
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="clients", **NULLABLE
    )

    def __str__(self):
        return f"{self.email}: {self.name}"

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Message(models.Model):
    """
    Модель сообщения
    """

    subject = models.CharField(
        max_length=255, verbose_name="Тема", help_text="введите тему сообщения"
    )
    message = models.TextField(
        verbose_name="Сообщение", help_text="введите текст сообщения"
    )
    owner = models.ForeignKey(
        User, verbose_name="Владелец", on_delete=models.SET_NULL, **NULLABLE
    )

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


class Mailing(models.Model):
    """
    Модель рассылки
    """

    DAILY = "Раз в день"
    WEEKLY = "Раз в неделю"
    MONTHLY = "Раз в месяц"

    PERIODICITY_CHOICES = [
        (DAILY, "Раз в день"),
        (WEEKLY, "Раз в неделю"),
        (MONTHLY, "Раз в месяц"),
    ]

    CREATED = "Создана"
    STARTED = "Запущена"
    COMPLETED = "Завершена"

    STATUS_CHOICES = [
        (COMPLETED, "Завершена"),
        (CREATED, "Создана"),
        (STARTED, "Запущена"),
    ]

    name = models.CharField(
        max_length=150, verbose_name="Название", help_text="введите название рассылки"
    )
    description = models.TextField(
        **NULLABLE,
        verbose_name="Описание",
        help_text="введите описание рассылки (необязательное поле)",
    )
    status = models.CharField(
        max_length=150,
        choices=STATUS_CHOICES,
        default=CREATED,
        verbose_name="Статус рассылки",
    )
    periodicity = models.CharField(
        max_length=150,
        choices=PERIODICITY_CHOICES,
        default=DAILY,
        verbose_name="Периодичность",
    )
    start_date = models.DateTimeField(
        verbose_name="Дата начала",
        **NULLABLE,
        help_text="(формат дд.мм.гггг) не обязательное поле",
    )
    end_date = models.DateTimeField(
        verbose_name="Дата окончания", **NULLABLE, help_text="не обязательное поле"
    )
    next_send_time = models.DateTimeField(
        verbose_name="Время следующей отправки",
        help_text="(формат дд.мм.гггг чч:мм:сс) обязательное поле",
        **NULLABLE,
    )
    clients = models.ManyToManyField(
        Client, related_name="mailing", verbose_name="Клиенты для рассылки"
    )
    message = models.ForeignKey(
        Message, verbose_name="Cообщение", on_delete=models.CASCADE, **NULLABLE
    )
    owner = models.ForeignKey(
        User, verbose_name="Владелец", on_delete=models.SET_NULL, **NULLABLE
    )

    def __str__(self):
        return f"{self.name}, статус: {self.status}"

    def save(self, *args, **kwargs):
        if not self.next_send_time:
            self.next_send_time = self.start_date
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ("name",)
        permissions = [
            ("deactivate_emailmessage", "Can deactivate mailing"),
            ("view_all_emailmessage", "Can view all mailings"),
        ]


class MailingLog(models.Model):
    """
    Модель для хранения информации о попытках рассылок
    """

    SUCCESS = "Успешно"
    FAIL = "Неуспешно"
    STATUS_VARIANTS = [
        (SUCCESS, "Успешно"),
        (FAIL, "Неуспешно"),
    ]

    time = models.DateTimeField(
        verbose_name="Дата и время попытки отправки", auto_now_add=True
    )
    status = models.CharField(
        max_length=50, choices=STATUS_VARIANTS, verbose_name="Cтатус рассылки"
    )
    server_response = models.CharField(
        max_length=150, verbose_name="Ответ сервера почтового сервиса", **NULLABLE
    )
    mailing = models.ForeignKey(
        Mailing, on_delete=models.CASCADE, verbose_name="Рассылка"
    )

    def __str__(self):
        return f"{self.mailing} {self.time} {self.status} {self.server_response}"

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылок"
