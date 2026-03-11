from django.contrib import admin
from .models import ShortLink

@admin.register(ShortLink)
class ShortLinkAdmin(admin.ModelAdmin):
    list_display = ('short_code', 'target_url', 'clicks', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('short_code', 'target_url')
    readonly_fields = ('clicks', 'created_at')
    
    fieldsets = (
        (None, {
            'fields': ('short_code', 'target_url', 'is_active')
        }),
        ('Statistiques & Informations', {
            'fields': ('clicks', 'created_at'),
            'classes': ('collapse',)
        }),
    )
