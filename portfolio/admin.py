from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from django.db.models import Count
from datetime import timedelta
from modeltranslation.admin import TranslationAdmin
from .models import Tag, Project, Article, Event, Video, Certification, Skill, Experience, VisitorLog


@admin.register(VisitorLog)
class VisitorLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'page', 'country_flag', 'city', 'browser', 'device_icon', 'referrer_badge')
    list_filter  = ('device_type', 'country_code', 'browser', 'os')
    search_fields = ('page', 'country', 'city', 'referrer_domain', 'ip_address')
    readonly_fields = [f.name for f in VisitorLog._meta.fields]
    date_hierarchy = 'timestamp'
    ordering = ['-timestamp']

    # Désactiver add/delete depuis l'admin (lecture seule)
    def has_add_permission(self, request): return False
    def has_delete_permission(self, request, obj=None): return True
    def has_change_permission(self, request, obj=None): return False

    def country_flag(self, obj):
        if obj.country_code:
            flag = ''.join(chr(0x1F1E6 + ord(c) - ord('A')) for c in obj.country_code.upper())
            return format_html('<span title="{}">{} {}</span>', obj.country, flag, obj.country)
        return '🌐 Inconnu'
    country_flag.short_description = 'Pays'

    def device_icon(self, obj):
        icons = {'desktop': '🖥️', 'mobile': '📱', 'tablet': '📟', 'bot': '🤖', 'other': '❓'}
        return format_html('<span title="{}">{}</span>', obj.device_type, icons.get(obj.device_type, '❓'))
    device_icon.short_description = 'Appareil'

    def referrer_badge(self, obj):
        if obj.referrer_domain:
            color_map = {
                'linkedin.com': '#0077B5', 'twitter.com': '#1DA1F2', 'x.com': '#000000',
                'github.com': '#24292E', 'google.com': '#4285F4', 't.me': '#2AABEE',
            }
            color = color_map.get(obj.referrer_domain, '#6B7280')
            return format_html(
                '<span style="background:{};color:white;padding:2px 8px;border-radius:12px;font-size:11px">{}</span>',
                color, obj.referrer_domain
            )
        return format_html('<span style="color:#aaa">Direct</span>')
    referrer_badge.short_description = 'Source'

    def changelist_view(self, request, extra_context=None):
        """Injecte les statistiques dans la vue liste."""
        now   = timezone.now()
        today = now.date()

        qs = VisitorLog.objects.exclude(device_type='bot')

        stats = {
            'total_today':   qs.filter(timestamp__date=today).count(),
            'total_7d':      qs.filter(timestamp__gte=now - timedelta(days=7)).count(),
            'total_30d':     qs.filter(timestamp__gte=now - timedelta(days=30)).count(),
            'total_all':     qs.count(),
            'unique_7d':     qs.filter(timestamp__gte=now - timedelta(days=7)).values('session_key').distinct().count(),
            'top_countries': qs.filter(timestamp__gte=now - timedelta(days=30))\
                               .exclude(country='')\
                               .values('country', 'country_code')\
                               .annotate(n=Count('id')).order_by('-n')[:8],
            'top_pages':     qs.filter(timestamp__gte=now - timedelta(days=30))\
                               .values('page').annotate(n=Count('id')).order_by('-n')[:8],
            'devices':       qs.filter(timestamp__gte=now - timedelta(days=30))\
                               .values('device_type').annotate(n=Count('id')),
            'top_referrers': qs.filter(timestamp__gte=now - timedelta(days=30))\
                               .exclude(referrer_domain='')\
                               .values('referrer_domain').annotate(n=Count('id')).order_by('-n')[:6],
        }

        extra_context = extra_context or {}
        extra_context['visitor_stats'] = stats
        return super().changelist_view(request, extra_context=extra_context)

@admin.register(Tag)
class TagAdmin(TranslationAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Project)
class ProjectAdmin(TranslationAdmin):
    list_display  = ('title', 'status', 'active_badge', 'created_at')
    list_filter   = ('status', 'is_active', 'tags')
    list_editable = ('status',)
    search_fields = ('title', 'description', 'impact')
    filter_horizontal = ('tags',)
    actions = ['activate_selected', 'deactivate_selected']

    def active_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="color:#16a34a;font-size:16px" title="Actif">✅</span>')
        return format_html('<span style="color:#dc2626;font-size:16px" title="Désactivé">❌</span>')
    active_badge.short_description = 'Visible'

    @admin.action(description="✅ Activer la sélection")
    def activate_selected(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} élément(s) activé(s).")

    @admin.action(description="❌ Désactiver la sélection")
    def deactivate_selected(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} élément(s) désactivé(s).")


