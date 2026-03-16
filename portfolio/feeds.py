from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import Article
from django.utils.translation import gettext_lazy as _

class LatestArticlesFeed(Feed):
    title = _("Abdel Aziz Mfossa - Articles & Tutoriels")
    link = "/blog/"
    description = _("Les derniers articles sur Google Workspace, l'automatisation et l'IA.")

    def items(self):
        return Article.objects.filter(is_active=True).order_by('-published_date')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.summary

    def item_link(self, item):
        return item.medium_url

    def item_pubdate(self, item):
        # Convert simple date to datetime for RSS compliance if possible, 
        # but Django handles DateField too.
        from datetime import datetime
        return datetime.combine(item.published_date, datetime.min.time())
