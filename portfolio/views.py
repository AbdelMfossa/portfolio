from django.shortcuts import render
from .models import Project, Article, Event, Video

def home(request):
    projects = Project.objects.filter(status='production')[:2]
    articles = Article.objects.all()[:3]
    recent_videos = Video.objects.all()[:3]
    events = Event.objects.all()[:3]
    
    return render(request, 'portfolio/index.html', {
        'projects': projects,
        'articles': articles,
        'videos': recent_videos,
        'events': events,
    })

def projects(request):
    projects_list = Project.objects.all()
    return render(request, 'portfolio/projects.html', {'projects': projects_list})

def blog(request):
    articles_list = Article.objects.all()
    return render(request, 'portfolio/blog.html', {'articles': articles_list})

def events(request):
    events_list = Event.objects.all()
    return render(request, 'portfolio/events.html', {'events': events_list})

def videos(request):
    featured_video = Video.objects.filter(is_featured=True).first()
    
    if featured_video:
        videos_list = Video.objects.exclude(id=featured_video.id)
    else:
        videos_list = Video.objects.all()
        featured_video = videos_list.first() if videos_list.exists() else None
        if featured_video:
            videos_list = videos_list.exclude(id=featured_video.id)
            
    return render(request, 'portfolio/videos.html', {
        'featured_video': featured_video,
        'videos': videos_list
    })
