from modeltranslation.translator import register, TranslationOptions
from .models import Tag, Project, Article, Event, Video, Certification, Skill, Experience

@register(Tag)
class TagTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Project)
class ProjectTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'impact')

@register(Article)
class ArticleTranslationOptions(TranslationOptions):
    fields = ('title', 'summary', 'category')

@register(Event)
class EventTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'location', 'role')

@register(Video)
class VideoTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

@register(Certification)
class CertificationTranslationOptions(TranslationOptions):
    fields = ('title', 'provider', 'description')

@register(Skill)
class SkillTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'bullets')

@register(Experience)
class ExperienceTranslationOptions(TranslationOptions):
    fields = ('job_title', 'company', 'location', 'description', 'bullets')
