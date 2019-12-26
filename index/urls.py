from django.urls import path

from .views import (GetAllRoute, GetRoute, IndexMapJsView, IndexMapPageView,
                    IndexPageView, PlaceDetailView, RouteDetailView)

urlpatterns = [
    path('route/<int:pk>/<format>', GetRoute.as_view(), name='getroute'),
    path('route/<int:pk>', RouteDetailView.as_view(), name='route'),
    path('place/<int:pk>/<format>', GetAllRoute.as_view(), name='getallroute'),
    path('place/<int:pk>', PlaceDetailView.as_view(), name='place'),
    path(
        'map/indexmap.js?type_place=<type_place>&district=<district>&region=<region>',
        IndexMapJsView.as_view(),
        name='indexmap_js',
    ),
    path('map', IndexMapPageView.as_view(), name='indexmap'),
    path('', IndexPageView.as_view(), name='index'),
]
