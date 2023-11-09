from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('gallery/', views.gallery_view, name='gallery'),
    path('service/<slug:service_slug>/', views.service_detail, name='service_detail'),
    path('reviews/', views.reviews_page, name='reviews_page'),
    path('reservation/', views.reservation_view, name='reservation'),
    path('reservation/reservation_success/', views.reservation_success, name='reservation_success'),
]