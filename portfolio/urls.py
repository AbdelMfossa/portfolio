from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('index.html', views.home, name='home_html'),
    path('projects.html', views.projects, name='projects'),
    path('blog.html', views.blog, name='blog'),
    path('events.html', views.events, name='events'),
    path('videos.html', views.videos, name='videos'),
]
