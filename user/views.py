from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView

from index.models import Place

from .forms import (CustomPasswordChangeForm, LoginForm, ProfileForm,
                    RegistrationForm, UserForm)
from .models import Profile


class ProfileView(DetailView):
    """Отображение профиля любого пользователя."""

    model = User
    template_name = 'user/profile.html'

    def title_page(self):
        return 'Профиль участника {0}'.format(self.get_object().username)


class CurrentProfileView(LoginRequiredMixin, ProfileView):
    """Показ профиля текущего пользователя по ссылке вида user/profile."""

    title_page = 'Мой профиль'

    def get_object(self):
        return self.get_queryset().get(pk=self.request.user.id)


class LogoutView(LoginRequiredMixin, RedirectView):
    """Класс для выхода с сайта."""

    url = '/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class CustomLoginView(SuccessMessageMixin, LoginView):
    """Кастомный класс для логина, наследуется от стандартного.

    Добавляются успешные сообщения и оформление форм из бутстрапа (может вынести в миксин?)

    """

    title_page = 'Вход на сайт'
    template_name = 'user/login.html'
    form_class = LoginForm
    success_message = 'Вы успешно вошли на сайт.'


class RegistrationView(SuccessMessageMixin, FormView):

    title_page = 'Регистрация'
    form_class = RegistrationForm
    template_name = 'user/registration.html'
    success_message = 'Вы успешно зарегистрировались, используйте логин и пароль для входа на сайт.'
    success_url = reverse_lazy('user:edit_profile')

    @method_decorator(sensitive_post_parameters('password1', 'password2'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)

        return super().form_valid(form)


class CustomPasswordChangeView(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    """Кастомный класс для смены пароля, наследуется от стандартного.

    Добавляются успешные сообщения и оформление форм из бутстрапа (может вынести в миксин?)

    """

    title_page = 'Изменить пароль'
    template_name = 'user/password_change_form.html'
    form_class = CustomPasswordChangeForm
    success_message = 'Пароль успешно изменён.'
    success_url = reverse_lazy('user:current_profile')


class ProfileEditView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Класс для редактирования профиля, состоящего из двух форм.

    В конце вызывается form_valid для добавления успешных сообщений и редиректа в профиль.
    В оригинале там render_on_response.

    """

    title_page = 'Редактировать профиль'
    model = User
    form_class = UserForm
    form_class2 = ProfileForm
    template_name = 'user/edit_profile.html'
    success_message = 'Профиль успешно сохранён.'
    success_url = reverse_lazy('user:current_profile')

    def get_object(self):
        return User.objects.get(pk=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object = self.get_object()
        context['form'] = self.form_class(instance=self.object)
        context['form2'] = self.form_class2(instance=self.object.profile)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=self.object)
        form2 = self.form_class2(request.POST, instance=self.object.profile)

        if form.is_valid() and form2.is_valid():
            user = form.save()
            profile = form2.save(commit=False)
            profile.user = user
            profile.save()

        return self.form_valid(form)


class ActionUserPlaceView(LoginRequiredMixin, RedirectView):

    url = '/'

    def get(self, request, *args, **kwargs):
        place = Place.objects.get(pk=kwargs.get('pk'))
        action = kwargs.get('action')
        if place and action:
            profile = Profile.objects.get(pk=request.user.id)
            if action == 'like':
                profile.like_place.add(place)
            elif action == 'unlike':
                profile.like_place.remove(place)
            elif action == 'done':
                profile.done_place.add(place)
            elif action == 'undone':
                profile.done_place.remove(place)
            elif action == 'want':
                profile.want_place.add(place)
            elif action == 'unwant':
                profile.want_place.remove(place)

        self.url = place.get_absolute_url()

        return super().get(request, *args, **kwargs)
