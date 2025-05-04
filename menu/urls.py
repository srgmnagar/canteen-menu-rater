from django.urls import path
from . import views
from . import api

app_name = 'menu'

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu_list, name='menu_list'),
    path('menu/<int:item_id>/', views.menu_item_detail, name='menu_item_detail'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('api/rate-item/', api.rate_item, name='rate_item'),
] 