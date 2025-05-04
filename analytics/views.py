from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Avg, Count
from .models import RatingAnalytics, UserActivity, PopularItem, Feedback
from menu.models import MenuItem
from django.contrib.auth import get_user_model

User = get_user_model()

def is_admin(user):
    return user.is_staff

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    # Handle feedback resolution
    if request.method == 'POST' and 'resolve_feedback' in request.POST:
        feedback_id = request.POST.get('resolve_feedback')
        try:
            feedback = Feedback.objects.get(id=feedback_id)
            feedback.is_resolved = True
            feedback.save()
        except Feedback.DoesNotExist:
            pass

    # Get recent ratings
    recent_ratings = RatingAnalytics.objects.all().order_by('-date')[:5]
    
    # Get popular items
    popular_items = PopularItem.objects.all().order_by('-view_count')[:5]
    
    # Get recent user activities
    recent_activities = UserActivity.objects.all().order_by('-timestamp')[:10]
    
    # Get recent feedback
    recent_feedback = Feedback.objects.filter(is_resolved=False).order_by('-timestamp')[:5]
    
    # Get all feedback for management
    all_feedback = Feedback.objects.all().order_by('-timestamp')
    
    # Get statistics
    total_users = User.objects.count()
    total_menu_items = MenuItem.objects.count()
    total_ratings = RatingAnalytics.objects.aggregate(total=Count('id'))['total']
    average_rating = RatingAnalytics.objects.aggregate(avg=Avg('average_rating'))['avg'] or 0

    # Top rated items (min 1 rating)
    top_rated_items = RatingAnalytics.objects.filter(total_ratings__gte=1).order_by('-average_rating')[:5]
    # Lowest rated items (min 1 rating)
    lowest_rated_items = RatingAnalytics.objects.filter(total_ratings__gte=1).order_by('average_rating')[:5]
    # Most active users
    most_active_users = UserActivity.objects.values('user__username').annotate(activity_count=Count('id')).order_by('-activity_count')[:5]

    context = {
        'recent_ratings': recent_ratings,
        'popular_items': popular_items,
        'recent_activities': recent_activities,
        'recent_feedback': recent_feedback,
        'all_feedback': all_feedback,
        'total_users': total_users,
        'total_menu_items': total_menu_items,
        'total_ratings': total_ratings,
        'average_rating': round(average_rating, 2),
        'top_rated_items': top_rated_items,
        'lowest_rated_items': lowest_rated_items,
        'most_active_users': most_active_users,
    }
    
    return render(request, 'analytics/admin_dashboard.html', context)
