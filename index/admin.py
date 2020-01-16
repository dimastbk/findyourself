from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

from .models import City, District, Place, Region, Route, Type


@admin.register(Place)
class PlaceAdmin(LeafletGeoAdmin):
    list_display = ('title', 'type_place', 'city', 'region', 'is_published')
    actions = ['make_published']

    def make_published(self, request, queryset):
        queryset.update(is_published=True)

    def demake_published(self, request, queryset):
        queryset.update(is_published=False)

    make_published.short_description = 'Опубликовать'
    demake_published.short_description = 'В черновики'


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'title_pl', 'icon')


@admin.register(City)
class CityAdmin(LeafletGeoAdmin):
    list_display = ('title', 'ae1', 'ae2', 'wd_id')


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('title', 'capital', 'region', 'wd_id')


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('title', 'capital', 'wd_id')


@admin.register(Route)
class RouteAdmin(LeafletGeoAdmin):
    list_display = ('rt_from', 'rt_to', 'rt_title', 'rt_length')
