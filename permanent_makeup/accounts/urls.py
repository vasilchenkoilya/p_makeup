from django.urls import path
from .views import MyLoginView, MyPasswordResetView, MyPasswordResetConfirmView , signup_view
from django.contrib.auth import views as auth_views

urlpatterns = [
path('login/', MyLoginView.as_view(), name='login'),
path('signup/', signup_view, name='signup'),
path('password_reset/', MyPasswordResetView.as_view(), name='password_reset'),
path('reset/<uidb64>/<token>/', MyPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),  
path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