@admin.register(Article)
class ArticleAdmin(TranslationAdmin):
    list_display  = ('title', 'category', 'published_date', 'read_time', 'active_badge')
    list_filter   = ('is_active', 'category', 'published_date', 'tags')
    search_fields = ('title', 'summary')
    filter_horizontal = ('tags',)
    actions = ['activate_selected', 'deactivate_selected']

    def active_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="color:#16a34a;font-size:16px" title="Actif">✅</span>')
        return format_html('<span style="color:#dc2626;font-size:16px" title="Désactivé">❌</span>')
    active_badge.short_description = 'Visible'

    @admin.action(description="✅ Activer la sélection")
    def activate_selected(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description="❌ Désactiver la sélection")
    def deactivate_selected(self, request, queryset):
        queryset.update(is_active=False)


@admin.register(Event)
class EventAdmin(TranslationAdmin):
    list_display  = ('title', 'date', 'location', 'role', 'active_badge')
    list_filter   = ('is_active', 'date', 'location')
    search_fields = ('title', 'description')
    actions = ['activate_selected', 'deactivate_selected']

    def active_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="color:#16a34a;font-size:16px" title="Actif">✅</span>')
        return format_html('<span style="color:#dc2626;font-size:16px" title="Désactivé">❌</span>')
    active_badge.short_description = 'Visible'

    @admin.action(description="✅ Activer la sélection")
    def activate_selected(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description="❌ Désactiver la sélection")
    def deactivate_selected(self, request, queryset):
        queryset.update(is_active=False)


@admin.register(Video)
class VideoAdmin(TranslationAdmin):
    list_display  = ('title', 'published_date', 'duration', 'is_featured', 'active_badge')
    list_filter   = ('is_active', 'is_featured', 'published_date', 'tags')
    search_fields = ('title', 'description')
    filter_horizontal = ('tags',)
    actions = ['activate_selected', 'deactivate_selected']

    def active_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="color:#16a34a;font-size:16px" title="Actif">✅</span>')
        return format_html('<span style="color:#dc2626;font-size:16px" title="Désactivé">❌</span>')
    active_badge.short_description = 'Visible'

    @admin.action(description="✅ Activer la sélection")
    def activate_selected(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description="❌ Désactiver la sélection")
    def deactivate_selected(self, request, queryset):
        queryset.update(is_active=False)


@admin.register(Certification)
class CertificationAdmin(TranslationAdmin):
    list_display  = ('title', 'provider', 'issue_date', 'active_badge')
    list_filter   = ('is_active', 'provider', 'issue_date', 'tags')
    search_fields = ('title', 'provider', 'description')
    filter_horizontal = ('tags',)
    actions = ['activate_selected', 'deactivate_selected']

    def active_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="color:#16a34a;font-size:16px" title="Actif">✅</span>')
        return format_html('<span style="color:#dc2626;font-size:16px" title="Désactivé">❌</span>')
    active_badge.short_description = 'Visible'

    @admin.action(description="✅ Activer la sélection")
    def activate_selected(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description="❌ Désactiver la sélection")
    def deactivate_selected(self, request, queryset):
        queryset.update(is_active=False)


@admin.register(Skill)
class SkillAdmin(TranslationAdmin):
    list_display  = ('title', 'order', 'color', 'active_badge')
    list_editable = ('order',)
    list_filter   = ('is_active',)
    search_fields = ('title', 'description')
    actions = ['activate_selected', 'deactivate_selected']

    def active_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="color:#16a34a;font-size:16px" title="Actif">✅</span>')
        return format_html('<span style="color:#dc2626;font-size:16px" title="Désactivé">❌</span>')
    active_badge.short_description = 'Visible'

    @admin.action(description="✅ Activer la sélection")
    def activate_selected(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description="❌ Désactiver la sélection")
    def deactivate_selected(self, request, queryset):
        queryset.update(is_active=False)


@admin.register(Experience)
class ExperienceAdmin(TranslationAdmin):
    list_display = ('job_title', 'company', 'order')
    list_editable = ('order',)
    search_fields = ('job_title', 'company', 'description')
