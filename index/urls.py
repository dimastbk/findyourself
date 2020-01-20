from django.urls import path

from user.views import ActionUserPlaceView

from .views import (GetAllRoute, GetRoute, IndexListPageView, IndexMapJsView,
                    IndexMapPageView, IndexPageView, PlaceCreateView,
                    PlaceDetailView, PlaceEditView)

urlpatterns = [
    path('route/<int:pk>/<format>/', GetRoute.as_view(), name='getroute'),
    path('place/<int:pk>/allroure/<format>/', GetAllRoute.as_view(), name='getallroute'),
    path('place/<int:pk>/edit/', PlaceEditView.as_view(), name='place_edit'),
    path('place/<int:pk>/<slug:action>/', ActionUserPlaceView.as_view(), name='action_user_place'),
    path('place/<int:pk>/', PlaceDetailView.as_view(), name='place'),
    path('place/create/', PlaceCreateView.as_view(), name='place_create'),
    path(
        'map/indexmap.js?type_place=<type_place>&district=<district>&region=<region>',
        IndexMapJsView.as_view(),
        name='indexmap_js',
    ),
    path('map/', IndexMapPageView.as_view(), name='indexmap'),
    path('list/', IndexListPageView.as_view(), name='indexlist'),
    path('', IndexPageView.as_view(), name='index'),
]
