import os
from django.contrib import admin
from django.urls import path, include

from django.http import Http404

# On récupère l'URL secrète depuis le .env, avec 'admin/' comme fallback de sécurité
ADMIN_URL = os.getenv('ADMIN_URL', 'admin/')

def admin_honeypot(request):
    """Leurre pour les robots cherchant l'URL admin par défaut"""
    raise Http404()

from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    # Si ADMIN_URL est différent du classique 'admin/', on bloque le chemin classique
    path('admin/', admin_honeypot) if ADMIN_URL != 'admin/' else path('__placeholder__/', admin_honeypot),
    path(f'{ADMIN_URL}', admin.site.urls),
    path('rosetta/', include('rosetta.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path('', include('portfolio.urls')),
    path('', include('shortener.urls')),
    prefix_default_language=False
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
