from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Food
from .forms import FoodForm, SignUpForm, LoginForm
from django.db.models import Sum
from django.utils import timezone

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('food_tracker')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('food_tracker')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def food_tracker(request):
    today = timezone.now().date()
    
    if request.method == 'POST':
        if 'delete' in request.POST:
            food_id = request.POST.get('delete')
            Food.objects.filter(id=food_id, user=request.user).delete()
            return redirect('food_tracker')
            
        form = FoodForm(request.POST)
        if form.is_valid():
            food = form.save(commit=False)
            food.user = request.user
            food.save()
            return redirect('food_tracker')
    else:
        form = FoodForm()

    foods = Food.objects.filter(user=request.user, date_created__date=today).order_by('-date_created')
    total_calories = foods.aggregate(Sum('calories'))['calories__sum'] or 0
    
    return render(request, 'food_tracker.html', {
        'form': form,
        'foods': foods,
        'total_calories': total_calories,
        'today': today
    })