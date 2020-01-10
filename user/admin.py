from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class PlaceAdmin(admin.ModelAdmin):
    pass
