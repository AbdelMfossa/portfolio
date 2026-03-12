from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import Tag, Project, Article, Event, Video, Certification, Skill, Experience

@admin.register(Tag)
class TagAdmin(TranslationAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Project)
class ProjectAdmin(TranslationAdmin):
    list_display = ('title', 'status', 'created_at')
    list_filter = ('status', 'tags')
    search_fields = ('title', 'description', 'impact')
    filter_horizontal = ('tags',)

@admin.register(Article)
class ArticleAdmin(TranslationAdmin):
    list_display = ('title', 'category', 'published_date', 'read_time')
    list_filter = ('category', 'published_date', 'tags')
    search_fields = ('title', 'summary')
    filter_horizontal = ('tags',)

@admin.register(Event)
class EventAdmin(TranslationAdmin):
    list_display = ('title', 'date', 'location', 'role')
    list_filter = ('date', 'location')
    search_fields = ('title', 'description')

@admin.register(Video)
class VideoAdmin(TranslationAdmin):
    list_display = ('title', 'published_date', 'duration', 'is_featured')
    list_filter = ('is_featured', 'published_date', 'tags')
    search_fields = ('title', 'description')
    filter_horizontal = ('tags',)

@admin.register(Certification)
class CertificationAdmin(TranslationAdmin):
    list_display = ('title', 'provider', 'issue_date')
    list_filter = ('provider', 'issue_date', 'tags')
    search_fields = ('title', 'provider', 'description')
    filter_horizontal = ('tags',)

@admin.register(Skill)
class SkillAdmin(TranslationAdmin):
    list_display = ('title', 'order', 'color')
    list_editable = ('order',)
    search_fields = ('title', 'description')

@admin.register(Experience)
class ExperienceAdmin(TranslationAdmin):
    list_display = ('job_title', 'company', 'order')
    list_editable = ('order',)
    search_fields = ('job_title', 'company', 'description')
