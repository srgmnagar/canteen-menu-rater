from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from menu.models import MenuItem
from django.contrib.auth.views import LogoutView

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('menu:home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def user_dashboard(request):
    selected_option = request.GET.get('option', '')
    funny_messages = {
        'snack': "Snack attack incoming! 🍪",
        'study': "Brain food coming right up! 🧠",
        'healthy': "Your body will thank you! 🥗",
        'dessert': "Sweet tooth satisfaction guaranteed! 🍰",
        'fancy': "Time to treat yourself! 🍾",
        'spicy': "Warning: May cause happy tears! 🌶️",
        'emotional': "We've all been there... 🍫",
        '': "Let's find something delicious! 🍽️"
    }
    funny_message = funny_messages.get(selected_option, funny_messages[''])
    
    # Get recommendations based on selected option
    recommendations = MenuItem.objects.all()  # This is a placeholder - you can add your own recommendation logic
    
    context = {
        'selected_option': selected_option,
        'funny_message': funny_message,
        'recommendations': recommendations
    }
    return render(request, 'user_dashboard.html', context)

class CustomLogoutView(LogoutView):
    http_method_names = ['get', 'post', 'head', 'options', 'trace']
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
