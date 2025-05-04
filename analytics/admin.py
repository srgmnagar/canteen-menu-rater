from django.contrib import admin
from .models import RatingAnalytics, UserActivity, PopularItem, Feedback

@admin.register(RatingAnalytics)
class RatingAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('menu_item', 'average_rating', 'total_ratings', 'date')
    list_filter = ('date', 'menu_item')
    search_fields = ('menu_item__name',)

@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'menu_item', 'timestamp')
    list_filter = ('action', 'timestamp')
    search_fields = ('user__username', 'menu_item__name')

@admin.register(PopularItem)
class PopularItemAdmin(admin.ModelAdmin):
    list_display = ('menu_item', 'view_count', 'rating_count', 'date')
    list_filter = ('date',)
    search_fields = ('menu_item__name',)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'message', 'timestamp', 'is_resolved')
    list_filter = ('is_resolved', 'timestamp')
    search_fields = ('user__username', 'subject', 'message')
    list_per_page = 20
    ordering = ['-timestamp']
