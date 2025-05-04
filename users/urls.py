from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('dashboard/', views.user_dashboard, name='dashboard'),
] 