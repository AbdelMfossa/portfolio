from django.shortcuts import render

def home(request):
    return render(request, 'portfolio/index.html')

def projects(request):
    return render(request, 'portfolio/projects.html')

def blog(request):
    return render(request, 'portfolio/blog.html')

def events(request):
    return render(request, 'portfolio/events.html')

def videos(request):
    return render(request, 'portfolio/videos.html')
