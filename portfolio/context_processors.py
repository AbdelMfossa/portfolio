"""
Context processor qui injecte des statistiques de visiteurs globales
dans tous les templates (pour le footer badge et d'autres zones).

Métriques exposées :
- visitor_sessions    : nombre de sessions distinctes (= "visites" au sens analytics)
- visitor_page_views  : nombre de pages vues au total
- visitor_country_count : nombre de pays distincts

Les stats sont mises en cache en mémoire pendant 1 minute pour ne pas
faire de requêtes DB à chaque chargement de page, tout en restant fraîches.

📖 Note sur le comptage :
   Une "visite" (session) = toutes les pages vues par un même visiteur
   pendant une session continue. C'est ce que Google Analytics appelle
   une "session". Notre clé de session est basée sur IP+UserAgent hashé.
   1 visiteur qui parcourt 8 pages = 1 session (pas 8 visites).
"""
import time
import threading

_stats_cache = {'data': None, 'updated_at': 0}
_stats_lock = threading.Lock()

CACHE_TTL = 60  # 1 minute (réduit pour que le badge soit quasi temps-réel)


def _fetch_stats() -> dict:
    """Interroge la base de données pour calculer les stats globales."""
    try:
        from portfolio.models import VisitorLog
        from django.db.models import Count

        qs = VisitorLog.objects.exclude(device_type='bot')

        # Nombre de pays distincts (hors entrées locales de dev)
        country_count = (
            qs.exclude(country_code='')
              .exclude(country_code='XX')
              .values('country_code')
              .distinct()
              .count()
        )

        # Sessions distinctes = visiteurs uniques par clé de session
        # 1 visiteur qui visite 8 pages = 1 session (comme Google Analytics)
        session_count = qs.values('session_key').distinct().count()

        # Pages vues totales (pour info dans l'admin, pas le badge)
        page_view_count = qs.count()

        return {
            'visitor_country_count': country_count,
            'visitor_sessions':      session_count,       # "Visites" au sens analytics
            'visitor_page_views':    page_view_count,     # Pages vues brutes
            # Rétrocompat : visitor_total pointe vers les sessions
            'visitor_total':         session_count,
        }
    except Exception:
        return {
            'visitor_country_count': 0,
            'visitor_sessions':      0,
            'visitor_page_views':    0,
            'visitor_total':         0,
        }


def visitor_stats(request):
    """
    Context processor : injecte les stats de visites dans chaque template.
    Résultat mis en cache pendant CACHE_TTL secondes.
    """
    now = time.time()
    with _stats_lock:
        if _stats_cache['data'] is None or (now - _stats_cache['updated_at']) > CACHE_TTL:
            _stats_cache['data'] = _fetch_stats()
            _stats_cache['updated_at'] = now
        return _stats_cache['data']
