from django.urls import path, include
from . import views
from django.conf import settings

#This is slow. So, you may check your server settings.
#if settings.DEBUG is False:
#    urlpatterns += patterns('',
#        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.STATIC_ROOT}),
#    )


urlpatterns = [
    path('', views.index),
    path('dashboard', views.dashboard),
    path('dashboard.html', views.dashboard),
    path('settings.html', views.user_settings),
    path('profile.html', views.profile),
    path('usages.html', views.usages),
    path('videos.html', views.videos),
    path('courses.html', views.courses),
    path('view_video.html', views.view_video),
    path('view_video', views.view_video),
    path('register.html', views.register),
    path('privacy', views.privacy),
    path('set_video', views.set_video),
    path('terms', views.terms),
    path('privacy.html', views.privacy),
    path('terms.html', views.terms),
    path('logout', views.logout),
    path('logout/', views.logout),
    path('', include('django.contrib.auth.urls')),
    path('', include('social_django.urls')),
]
