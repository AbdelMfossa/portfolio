from django.shortcuts import render
from .models import Tag, Project, Article, Event, Video, Certification, Skill, Experience

def home(request):
    projects = Project.objects.filter(status='production', is_active=True)[:2]
    articles = Article.objects.filter(is_active=True)[:3]
    recent_videos = Video.objects.filter(is_active=True)[:3]
    events = Event.objects.filter(is_active=True)[:3]
    certifications = Certification.objects.filter(is_active=True)
    skills = Skill.objects.filter(is_active=True)
    experiences = Experience.objects.all()
    
    return render(request, 'portfolio/index.html', {
        'projects': projects,
        'articles': articles,
        'videos': recent_videos,
        'events': events,
        'certifications': certifications,
        'skills': skills,
        'experiences': experiences,
    })

def projects(request):
    projects_list = Project.objects.filter(is_active=True)
    tags = Tag.objects.filter(projects__is_active=True).distinct()
    return render(request, 'portfolio/projects.html', {
        'projects': projects_list,
        'tags': tags
    })

def blog(request):
    articles_list = Article.objects.filter(is_active=True)
    return render(request, 'portfolio/blog.html', {'articles': articles_list})

def events(request):
    events_list = Event.objects.filter(is_active=True)
    return render(request, 'portfolio/events.html', {'events': events_list})

def videos(request):
    featured_video = Video.objects.filter(is_featured=True, is_active=True).first()
    
    if featured_video:
        videos_list = Video.objects.filter(is_active=True).exclude(id=featured_video.id)
    else:
        videos_list = Video.objects.filter(is_active=True)
        featured_video = videos_list.first() if videos_list.exists() else None
        if featured_video:
            videos_list = videos_list.exclude(id=featured_video.id)
            
    return render(request, 'portfolio/videos.html', {
        'featured_video': featured_video,
        'videos': videos_list
    })

def contact(request):
    return render(request, 'portfolio/contact.html')

def trigger_error(request):
    """Fonction temporaire pour simuler une erreur 500"""
    raise Exception("Simulated Server Error")
