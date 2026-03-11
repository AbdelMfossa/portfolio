from django.shortcuts import get_object_or_404, redirect
from .models import ShortLink
from django.http import Http404

def redirect_short_link(request, short_code):
    link = get_object_or_404(ShortLink, short_code=short_code)
    
    if not link.is_active:
        raise Http404("Ce lien n'est plus actif.")
        
    # Incrémenter le compteur de clics
    link.increment_clicks()
    
    # Rediriger vers l'URL cible
    return redirect(link.target_url)
