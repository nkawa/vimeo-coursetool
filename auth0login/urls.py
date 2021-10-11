from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('dashboard', views.dashboard),
    path('dashboard.html', views.dashboard),
    path('settings.html', views.user_settings),
    path('usages.html', views.usages),
    path('videos.html', views.videos),
    path('register.html', views.register),
    path('privacy', views.privacy),
    path('terms', views.terms),
    path('privacy.html', views.privacy),
    path('terms.html', views.terms),
    path('logout', views.logout),
    path('logout/', views.logout),
    path('', include('django.contrib.auth.urls')),
    path('', include('social_django.urls')),
]
