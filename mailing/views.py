from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    CreateView,
    DeleteView,
    UpdateView,
)

from blog.services import get_blog_from_cache
from mailing.forms import ClientsForm, MessageForm, MailingForm, ManagerMailingForm
from mailing.models import Client, Mailing, Message, MailingLog


class HomeView(TemplateView):
    """
    Контроллер просмотра главной страницы
    """

    template_name = "mailing/index.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        mailing = Mailing.objects.all()
        client = Client.objects.all()
        context_data["all_email_massages"] = mailing.count()
        context_data["active_email_messages"] = mailing.filter(
            status=Mailing.STARTED
        ).count()
        context_data["unique_client"] = client.values("email").distinct().count()
        context_data["random_blogs"] = get_blog_from_cache().order_by("?")[:3]
        return context_data


class ClientListView(LoginRequiredMixin, ListView):
    """
    Контроллер отображения списка клиентов
    """

    model = Client
    template_name = "mailing/clients_list.html"

    def get_queryset(self, queryset=None):
        queryset = super().get_queryset()
        user = self.request.user
        if not user.is_superuser and not user.groups.filter(name="manager"):
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class ClientDetailView(LoginRequiredMixin, DetailView):
    """
    Контроллер отображения информации о клиенте
    """

    model = Client

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner or self.request.user.is_superuser:
            return self.object
        raise PermissionDenied


class ClientCreateView(LoginRequiredMixin, CreateView):
    """
    Контроллер создания клиента
    """

    model = Client
    form_class = ClientsForm
    template_name = "mailing/client_form.html"
    success_url = reverse_lazy("mailing:clients_list")

    def form_valid(self, form):
        client = form.save()
        user = self.request.user
        client.owner = user
        client.save()
        return super().form_valid(form)


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    """
    Контроллер удаления клиента
    """

    model = Client
    success_url = reverse_lazy("mailing:clients_list")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner or self.request.user.is_superuser:
            return self.object
        raise PermissionDenied


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    """
    Контроллер обновления информации о клиенте
    """

    model = Client
    form_class = ClientsForm
    template_name = "mailing/client_form.html"

    def get_success_url(self):
        return reverse("mailing:client_detail", args=[self.kwargs.get("pk")])

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner or self.request.user.is_superuser:
            return self.object
        raise PermissionDenied


class MessageListView(LoginRequiredMixin, ListView):
    """
    Контроллер просмотра списка сообщений
    """

    model = Message
    template_name = "mailing/message_list.html"


class MessageCreateView(LoginRequiredMixin, CreateView):
    """
    Контроллер создания сообщений
    """

    model = Message
    form_class = MessageForm
    template_name = "mailing/message_form.html"
    success_url = reverse_lazy("mailing:message_list")

    def form_valid(self, form):
        client = form.save()
        user = self.request.user
        client.owner = user
        client.save()
        return super().form_valid(form)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    """
    Контроллер удаления сообщений
    """

    model = Message
    template_name = "mailing/message_confirm_delete.html"
    success_url = reverse_lazy("mailing:message_list")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner or self.request.user.is_superuser:
            return self.object
        raise PermissionDenied


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    """
    Контроллер обновления сообщений
    """

    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:message_list")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner or self.request.user.is_superuser:
            return self.object
        raise PermissionDenied


class MessageDetailView(LoginRequiredMixin, DetailView):
    """
    Контроллер просмотра сообщения
    """

    model = Message
    template_name = "mailing/message_detail.html"

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner or self.request.user.is_superuser:
            return self.object
        raise PermissionDenied


class MailingListView(LoginRequiredMixin, ListView):
    """
    Контроллер  просмотра списка рассылок
    """

    model = Mailing
    template_name = "mailing/mailing_list.html"

    def get_queryset(self, queryset=None):
        queryset = super().get_queryset()
        user = self.request.user
        if not user.is_superuser and not user.groups.filter(name="manager"):
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class MailingCreateView(LoginRequiredMixin, CreateView):
    """
    Контроллер  создания рассылки
    """

    model = Mailing
    form_class = MailingForm
    template_name = "mailing/mailing_form.html"
    success_url = reverse_lazy("mailing:mailing_list")

    def form_valid(self, form):
        mailing = form.save()
        user = self.request.user
        mailing.owner = user
        mailing.save()
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    """
    Контроллер  обновления рассылки
    """

    model = Mailing
    form_class = MailingForm
    template_name = "mailing/mailing_form.html"

    def get_success_url(self):
        return reverse("mailing:mailing_detail", args=[self.kwargs.get("pk")])

    def get_form_class(self):
        """
        Функция, определяющая поля для редактирования в зависимости от прав пользователя
        """
        user = self.request.user
        if user == self.object.owner or user.is_superuser:
            return MailingForm
        elif user.has_perm("mailing.deactivate_mailing"):
            return ManagerMailingForm
        else:
            raise PermissionDenied


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    """
    Контроллер  удаления рассылки
    """

    model = Mailing
    template_name = "mailing/mailing_confirm_delete.html"
    success_url = reverse_lazy("mailing:mailing_list")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner or self.request.user.is_superuser:
            return self.object
        raise PermissionDenied


class MailingDetailView(LoginRequiredMixin, DetailView):
    """
    Контроллер  просмотра рассылки
    """

    model = Mailing
    template_name = "mailing/mailing_detail.html"

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if (
            not user.is_superuser
            and not user.groups.filter(name="manager")
            and user != self.object.owner
        ):
            raise PermissionDenied
        else:
            return self.object


class MailingLogView(ListView):
    """
    Контроллер отображения списка попыток рассылок
    """

    model = MailingLog
    template_name = "mailing/mailing_log_list.html"
