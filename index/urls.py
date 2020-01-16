from django.urls import path

from user.views import ActionUserPlaceView

from .views import (GetAllRoute, GetRoute, IndexMapJsView, IndexMapPageView,
                    IndexPageView, PlaceDetailView, RouteDetailView, IndexListPageView)

urlpatterns = [
    path('route/<int:pk>/<format>/', GetRoute.as_view(), name='getroute'),
    path('route/<int:pk>/', RouteDetailView.as_view(), name='route'),
    path('place/<int:pk>/<format>', GetAllRoute.as_view(), name='getallroute'),
    path('place/<int:pk>/<slug:action>/', ActionUserPlaceView.as_view(), name='action_user_place'),
    path('place/<int:pk>/', PlaceDetailView.as_view(), name='place'),
    path(
        'map/indexmap.js?type_place=<type_place>&district=<district>&region=<region>',
        IndexMapJsView.as_view(),
        name='indexmap_js',
    ),
    path('map/', IndexMapPageView.as_view(), name='indexmap'),
    path(
        'list/<type_place>/<district>/<region>/',
        IndexListPageView.as_view(),
        name='indexlist_param',
    ),
    path('list/', IndexListPageView.as_view(), name='indexlist'),
    path('', IndexPageView.as_view(), name='index'),
]
