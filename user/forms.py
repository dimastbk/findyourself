from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput
from django.utils.translation import gettext_lazy as _

from index.mixin import CssClassFormMixin

from .models import Profile


class LoginForm(CssClassFormMixin, AuthenticationForm):
    pass


class RegistrationForm(CssClassFormMixin, forms.ModelForm):

    password1 = forms.CharField(
        label='Пароль',
        max_length=30,
        min_length=8,
        widget=PasswordInput(),
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        max_length=30,
        min_length=8,
        widget=PasswordInput(),
    )

    password_mismatch = 'Пароли не совпадают.'

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.password_mismatch,
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserForm(CssClassFormMixin, forms.ModelForm):

    def clean_username(self):
        user_id = self.instance.id
        username = self.cleaned_data['username']
        user = User.objects.filter(pk=user_id).exclude(username=username).exists()
        if user:
            raise forms.ValidationError(_('A user with that username already exists.'))
        return username

    class Meta:
        model = User
        fields = ('username', 'first_name')


class ProfileForm(CssClassFormMixin, forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('image', 'bio', 'city', 'instagram')


class CustomPasswordChangeForm(CssClassFormMixin, PasswordChangeForm):

    old_password = forms.CharField(
        label=_('Old password'),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password',
            'autofocus': True,
        }),
    )
    new_password1 = forms.CharField(
        label=_('New password'),
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
        }),
        strip=False,
    )
    new_password2 = forms.CharField(
        label=_('New password confirmation'),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
        }),
    )
