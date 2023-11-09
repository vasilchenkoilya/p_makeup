from django.contrib import admin
from django.core.exceptions import ValidationError
from . import models
from django import forms


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


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['service', 'author', 'created_at']
    list_filter = ['service', 'author', 'created_at']
    search_fields = ['text']


class TimeSlotAdminForm(forms.ModelForm):
    class Meta:
        model = models.TimeSlot
        fields = ['service', 'start_time', 'end_time', 'is_available']

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time and start_time >= end_time:
            raise ValidationError("End time must be after start time.")
        

@admin.register(models.TimeSlot)           
class TimeSlotAdmin(admin.ModelAdmin):
    form = TimeSlotAdminForm
