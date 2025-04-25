from django.contrib import admin
from .models import Category, MenuItem, Rating, Review, DailyMenu

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_available', 'average_rating')
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'menu_item', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'menu_item__name')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'menu_item', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'menu_item__name', 'content')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(DailyMenu)
class DailyMenuAdmin(admin.ModelAdmin):
    list_display = ('date', 'created_at')
    filter_horizontal = ('items',)
    readonly_fields = ('created_at', 'updated_at')
