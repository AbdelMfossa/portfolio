import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from portfolio.models import Tag, Project, Article, Event, Video, Certification, Skill, Experience

def translate_all():
    # 1. ARTICLES
    print("Translating Articles...")
    articles_map = {
        "Comment automatiser la création de rapports Google Docs avec Apps Script": {
            "title_en": "How to automate Google Docs report generation with Apps Script",
            "summary_en": "In this complete tutorial, we will explore how to use Google Apps Script to automatically generate professional reports from your data.",
            "category_en": "Automation / Tutorial"
        },
        "Retour d'expérience : Gérer 80 000+ utilisateurs sur Google Workspace": {
            "title_en": "Case Study: Managing 80,000+ users on Google Workspace",
            "summary_en": "Deploying and securing a Google Workspace environment for an entire university is no small task. Here is my feedback on this massive project.",
            "category_en": "Administration / Case Study"
        },
        "NotebookLM : L'assistant IA ultime pour l'analyse de documents": {
            "title_en": "NotebookLM: The ultimate AI assistant for document analysis",
            "summary_en": "I had the chance to present NotebookLM at DevFest Yaoundé. In this article, I show you how this AI tool can transform your information management.",
            "category_en": "Artificial Intelligence"
        }
    }
    for a in Article.objects.all():
        if a.title in articles_map:
            m = articles_map[a.title]
            a.title_en = m['title_en']
            a.summary_en = m['summary_en']
            a.category_en = m['category_en']
        # Always fill FR if empty
        if not a.title_fr: a.title_fr = a.title
        if not a.summary_fr: a.summary_fr = a.summary
        if not a.category_fr: a.category_fr = a.category
        a.save()

    # 2. PROJECTS
    print("Translating Projects...")
    projects_map = {
        "Analytics pour Google Classroom": {
            "title_en": "Google Classroom Analytics",
            "description_en": "Python script extracting engagement metrics from the Google Classroom API to fuel an interactive tracking dashboard for university decision-makers.",
            "impact_en": "Real-time visibility into the activity of +80,000 users, facilitating academic decision-making."
        },
        "Synchronisation & Sauvegarde de Contacts": {
            "title_en": "Contact Sync & Backup",
            "description_en": "Design of an automated tool using Google APIs to ensure systematic backup and bidirectional synchronization of professional contacts to the Google Contacts directory.",
            "impact_en": "100% security of the professional directory and prevention of data loss related to device failure."
        },
        "Workflow d'Onboarding RH Automatisé": {
            "title_en": "Automated HR Onboarding Workflow",
            "description_en": "System triggered by a Google Form that automatically generates contracts (Docs), creates the employee folder (Drive), and sends the welcome email (Gmail).",
            "impact_en": "New employee integration process accelerated from 2 hours to less than 5 minutes per recruit."
        }
    }
    for p in Project.objects.all():
        if p.title in projects_map:
            m = projects_map[p.title]
            p.title_en = m['title_en']
            p.description_en = m['description_en']
            p.impact_en = m['impact_en']
        if not p.title_fr: p.title_fr = p.title
        if not p.description_fr: p.description_fr = p.description
        if not p.impact_fr: p.impact_fr = p.impact
        p.save()

    # 3. EXPERIENCES
    print("Translating Experiences...")
    exp_map = {
        "Google Workspace Engineer": {
            "description_en": "Full administration and automation of the Google Workspace environment for over 80,000 users.",
            "location_en": "Greater London (Remote)"
        },
        "IT Manager & GW Support": {
            "description_en": "Management of information systems, full Google Workspace administration (deployment, onboarding/offboarding) and support for the digital transformation of the institution.",
            "location_en": "Yaoundé, Cameroon"
        },
        "Technical Trainer": {
            "description_en": "Designing and facilitating interactive training sessions on web technologies and cloud automation.",
            "location_en": "Yaoundé, Cameroon"
        }
    }
    for e in Experience.objects.all():
        if e.job_title in exp_map:
            m = exp_map[e.job_title]
            e.description_en = m['description_en']
            if 'location_en' in m: e.location_en = m['location_en']
        if not e.job_title_fr: e.job_title_fr = e.job_title
        if not e.description_fr: e.description_fr = e.description
        if not e.bullets_fr: e.bullets_fr = e.bullets
        if not e.location_fr: e.location_fr = e.location
        e.save()

    # 4. CERTIFICATIONS
    print("Translating Certifications...")
    for c in Certification.objects.all():
        if not c.title_fr: c.title_fr = c.title
        if not c.description_fr: c.description_fr = c.description
        if not c.provider_fr: c.provider_fr = c.provider
        
        # Simple auto-translation for common terms
        if "Administration" in c.title:
            c.title_en = c.title.replace("Administration", "Administration") # Already same
            c.description_en = "Mastery of the admin console, user management, access, and strict security policies."
        elif "Deployment" in c.title:
            c.title_en = c.title.replace("Services de Déploiement", "Deployment Services")
            c.description_en = "Certification validating expertise in planning, configuring, and migrating data to the ecosystem."
        elif "Automation" in c.title or "Automatisation" in c.title:
            c.title_en = "IT Automation with Python"
            c.description_en = "Specialization in automating system administration tasks and configuration management via scripts."
        c.save()

    # 5. TAGS & GENERAL FIX
    print("Finalizing all other models...")
    for model in [Tag, Event, Video, Skill]:
        for item in model.objects.all():
            fields = [f.name for f in model._meta.fields]
            fr_fields = [f for f in fields if f.endswith('_fr')]
            for fr_f in fr_fields:
                base_f = fr_f[:-3]
                if getattr(item, base_f) and not getattr(item, fr_f):
                    setattr(item, fr_f, getattr(item, base_f))
            item.save()

if __name__ == "__main__":
    translate_all()
    print("🎉 All dynamic content fully synchronized and translated!")
