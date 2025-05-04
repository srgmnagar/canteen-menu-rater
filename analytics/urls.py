from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
] 