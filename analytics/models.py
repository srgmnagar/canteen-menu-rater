from django.db import models
from django.contrib.auth import get_user_model
from menu.models import MenuItem

User = get_user_model()

class RatingAnalytics(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    average_rating = models.FloatField(default=0.0)
    total_ratings = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Rating Analytics"
        ordering = ['-date']

class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=100)  # e.g., 'rated_item', 'added_review'
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "User Activities"
        ordering = ['-timestamp']

class PopularItem(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    view_count = models.IntegerField(default=0)
    rating_count = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Popular Items"
        ordering = ['-view_count']

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Feedback"
        ordering = ['-timestamp']
