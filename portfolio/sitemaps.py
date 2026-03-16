from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Project, Article, Event

class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'monthly'

    def items(self):
        return ['home', 'projects', 'blog', 'events', 'videos', 'contact']

    def location(self, item):
        return reverse(item)

class ProjectSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return Project.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return reverse('projects') # Actuellement les projets n'ont pas de page individuelle, on renvoie vers la grille

class ArticleSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Article.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.published_date
    
    def location(self, obj):
        return obj.medium_url # Redirection vers Medium car pas de page individuelle locale

class EventSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Event.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.date

    def location(self, obj):
        return reverse('events')
