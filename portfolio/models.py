from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.utils.text import slugify
import os
from PIL import Image


class VisitorLog(models.Model):
    DEVICE_CHOICES = [
        ('desktop', 'Desktop'),
        ('mobile', 'Mobile'),
        ('tablet', 'Tablette'),
        ('bot', 'Bot'),
        ('other', 'Autre'),
    ]

    # --- Quand & Où ---
    timestamp       = models.DateTimeField(default=timezone.now, verbose_name="Date/Heure")
    page            = models.CharField(max_length=300, verbose_name="Page visitée")

    # --- Qui ---
    ip_address      = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP (anonymisée)")
    session_key     = models.CharField(max_length=64, blank=True, verbose_name="Clé de session")

    # --- D'où (Géolocalisation) ---
    country         = models.CharField(max_length=100, blank=True, verbose_name="Pays")
    country_code    = models.CharField(max_length=5, blank=True, verbose_name="Code Pays")
    city            = models.CharField(max_length=100, blank=True, verbose_name="Ville")
    region          = models.CharField(max_length=100, blank=True, verbose_name="Région")

    # --- Avec quoi ---
    browser         = models.CharField(max_length=100, blank=True, verbose_name="Navigateur")
    browser_version = models.CharField(max_length=30, blank=True, verbose_name="Version navigateur")
    os              = models.CharField(max_length=100, blank=True, verbose_name="Système d'exploitation")
    device_type     = models.CharField(max_length=20, choices=DEVICE_CHOICES, default='other', verbose_name="Type d'appareil")

    # --- Comment ---
    referrer        = models.URLField(max_length=500, blank=True, verbose_name="Page de référence")
    referrer_domain = models.CharField(max_length=150, blank=True, verbose_name="Domaine référent")
    language        = models.CharField(max_length=20, blank=True, verbose_name="Langue du navigateur")
    user_agent      = models.TextField(blank=True, verbose_name="User-Agent complet")

    class Meta:
        verbose_name = "Visite"
        verbose_name_plural = "Visites"
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['country_code']),
            models.Index(fields=['device_type']),
            models.Index(fields=['page']),
        ]

    def __str__(self):
        return f"[{self.timestamp.strftime('%d/%m/%Y %H:%M')}] {self.page} — {self.country or 'Inconnu'}"


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Nom du tag")
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Project(models.Model):
    STATUS_CHOICES = (
        ('production', 'En production'),
        ('poc', 'PoC / Démo'),
        ('development', 'En développement'),
    )
    
    title = models.CharField(max_length=200, verbose_name="Titre du projet")
    description = models.TextField(verbose_name="Description détaillée")
    impact = models.CharField(max_length=255, blank=True, null=True, verbose_name="Impact métier")
    
    image = models.ImageField(upload_to='projects/', blank=True, null=True, verbose_name="Image de couverture")
    image_url = models.URLField(blank=True, null=True, verbose_name="URL de l'image (Ex: Unsplash)")
    icon = models.CharField(max_length=50, default='users', verbose_name="Icône Lucide (ex: users, bot)")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='production', verbose_name="Statut")
    is_active = models.BooleanField(default=True, verbose_name="Actif (visible sur le site)")

    github_url = models.URLField(blank=True, null=True, verbose_name="Lien GitHub")
    demo_url = models.URLField(blank=True, null=True, verbose_name="Lien de Démo")
    article_url = models.URLField(blank=True, null=True, verbose_name="Lien de l'article (Medium)")
    
    tags = models.ManyToManyField(Tag, related_name='projects', blank=True)
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Date de création")

    class Meta:
        verbose_name = "Projet"
        verbose_name_plural = "Projets"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            try:
                img = Image.open(self.image.path)
                if img.height > 1080 or img.width > 1920:
                    output_size = (1920, 1080)
                    img.thumbnail(output_size, Image.Resampling.LANCZOS)
                
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                    
                img.save(self.image.path, optimize=True, quality=80)
            except Exception:
                pass

