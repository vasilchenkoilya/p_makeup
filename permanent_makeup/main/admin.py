from django.contrib import admin
from . import models


@admin.register(models.WorkGalllery)
class WorkGallleryAdmin(admin.ModelAdmin):
    list_display = ('image', 'title', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title','created_at')


@admin.register(models.Service)   
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price')
    list_filter = ('name', 'price')
    search_fields = ('name', 'price')
    readonly_fields = ('customers',)