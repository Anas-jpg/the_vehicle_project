from django.contrib import admin
from .models import Brand, Car


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('page_id', 'page_name', 'url', 'created_at', 'updated_at')
    search_fields = ('page_id', 'page_name')
    ordering = ['created_at']


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('name', 'model', 'year', 'brand', 'created_at', 'updated_at')
    search_fields = ('name', 'model', 'brand__page_name')
    list_filter = ('brand', 'year')
