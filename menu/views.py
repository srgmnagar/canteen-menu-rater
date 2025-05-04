from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg
from .models import Category, MenuItem
from django.contrib.auth.decorators import login_required
import random

def home(request):
    categories = Category.objects.all()
    top_rated_items = MenuItem.objects.annotate(
        average_rating=Avg('ratings__rating')
    ).order_by('-average_rating')[:6]
    
    context = {
        'categories': categories,
        'top_rated_items': top_rated_items,
    }
    return render(request, 'home.html', context)

def menu_list(request):
    categories = Category.objects.all()
    menu_items = MenuItem.objects.all()
    
    # Filter by category if specified
    category_id = request.GET.get('category')
    if category_id:
        menu_items = menu_items.filter(category_id=category_id)
    
    # Sort items
    sort_by = request.GET.get('sort', 'name')
    if sort_by == 'rating':
        menu_items = menu_items.annotate(
            average_rating=Avg('ratings__rating')
        ).order_by('-average_rating')
    elif sort_by == 'price':
        menu_items = menu_items.order_by('price')
    else:  # default sort by name
        menu_items = menu_items.order_by('name')
    
    context = {
        'categories': categories,
        'menu_items': menu_items,
        'selected_category': category_id,
    }
    return render(request, 'menu_list.html', context)

def menu_item_detail(request, item_id):
    menu_item = get_object_or_404(MenuItem, id=item_id)
    context = {
        'menu_item': menu_item,
    }
    return render(request, 'menu_item_detail.html', context)

@login_required
def user_dashboard(request):
    if request.user.is_superuser:
        return redirect('/admin/')
    menu_items = MenuItem.objects.all()
    categories = Category.objects.all()
    selected_option = request.GET.get('option')
    funny_messages = {
        'snack': "Here's something to munch on while you procrastinate!",
        'study': "Fuel up for your all-nighter or that boring lecture!",
        'healthy': "Look at you making healthy choices! (No, fried rice doesn't count)",
        'dessert': "Because life is short, eat dessert first!",
        'fancy': "Feeling fancy? Pinkies up!",
        'spicy': "Spice up your life (and your taste buds)!",
        'emotional': "Eat your feelings, we won't judge.",
        'broke': "Month end? Here's what you can afford with pocket change!",
        'surprise': "Surprise! You never know what you'll get!",
        'study_boring': "Fuel up for your all-nighter or that boring lecture!",
    }
    if selected_option == 'snack':
        recommendations = menu_items.filter(name__icontains='samosa') | \
                         menu_items.filter(name__icontains='vada') | \
                         menu_items.filter(name__icontains='sandwich') | \
                         menu_items.filter(name__icontains='pav') | \
                         menu_items.filter(name__icontains='roll')
        recommendations = recommendations.distinct()[:3]
        message = funny_messages['snack']
    elif selected_option == 'study' or selected_option == 'study_boring':
        recommendations = menu_items.filter(name__icontains='coffee') | \
                         menu_items.filter(name__icontains='tea') | \
                         menu_items.filter(name__icontains='energy') | \
                         menu_items.filter(name__icontains='chai')
        recommendations = recommendations.distinct()[:3]
        message = funny_messages['study_boring']
    elif selected_option == 'healthy':
        recommendations = menu_items.filter(name__icontains='salad') | \
                         menu_items.filter(name__icontains='fruit') | \
                         menu_items.filter(name__icontains='sprout') | \
                         menu_items.filter(name__icontains='juice')
        recommendations = recommendations.distinct()[:3]
        message = funny_messages['healthy']
    elif selected_option == 'dessert':
        recommendations = menu_items.filter(name__icontains='ice cream') | \
                         menu_items.filter(name__icontains='cake') | \
                         menu_items.filter(name__icontains='gulab') | \
                         menu_items.filter(name__icontains='sweet') | \
                         menu_items.filter(name__icontains='dessert')
        recommendations = recommendations.distinct()[:3]
        message = funny_messages['dessert']
    elif selected_option == 'fancy':
        recommendations = menu_items.filter(name__icontains='paneer') | \
                         menu_items.filter(name__icontains='biryani') | \
                         menu_items.filter(name__icontains='special')
        recommendations = recommendations.distinct()[:3]
        message = funny_messages['fancy']
    elif selected_option == 'spicy':
        recommendations = menu_items.filter(name__icontains='spicy') | \
                         menu_items.filter(name__icontains='masala') | \
                         menu_items.filter(name__icontains='mirchi')
        recommendations = recommendations.distinct()[:3]
        message = funny_messages['spicy']
    elif selected_option == 'emotional':
        recommendations = menu_items.filter(name__icontains='chocolate') | \
                         menu_items.filter(name__icontains='ice cream') | \
                         menu_items.filter(name__icontains='cake')
        recommendations = recommendations.distinct()[:3]
        message = funny_messages['emotional']
    elif selected_option == 'broke':
        recommendations = menu_items.order_by('price')[:3]
        message = funny_messages['broke']
    else:
        recommendations = menu_items.order_by('?')[:3]
        message = funny_messages['surprise']
    # Fallback if no recommendations found
    if not recommendations:
        recommendations = menu_items.order_by('?')[:3]
        message = "We couldn't find anything for that, so here's something random!"
    context = {
        'recommendations': recommendations,
        'categories': categories,
        'selected_option': selected_option,
        'funny_message': message,
    }
    return render(request, 'user_dashboard.html', context)
