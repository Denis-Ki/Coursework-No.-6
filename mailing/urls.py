from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import HomeView

# from django.views.decorators.cache import cache_page

app_name = MailingConfig.name

urlpatterns = [
    path("", HomeView.as_view(), name="index")
]
