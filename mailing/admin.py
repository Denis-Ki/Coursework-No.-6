from django.contrib import admin

from mailing.models import Client, Message


# Register your models here.

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'comments', 'owner')
    search_fields = ('name', 'email')
    list_filter = ('name', 'email', 'owner')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'message', 'owner')
    list_filter = ('owner',)
    search_fields = ('subject', 'message')