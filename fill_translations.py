import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from portfolio.models import Tag, Project, Article, Event, Video, Certification, Skill, Experience

def translate_skill():
    print("Translating Skills...")
    for s in Skill.objects.all():
        # Ensure FR is filled
        if not s.title_fr: s.title_fr = s.title
        if not s.description_fr: s.description_fr = s.description
        if not s.bullets_fr: s.bullets_fr = s.bullets
        
        # Translate to EN (Simple mapping for now)
        if s.title == "Automatisation":
            s.title_en = "Automation"
            s.description_en = "Automate your repetitive tasks to save time."
            s.bullets_en = "Google Apps Script\nPython Automation\nWorkflow Integration"
        elif s.title == "IA & Innovation":
            s.title_en = "AI & Innovation"
            s.description_en = "Leveraging GenAI and NotebookLM for productivity."
            s.bullets_en = "Generative AI\nNotebookLM Expert\nPrompt Engineering"
        elif s.title == "Google Workspace":
            s.title_en = "Google Workspace"
            s.description_en = "Management and optimization of your digital workspace."
            s.bullets_en = "System Administration\nSecurity & Compliance\nMigration & Support"
        s.save()

def translate_experience():
    print("Translating Experiences...")
    for e in Experience.objects.all():
        if not e.job_title_fr: e.job_title_fr = e.job_title
        if not e.description_fr: e.description_fr = e.description
        if not e.bullets_fr: e.bullets_fr = e.bullets
        
        if "Engineer" in e.job_title:
            e.job_title_en = "Google Workspace Engineer"
            e.description_en = "Administration and automation for over 80k users."
        elif "Lead" in e.job_title and "GDG" in e.job_title:
            e.job_title_en = "GDG Yaoundé Lead"
            e.description_en = "Coordinating the tech community and organizing major events like DevFest."
        elif "Trainer" in e.job_title:
            e.job_title_en = "Technical Trainer"
            e.description_en = "Designing and facilitating web and cloud technology training sessions."
        
        e.save()

def translate_project():
    print("Translating Projects...")
    for p in Project.objects.all():
        if not p.title_fr: p.title_fr = p.title
        if not p.description_fr: p.description_fr = p.description
        if not p.impact_fr: p.impact_fr = p.impact
        
        if "Portfolio" in p.title:
            p.title_en = "Personal Portfolio"
            p.description_en = "A modern portfolio built with Django and Tailwind CSS."
        elif "Automis" in p.title:
            p.title_en = "Automis"
            p.description_en = "Automation tool for managing complex workflows."
            
        p.save()

def general_fix():
    print("Fixing other models (copying FR)...")
    models = [Tag, Article, Event, Video, Certification]
    for model in models:
        for item in model.objects.all():
            updated = False
            fields = [f.name for f in model._meta.fields]
            fr_fields = [f for f in fields if f.endswith('_fr')]
            for fr_f in fr_fields:
                base_f = fr_f[:-3]
                if getattr(item, base_f) and not getattr(item, fr_f):
                    setattr(item, fr_f, getattr(item, base_f))
                    updated = True
            if updated:
                item.save()

if __name__ == "__main__":
    translate_skill()
    translate_experience()
    translate_project()
    general_fix()
    print("Done!")
