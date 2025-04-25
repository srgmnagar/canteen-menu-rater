from django.shortcuts import render, get_object_or_404
from django.db.models import Avg
from .models import Category, MenuItem

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
