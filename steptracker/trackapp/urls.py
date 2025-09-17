from django.contrib import admin
from django.urls import path
from trackapp.views import register_view, login_view, logout_view, steps_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', steps_view, name='steps'),  # homepage
]
