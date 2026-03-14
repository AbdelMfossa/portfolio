"""
Middleware de tracking des visiteurs pour le portfolio.

Fonctionnalités :
- Enregistrement asynchrone (thread) pour ne pas ralentir les réponses
- Déduplication par session (fenêtre de 30 min) : une actualisation de page n'est PAS recomptée
- En mode DEBUG : IP complète affichée, données fictives pour l'IP locale (tests)
- En production (DEBUG=False) : IP anonymisée automatiquement (RGPD)
- L'URL admin (définie dans .env via ADMIN_URL) est exclue du tracking
- Les bots sont ignorés via user-agents
- Géolocalisation via ip-api.com (sans clé API, gratuit)
"""
import hashlib
import threading
import urllib.request
import json
import time
import os
from urllib.parse import urlparse

from django.utils import timezone
from django.conf import settings

try:
    from user_agents import parse as parse_ua
    HAS_UA = True
except ImportError:
    HAS_UA = False

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# En mode DEBUG (dev) → IP complète affichée pour faciliter les tests.
# En production (DEBUG=False) → IP anonymisée pour la conformité RGPD.
# Pour forcer l'anonymisation même en debug : VISITOR_ANONYMIZE_IP = True dans settings.py
ANONYMIZE_IP = getattr(settings, 'VISITOR_ANONYMIZE_IP', not settings.DEBUG)

# Fenêtre de déduplication : une même page n'est comptée qu'une fois
# par session dans cet intervalle de temps.
DEDUP_WINDOW_SECONDS = 30 * 60  # 30 minutes

# URL admin récupérée depuis le .env pour être exclue du tracking
_ADMIN_URL_PREFIX = '/' + os.environ.get('ADMIN_URL', 'admin/')

# Cache en mémoire des résultats de géolocalisation (IP → dict)
_geo_cache: dict = {}
_geo_lock = threading.Lock()


def _get_ignored_prefixes() -> tuple:
    """Retourne la liste des préfixes d'URL à ne pas loguer."""
    return (
        '/static/', '/media/', '/favicon', '/rosetta/', '/robots.txt',
        '/sitemap', '/__debug__', '/jsi18n/',
        _ADMIN_URL_PREFIX,  # URL admin dynamique depuis .env (ex: /url-ghost/)
    )


# ---------------------------------------------------------------------------
# Fonctions utilitaires
# ---------------------------------------------------------------------------

def _anonymize_ip(ip: str) -> str:
    """Masque les 2 derniers octets IPv4 ou la moitié d'une IPv6 (conformité RGPD)."""
    if not ip:
        return ''
    if ':' in ip:
        parts = ip.split(':')
        return ':'.join(parts[:4]) + ':xxxx:xxxx:xxxx:xxxx'
    parts = ip.split('.')
    if len(parts) == 4:
        return f"{parts[0]}.{parts[1]}.xxx.xxx"
    return ip


def _get_client_ip(request) -> str:
    """Récupère l'IP réelle même derrière un proxy/Nginx (X-Forwarded-For)."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '')


def _get_geo(ip: str) -> dict:
    """
    Géolocalise une IP via ip-api.com (gratuit, 1000 req/min, sans clé API).

    - En mode DEBUG : retourne des données fictives pour les IPs locales (127.x, 192.168.x…)
      afin de tester l'interface admin sans serveur de production.
    - En production : les IPs locales retournent un dict vide (aucune requête réseau faite).
    """
    if not ip:
        return {}

    is_local = ip.startswith(('127.', '192.168.', '10.', '::1'))
    if is_local:
        if settings.DEBUG:
            # Données fictives pour le dev local uniquement
            return {
                'country':      'Local (Dev)',
                'country_code': 'XX',
                'region':       'Localhost',
                'city':         'Développement',
            }
        return {}

    # Vérifier le cache d'abord
    with _geo_lock:
        if ip in _geo_cache:
            return _geo_cache[ip]

    try:
        url = f"http://ip-api.com/json/{ip}?fields=status,country,countryCode,regionName,city"
        with urllib.request.urlopen(url, timeout=2) as resp:
            data = json.loads(resp.read())
            if data.get('status') == 'success':
                result = {
                    'country':      data.get('country', ''),
                    'country_code': data.get('countryCode', ''),
                    'region':       data.get('regionName', ''),
                    'city':         data.get('city', ''),
                }
                with _geo_lock:
                    _geo_cache[ip] = result
                return result
    except Exception:
        pass
    return {}


def _get_referrer_domain(referrer: str) -> str:
    """Extrait le domaine (sans www.) depuis une URL référente."""
    try:
        parsed = urlparse(referrer)
        domain = parsed.netloc.lower()
        if domain.startswith('www.'):
            domain = domain[4:]
        return domain
    except Exception:
        return ''


def _get_session_hash(request) -> str:
    """Génère une clé de session anonyme à partir de l'IP + User-Agent (sans stocker de données perso)."""
    raw = f"{_get_client_ip(request)}{request.META.get('HTTP_USER_AGENT', '')}"
    return hashlib.sha256(raw.encode()).hexdigest()[:32]


