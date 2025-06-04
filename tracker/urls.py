from django.contrib import admin
from django.urls import path
from tracker.views import login_view, register_view, logout_view, food_tracker

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('tracker/', food_tracker, name='food_tracker'),
]