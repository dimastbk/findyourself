from django.urls import path

from .views import (
    ActionUserPlaceView,
    CurrentProfileView,
    CurrentUserFavorPlaceView,
    CustomLoginView,
    CustomPasswordChangeView,
    LogoutView,
    ProfileEditView,
    ProfileView,
    RegistrationView,
    UserFavorPlaceView,
)

app_name = 'user'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path(
        '<int:pk>/place/<slug:type_list>/', UserFavorPlaceView.as_view(), name='user_favor_place',
    ),
    path(
        'place/<slug:type_list>/',
        CurrentUserFavorPlaceView.as_view(),
        name='current_user_favor_place',
    ),
    path('place/<int:pk>/<slug:action>/', ActionUserPlaceView.as_view(), name='action_user_place'),
    path('<int:pk>/profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', ProfileEditView.as_view(), name='edit_profile'),
    path('profile/', CurrentProfileView.as_view(), name='current_profile'),
    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
]
