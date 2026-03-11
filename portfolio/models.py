from django.db import models
from django.utils import timezone
from django.utils.text import slugify

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

class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titre de l'article")
    summary = models.TextField(verbose_name="Extrait / Résumé")
    
    image = models.ImageField(upload_to='articles/', blank=True, null=True, verbose_name="Image de couverture")
    image_url = models.URLField(blank=True, null=True, verbose_name="URL de l'image (Ex: Unsplash)")
    
    medium_url = models.URLField(verbose_name="Lien Medium")
    published_date = models.DateField(default=timezone.now, verbose_name="Date de publication")
    read_time = models.PositiveIntegerField(default=5, verbose_name="Temps de lecture (minutes)")
    
    category = models.CharField(max_length=100, verbose_name="Catégorie principale (ex: Intelligence Artificielle)")
    tags = models.ManyToManyField(Tag, related_name='articles', blank=True)

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        ordering = ['-published_date']

    def __str__(self):
        return self.title

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

    class Meta:
        verbose_name = "Événement"
        verbose_name_plural = "Événements"
        ordering = ['-date']

    def __str__(self):
        return self.title

class Video(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titre de la vidéo")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    
    thumbnail = models.ImageField(upload_to='videos/', blank=True, null=True, verbose_name="Miniature")
    thumbnail_url = models.URLField(blank=True, null=True, verbose_name="URL de la miniature (Ex: Unsplash)")
    
    youtube_url = models.URLField(verbose_name="Lien YouTube")
    duration = models.CharField(max_length=10, help_text="Ex: 14:25", verbose_name="Durée")
    
    published_date = models.DateField(default=timezone.now, verbose_name="Date de publication")
    is_featured = models.BooleanField(default=False, verbose_name="Mettre à la une")
    
    tags = models.ManyToManyField(Tag, related_name='videos', blank=True)

    class Meta:
        verbose_name = "Vidéo"
        verbose_name_plural = "Vidéos"
        ordering = ['-published_date']

    def __str__(self):
        return self.title

class Certification(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titre de la certification")
    provider = models.CharField(max_length=100, verbose_name="Fournisseur (ex: Google, Coursera)")
    issue_date = models.DateField(default=timezone.now, verbose_name="Date d'obtention")
    description = models.TextField(verbose_name="Description")
    
    image = models.ImageField(upload_to='certifications/', blank=True, null=True, verbose_name="Image de fond")
    image_url = models.URLField(blank=True, null=True, verbose_name="URL de l'image (Ex: Unsplash)")
    icon = models.CharField(max_length=50, default='award', verbose_name="Icône Lucide (ex: cloud, shield-check)")
    
    verify_url = models.URLField(blank=True, null=True, verbose_name="Lien de vérification")
    
    tags = models.ManyToManyField(Tag, related_name='certifications', blank=True)

    class Meta:
        verbose_name = "Certification"
        verbose_name_plural = "Certifications"
        ordering = ['-issue_date']

    def __str__(self):
        return f"{self.title} - {self.provider}"
