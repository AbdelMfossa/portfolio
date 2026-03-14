"""
Context processor qui injecte des statistiques de visiteurs globales
dans tous les templates (pour le footer badge et éventuellement d'autres zones).

Les stats sont mises en cache en mémoire pendant 10 minutes pour ne pas
faire de requêtes DB à chaque chargement de page.
"""
import time
import threading

_stats_cache = {'data': None, 'updated_at': 0}
_stats_lock = threading.Lock()

CACHE_TTL = 10 * 60  # 10 minutes


def _fetch_stats() -> dict:
    """Interroge la base de données pour calculer les stats globales."""
    try:
        from portfolio.models import VisitorLog
        from django.db.models import Count

        qs = VisitorLog.objects.exclude(device_type='bot')

        country_count = (
            qs.exclude(country_code='')
              .exclude(country_code='XX')   # Exclure les entrées "Local (Dev)"
              .values('country_code')
              .distinct()
              .count()
        )
        total_visits = qs.count()

        return {
            'visitor_country_count': country_count,
            'visitor_total':         total_visits,
        }
    except Exception:
        return {
            'visitor_country_count': 0,
            'visitor_total':         0,
        }


def visitor_stats(request):
    """
    Context processor : injecte visitor_country_count et visitor_total
    dans le contexte de chaque template.

    Résultat mis en cache pendant CACHE_TTL secondes pour éviter
    une requête DB à chaque page vue.
    """
    now = time.time()
    with _stats_lock:
        if _stats_cache['data'] is None or (now - _stats_cache['updated_at']) > CACHE_TTL:
            _stats_cache['data'] = _fetch_stats()
            _stats_cache['updated_at'] = now
        return _stats_cache['data']