class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titre de l'article")
    summary = models.TextField(verbose_name="Extrait / Résumé")
    
    image = models.ImageField(upload_to='articles/', blank=True, null=True, verbose_name="Image de couverture")
    image_url = models.URLField(blank=True, null=True, verbose_name="URL de l'image (Ex: Unsplash)")
    
    medium_url = models.URLField(verbose_name="Lien Medium")
    published_date = models.DateField(default=timezone.now, verbose_name="Date de publication")
    read_time = models.PositiveIntegerField(default=5, verbose_name="Temps de lecture (minutes)")
    is_active = models.BooleanField(default=True, verbose_name="Actif (visible sur le site)")

    category = models.CharField(max_length=100, verbose_name="Catégorie principale (ex: Intelligence Artificielle)")
    tags = models.ManyToManyField(Tag, related_name='articles', blank=True)

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        ordering = ['-published_date']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            try:
                img = Image.open(self.image.path)
                if img.height > 800 or img.width > 1200:
                    output_size = (1200, 800)
                    img.thumbnail(output_size, Image.Resampling.LANCZOS)
                
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                
                img.save(self.image.path, optimize=True, quality=80)
            except Exception:
                pass

class Event(models.Model):
    title = models.CharField(max_length=200, verbose_name="Nom de l'événement")
    description = models.TextField(verbose_name="Description de l'événement")
    
    image = models.ImageField(upload_to='events/', blank=True, null=True, verbose_name="Image de l'événement")
    image_url = models.URLField(blank=True, null=True, verbose_name="URL de l'image (Ex: Unsplash)")
    
    date = models.DateField(default=timezone.now, verbose_name="Date de l'événement")
    location = models.CharField(max_length=200, default='Yaoundé, Cameroun', verbose_name="Lieu")
    
    role = models.CharField(max_length=100, verbose_name="Rôle (ex: Speaker & Lead Orga)")
    role_icon = models.CharField(max_length=50, default='mic', verbose_name="Icône du rôle (ex: mic, users)")
    
    official_site_url = models.URLField(blank=True, null=True, verbose_name="Lien site officiel")
    linkedin_url = models.URLField(blank=True, null=True, verbose_name="Lien post LinkedIn")
    video_url = models.URLField(blank=True, null=True, verbose_name="Lien replay vidéo")
    photos_url = models.URLField(blank=True, null=True, verbose_name="Lien galerie photos")
    is_active = models.BooleanField(default=True, verbose_name="Actif (visible sur le site)")

    class Meta:
        verbose_name = "Événement"
        verbose_name_plural = "Événements"
        ordering = ['-date']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            try:
                img = Image.open(self.image.path)
                if img.height > 1080 or img.width > 1920:
                    output_size = (1920, 1080)
                    img.thumbnail(output_size, Image.Resampling.LANCZOS)
                    img.save(self.image.path, optimize=True, quality=80)
            except Exception:
                pass

