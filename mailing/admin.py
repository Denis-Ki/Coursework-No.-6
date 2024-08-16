from django.contrib import admin

from mailing.models import Client, Message, Mailing


# Register your models here.


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "comments", "owner")
    search_fields = ("name", "email")
    list_filter = ("name", "email", "owner")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "subject", "message", "owner")
    list_filter = ("owner",)
    search_fields = ("subject", "message")


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "status",
        "periodicity",
        "start_date",
        "end_date",
        "next_send_time",
        "message",
        "owner",
    )
    list_filter = (
        "periodicity",
        "status",
        "start_date",
        "end_date",
        "clients",
        "message",
        "owner",
    )
    search_fields = ("name", "description", "clients__name", "message__subject")
