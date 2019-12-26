from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

from .models import City, District, Place, Region, Route, Type


@admin.register(Place)
class PlaceAdmin(LeafletGeoAdmin):
    list_display = ('title', 'type_place', 'city', 'region', 'is_published')


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    pass


@admin.register(City)
class TagAdmin(LeafletGeoAdmin):
    pass


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    pass


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    pass


@admin.register(Route)
class RouteAdmin(LeafletGeoAdmin):
    list_display = ('rt_from', 'rt_to', 'rt_title', 'rt_length')