class Video(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titre de la vidéo")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    
    thumbnail = models.ImageField(upload_to='videos/', blank=True, null=True, verbose_name="Miniature")
    thumbnail_url = models.URLField(blank=True, null=True, verbose_name="URL de la miniature (Ex: Unsplash)")
    
    youtube_url = models.URLField(verbose_name="Lien YouTube")
    duration = models.CharField(max_length=10, help_text="Ex: 14:25", verbose_name="Durée")
    
    published_date = models.DateField(default=timezone.now, verbose_name="Date de publication")
    is_featured = models.BooleanField(default=False, verbose_name="Mettre à la une")
    is_active = models.BooleanField(default=True, verbose_name="Actif (visible sur le site)")

    tags = models.ManyToManyField(Tag, related_name='videos', blank=True)

    class Meta:
        verbose_name = "Vidéo"
        verbose_name_plural = "Vidéos"
        ordering = ['-published_date']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.thumbnail:
            try:
                img = Image.open(self.thumbnail.path)
                if img.height > 720 or img.width > 1280:
                    output_size = (1280, 720)
                    img.thumbnail(output_size, Image.Resampling.LANCZOS)
                
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                    
                img.save(self.thumbnail.path, optimize=True, quality=80)
            except Exception:
                pass

class Certification(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titre de la certification")
    provider = models.CharField(max_length=100, verbose_name="Fournisseur (ex: Google, Coursera)")
    issue_date = models.DateField(default=timezone.now, verbose_name="Date d'obtention")
    description = models.TextField(verbose_name="Description")
    
    image = models.ImageField(upload_to='certifications/', blank=True, null=True, verbose_name="Image de fond")
    image_url = models.URLField(blank=True, null=True, verbose_name="URL de l'image (Ex: Unsplash)")
    icon = models.CharField(max_length=50, default='award', verbose_name="Icône Lucide (ex: cloud, shield-check)")
    
    verify_url = models.URLField(blank=True, null=True, verbose_name="Lien de vérification")
    is_active = models.BooleanField(default=True, verbose_name="Actif (visible sur le site)")

    tags = models.ManyToManyField(Tag, related_name='certifications', blank=True)

    class Meta:
        verbose_name = "Certification"
        verbose_name_plural = "Certifications"
        ordering = ['-issue_date']

    def __str__(self):
        return f"{self.title} - {self.provider}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 1000 or img.width > 1000:
                output_size = (1000, 1000)
                img.thumbnail(output_size, Image.Resampling.LANCZOS)
                img.save(self.image.path, optimize=True, quality=80)

class Skill(models.Model):
    title = models.CharField(max_length=100, verbose_name="Titre de la compétence")
    icon = models.CharField(max_length=50, default='cloud', verbose_name="Icône Lucide")
    color = models.CharField(max_length=20, default='blue', help_text="Couleur Tailwind (ex: blue, emerald, purple, red)", verbose_name="Couleur principale")
    description = models.TextField(blank=True, null=True, verbose_name="Description optionnelle")
    
    # Pour stocker les points de la liste, on peut utiliser un TextField où chaque ligne est un point
    bullets = models.TextField(help_text="Un point par ligne", verbose_name="Points clés de la compétence")
    
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")
    is_active = models.BooleanField(default=True, verbose_name="Actif (visible sur le site)")

    class Meta:
        verbose_name = "Expertise (Skill)"
        verbose_name_plural = "Expertises (Skills)"
        ordering = ['order']

    def __str__(self):
        return self.title
        
    def get_bullets_list(self):
        return [b.strip() for b in self.bullets.split('\n') if b.strip()]

class Experience(models.Model):
    job_title = models.CharField(max_length=200, verbose_name="Titre du poste")
    company = models.CharField(max_length=200, verbose_name="Entreprise / Organisation")
    period = models.CharField(max_length=100, verbose_name="Période (ex: Mai 2022 - Présent)")
    location = models.CharField(max_length=200, verbose_name="Lieu")
    
    description = models.TextField(verbose_name="Description détaillée")
    bullets = models.TextField(help_text="Un point par ligne", verbose_name="Tâches / Réalisations")
    
    icon = models.CharField(max_length=50, default='briefcase', verbose_name="Icône Lucide")
    color = models.CharField(max_length=20, default='blue-600', help_text="Couleur ex: blue-600, slate-400, purple-500", verbose_name="Couleur d'accent")
    
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")

    class Meta:
        verbose_name = "Expérience"
        verbose_name_plural = "Expériences"
        ordering = ['order']

    def __str__(self):
        return f"{self.job_title} chez {self.company}"
        
    def get_bullets_list(self):
        return [b.strip() for b in self.bullets.split('\n') if b.strip()]

class ContactMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Nom complet"))
    email = models.EmailField(verbose_name=_("Adresse email"))
    subject = models.CharField(max_length=200, verbose_name=_("Sujet"))
    message = models.TextField(verbose_name=_("Message"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Date de réception"))
    is_read = models.BooleanField(default=False, verbose_name=_("Message lu"))

    class Meta:
        verbose_name = _("Message de contact")
        verbose_name_plural = _("Messages de contact")
        ordering = ['-created_at']

    def __str__(self):
        return f"Message de {self.name} - {self.subject}"
