from django.contrib.auth.views import (PasswordChangeDoneView,
                                       PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.urls import path

from .views import (CurrentProfileView, CustomLoginView,
                    CustomPasswordChangeView, LogoutView, ProfileEditView,
                    ProfileView, RegistrationView)

app_name = 'user'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('profile/<int:pk>', ProfileView.as_view(), name='profile'),
    path('profile/edit/', ProfileEditView.as_view(), name='edit_profile'),
    path('profile/', CurrentProfileView.as_view(), name='current_profile'),
    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
]
