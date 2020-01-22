from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView

from index.models import Place

from .forms import CustomPasswordChangeForm, LoginForm, ProfileForm, RegistrationForm, UserForm


class ProfileView(DetailView):
    """Отображение профиля любого пользователя."""

    model = User
    template_name = 'user/user_detail.html'

    def title_page(self):
        return 'Профиль участника {0}'.format(self.get_object().username)


class CurrentProfileView(LoginRequiredMixin, ProfileView):
    """Показ профиля текущего пользователя по ссылке вида user/profile."""

    title_page = 'Мой профиль'

    def get_object(self):
        return self.get_queryset().get(pk=self.request.user.id)


class UserFavorPlaceView(DetailView):

    model = User
    template_name = 'user/user_favor_place.html'
    type_dict = {
        'likes': 'Избранное участника',
        'dones': 'Посещённое участником',
        'wants': 'Хотелки участника',
    }

    def get(self, request, *args, **kwargs):
        self.type_list = kwargs.get('type_list')
        if self.type_list not in self.type_dict:
            return HttpResponse('Bad request.', status=400)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_object = self.get_object().profile
        if self.type_list == 'likes':
            context['place_list'] = profile_object.like_place.order_by('title').all()
        elif self.type_list == 'dones':
            context['place_list'] = profile_object.done_place.order_by('title').all()
        elif self.type_list == 'wants':
            context['place_list'] = profile_object.want_place.order_by('title').all()

        return context

    def title_page(self):
        return f'{self.type_dict[self.type_list]} @{self.get_object().username}'


class CurrentUserFavorPlaceView(LoginRequiredMixin, UserFavorPlaceView):

    type_dict = {
        'likes': 'Моё избранное',
        'dones': 'Мои посещения',
        'wants': 'Мои хотелки',
    }

    def get_object(self):
        return self.get_queryset().get(pk=self.request.user.id)

    def title_page(self):
        return self.type_dict[self.type_list]


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
        if not context.get('form'):
            context['form'] = self.form_class(instance=self.object)
        if not context.get('form2'):
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

        return self.render_to_response(self.get_context_data(form=form, form2=form2))


class ActionUserPlaceView(LoginRequiredMixin, RedirectView):

    url = '/'
    action_dict = {
        'like': 'добавлено в избранное.',
        'unlike': 'удалено из избранного.',
        'done': 'отмечено посещённым.',
        'undone': 'отмечено непосещённым.',
        'want': 'добавлено в хотелки.',
        'unwant': 'убрано из хотелок.',
    }

    def get(self, request, *args, **kwargs):
        place = Place.objects.get(pk=kwargs.get('pk'))
        action = kwargs.get('action')
        if place and action and action in self.action_dict:
            profile = User.objects.get(pk=request.user.id).profile
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

            messages.success(
                request,
                'Место «{0} {1}» {2}'.format(
                    place.type_place.title.lower(), place.title, self.action_dict[action],
                ),
            )

        if request.GET.get('next'):
            url = request.GET.get('next')
        else:
            url = place.get_absolute_url()

        if url_has_allowed_host_and_scheme(url, request.site.domain):
            self.url = url

        return super().get(request, *args, **kwargs)
