import secrets
import string
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from users.forms import UserRegisterForm, UserProfileForm
from users.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse


# Create your views here.


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        verification_link = f"{settings.SITE_URL}{reverse('users:verify', args=[user.pk, user.verification_token])}"

        send_mail(
            'Подтверждение регистрации',
            f'Для подтверждения регистрации перейдите по ссылке: {verification_link}',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False, )
        return super().form_valid(form)


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


def verify_email(request, user_id, token):
    user = get_object_or_404(User, pk=user_id, verification_token=token)
    user.is_active = True
    user.save()
    return redirect('users:login')


def logout(request):
    return redirect('users:login')


def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            new_password = generate_random_password()
            user.password = make_password(new_password)
            user.save()
            send_mail(
                'Password Reset',
                f'Ваш новый пароль: {new_password}',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False, )
            return redirect('users:login')
        except User.DoesNotExist:
            error_message = 'Пользователь с таким адресом электронной почты не существует.'
    else:
        error_message = ''

    return render(request, 'users/reset_password.html', {'error_message': error_message})


def generate_random_password(length=12, include_special_chars=True):
    characters = string.ascii_letters + string.digits
    if include_special_chars:
        characters += string.punctuation

    password = ''.join(secrets.choice(characters) for i in range(length))
    return password


from django.shortcuts import render

# Create your views here.
