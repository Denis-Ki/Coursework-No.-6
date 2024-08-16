from django.urls import path
from django.views.decorators.cache import cache_page

from mailing.apps import MailingConfig
from mailing.views import (
    HomeView,
    ClientListView,
    ClientCreateView,
    ClientDetailView,
    ClientDeleteView,
    ClientUpdateView,
    MessageListView,
    MessageCreateView,
    MessageDeleteView,
    MessageUpdateView,
    MessageDetailView,
    MailingListView,
    MailingCreateView,
    MailingUpdateView,
    MailingDeleteView,
    MailingDetailView,
    MailingLogView,
)

# from django.views.decorators.cache import cache_page

app_name = MailingConfig.name

urlpatterns = [
    path("", HomeView.as_view(), name="index"),
    path("clients/", ClientListView.as_view(), name="clients_list"),
    path("client_create/", ClientCreateView.as_view(), name="client_create"),
    path(
        "client_detail/<int:pk>/",
        cache_page(60)(ClientDetailView.as_view()),
        name="client_detail",
    ),
    path("client_delete/<int:pk>/", ClientDeleteView.as_view(), name="client_delete"),
    path("client_update/<int:pk>/", ClientUpdateView.as_view(), name="client_update"),
    path("message_list/", MessageListView.as_view(), name="message_list"),
    path("message_create/", MessageCreateView.as_view(), name="message_create"),
    path(
        "message_delete/<int:pk>/", MessageDeleteView.as_view(), name="message_delete"
    ),
    path(
        "message_update/<int:pk>/", MessageUpdateView.as_view(), name="message_update"
    ),
    path(
        "message_detail/<int:pk>/",
        cache_page(60)(MessageDetailView.as_view()),
        name="message_detail",
    ),
    path("mailing_list/", MailingListView.as_view(), name="mailing_list"),
    path("mailing_create/", MailingCreateView.as_view(), name="mailing_create"),
    path(
        "mailing_update/<int:pk>/", MailingUpdateView.as_view(), name="mailing_update"
    ),
    path(
        "mailing_delete/<int:pk>/", MailingDeleteView.as_view(), name="mailing_delete"
    ),
    path(
        "mailing_detail/<int:pk>/",
        cache_page(60)(MailingDetailView.as_view()),
        name="mailing_detail",
    ),
    path("mailing_log_list/", MailingLogView.as_view(), name="mailing_log_list"),
]
