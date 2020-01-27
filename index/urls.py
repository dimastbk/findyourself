from django.urls import path

from .views import (
    IndexListPageView,
    IndexMapJsView,
    IndexMapPageView,
    IndexPageView,
    PlaceAllRouteDownloadView,
    PlaceCreateView,
    PlaceDetailView,
    PlaceEditView,
    RouteCreatePkView,
    RouteCreateView,
    RouteDownloadView,
    RouteEditView,
)

app_name = 'index'

urlpatterns = [
    path('route/<int:pk>/get/<format>/', RouteDownloadView.as_view(), name='route_get'),
    path('route/<int:pk>/edit/', RouteEditView.as_view(), name='route_edit'),
    path('route/create/<int:pk>/', RouteCreatePkView.as_view(), name='route_create_pk'),
    path('route/create/', RouteCreateView.as_view(), name='route_create'),
    path(
        'place/<int:pk>/allroute/<format>/',
        PlaceAllRouteDownloadView.as_view(),
        name='place_allroute_get',
    ),
    path('place/<int:pk>/edit/', PlaceEditView.as_view(), name='place_edit'),
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