# ---------------------------------------------------------------------------
# Déduplication
# ---------------------------------------------------------------------------

def _should_log(request, path: str) -> bool:
    """
    Retourne True uniquement si cette visite doit être enregistrée.

    Logique : si la même session a déjà visité cette page dans les
    DEDUP_WINDOW_SECONDS dernières secondes, on renvoie False (doublon ignoré).
    Sinon, on mémorise la visite dans la session Django et on renvoie True.
    """
    if not hasattr(request, 'session'):
        return True

    now_ts = time.time()
    visited = request.session.get('_visited_pages', {})

    last_visit_ts = visited.get(path)
    if last_visit_ts and (now_ts - last_visit_ts) < DEDUP_WINDOW_SECONDS:
        return False  # Déjà loggé récemment → on ignore

    # Mémoriser la visite dans la session
    visited[path] = now_ts

    # Limiter la taille du dict en session (max 50 pages)
    if len(visited) > 50:
        oldest_key = min(visited, key=visited.get)
        del visited[oldest_key]

    request.session['_visited_pages'] = visited
    request.session.modified = True
    return True


# ---------------------------------------------------------------------------
# Enregistrement asynchrone
# ---------------------------------------------------------------------------

def _log_visit_async(request, path: str):
    """
    Collecte toutes les informations disponibles sur le visiteur
    et les sauvegarde en base de données.
    Exécuté dans un thread séparé pour ne pas ralentir la réponse HTTP.
    """
    from portfolio.models import VisitorLog

    raw_ip    = _get_client_ip(request)
    ua_string = request.META.get('HTTP_USER_AGENT', '')
    referrer  = request.META.get('HTTP_REFERER', '')
    language  = request.META.get('HTTP_ACCEPT_LANGUAGE', '').split(',')[0][:20]

    # --- Parse du User-Agent ---
    browser = browser_version = os_name = device_type = ''
    if HAS_UA and ua_string:
        ua = parse_ua(ua_string)
        browser         = ua.browser.family or ''
        browser_version = ua.browser.version_string or ''
        os_name         = ua.os.family or ''
        if ua.is_bot:
            device_type = 'bot'
        elif ua.is_mobile:
            device_type = 'mobile'
        elif ua.is_tablet:
            device_type = 'tablet'
        elif ua.is_pc:
            device_type = 'desktop'
        else:
            device_type = 'other'

    # Ignorer les bots
    if device_type == 'bot':
        return

    # --- Géolocalisation ---
    geo = _get_geo(raw_ip)

    # --- Choix IP complète ou anonymisée ---
    stored_ip = raw_ip if not ANONYMIZE_IP else _anonymize_ip(raw_ip)

    VisitorLog.objects.create(
        page            = path,
        ip_address      = stored_ip,
        session_key     = _get_session_hash(request),
        country         = geo.get('country', ''),
        country_code    = geo.get('country_code', ''),
        city            = geo.get('city', ''),
        region          = geo.get('region', ''),
        browser         = browser,
        browser_version = browser_version,
        os              = os_name,
        device_type     = device_type,
        referrer        = referrer[:500],
        referrer_domain = _get_referrer_domain(referrer),
        language        = language,
        user_agent      = ua_string[:500],
        timestamp       = timezone.now(),
    )


# ---------------------------------------------------------------------------
# Middleware principal
# ---------------------------------------------------------------------------

class VisitorTrackingMiddleware:
    """
    Middleware Django léger pour le tracking des visiteurs.

    Ce middleware :
    1. Laisse passer la requête normalement (aucun délai ajouté)
    2. Vérifie si la page doit être loggée (exclusions, méthode, statut)
    3. Vérifie la déduplication via la session
    4. Lance l'enregistrement dans un thread daemon en arrière-plan
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # 1) Exclure les chemins ignorés (statiques, admin, favicon…)
        path = request.path
        if any(path.startswith(p) for p in _get_ignored_prefixes()):
            return response

        # 2) Ne logger que les pages HTML (pas les images, JS, CSS…)
        content_type = response.get('Content-Type', '')
        if 'text/html' not in content_type:
            return response

        # 3) Ne logger que les succès (200 OK)
        if response.status_code != 200:
            return response

        # 4) GET uniquement
        if request.method != 'GET':
            return response

        # 5) Vérification de déduplication par session
        if not _should_log(request, path):
            return response

        # 6) Enregistrement asynchrone (thread daemon)
        thread = threading.Thread(
            target=_log_visit_async,
            args=(request, path),
            daemon=True
        )
        thread.start()

        return response
