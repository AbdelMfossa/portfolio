from django.db import models
from django.utils.translation import gettext_lazy as _

class ShortLink(models.Model):
    target_url = models.URLField(_("URL cible"), max_length=1000, help_text=_("Le lien d'origine vers lequel rediriger"))
    short_code = models.CharField(_("Code court"), max_length=50, unique=True, help_text=_("Le mot clé pour le raccourci, ex: 'spotify'"))
    clicks = models.PositiveIntegerField(_("Nombre de clics"), default=0)
    created_at = models.DateTimeField(_("Date de création"), auto_now_add=True)
    is_active = models.BooleanField(_("Actif"), default=True)

    class Meta:
        verbose_name = _("Lien raccourci")
        verbose_name_plural = _("Liens raccourcis")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.short_code} -> {self.target_url}"
    
    def increment_clicks(self):
        self.clicks += 1
        self.save()
