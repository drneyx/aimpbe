from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at',)
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(District)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'created_at',)
    search_fields = ('name',)
    list_filter = ('name',)
