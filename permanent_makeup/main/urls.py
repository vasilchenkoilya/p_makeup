from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('gallery/', views.gallery_view, name='gallery'),
    path('service/<slug:service_slug>/', views.service_detail, name='service_detail'),
]