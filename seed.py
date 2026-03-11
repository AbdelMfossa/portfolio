import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from portfolio.models import Tag, Project, Article, Event, Video

def run():
    print("Nettoyage de la base de données...")
    Project.objects.all().delete()
    Article.objects.all().delete()
    Event.objects.all().delete()
    Video.objects.all().delete()
    Tag.objects.all().delete()

    print("Création des Tags...")
    tags_data = [
        "Google Apps Script", "Python", "API Google", "Google Workspace Admin SDK", 
        "Bash", "People API", "Automatisation", "Drive API", "Triggers", 
        "Classroom API", "Looker Studio", "Tutoriel", "Administration", 
        "Sécurité", "Étude de cas", "Intelligence Artificielle", "Gemini", 
        "NotebookLM", "DevOps", "Scripting", "HTML/CSS", "Web App", "Gmail API",
        "Apps Script"
    ]
    tags_dict = {}
    for name in tags_data:
        tag, _ = Tag.objects.get_or_create(name=name)
        tags_dict[name] = tag

    print("Création des Projets...")
    p1 = Project.objects.create(
        title="Automatisation du cycle de vie des comptes",
        description="Développement d'un pipeline complet de scripts pour automatiser la création, la gestion des accès, l'archivage et la suppression sécurisée des comptes utilisateurs au sein d'une organisation.",
        impact="Réduction de 70% du temps de gestion manuel par les administrateurs et élimination des erreurs de saisie.",
        image_url="https://images.unsplash.com/photo-1555949963-aa79dcee981c?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        icon="users",
        status="production",
        github_url="#"
    )
    p1.tags.add(tags_dict["Python"], tags_dict["Google Workspace Admin SDK"], tags_dict["Bash"])

    p2 = Project.objects.create(
        title="Synchronisation & Sauvegarde de Contacts",
        description="Conception d'un outil automatisé exploitant les API Google pour assurer la sauvegarde systématique et la synchronisation bidirectionnelle des contacts téléphoniques vers l'annuaire Google Contacts.",
        impact="Sécurisation à 100% du répertoire professionnel et prévention des pertes de données liées aux pannes d'appareils.",
        image_url="https://images.unsplash.com/photo-1611162617474-5b21e879e113?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        icon="contact",
        status="production",
        github_url="#"
    )
    p2.tags.add(tags_dict["Google Apps Script"], tags_dict["People API"], tags_dict["Automatisation"])

    p3 = Project.objects.create(
        title="Workflow d'Onboarding RH Automatisé",
        description="Création d'un système déclenché par un Google Form qui génère automatiquement les contrats (Docs), crée le dossier de l'employé (Drive), et envoie le mail de bienvenue (Gmail).",
        impact="Processus d'intégration des nouveaux employés accéléré de 2h à moins de 5 minutes par recrue.",
        image_url="https://images.unsplash.com/photo-1552664730-d307ca884978?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        icon="bot",
        status="poc",
        demo_url="#"
    )
    p3.tags.add(tags_dict["Google Apps Script"], tags_dict["Drive API"], tags_dict["Triggers"])

    p4 = Project.objects.create(
        title="Analytics pour Google Classroom",
        description="Script Python extrayant les métriques d'engagement depuis l'API Google Classroom pour alimenter un dashboard de suivi académique interactif destiné aux décideurs de l'université.",
        impact="Visibilité en temps réel sur l'activité de +80 000 utilisateurs, facilitant la prise de décision académique.",
        image_url="https://images.unsplash.com/photo-1460925895917-afdab827c52f?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        icon="bar-chart-3",
        status="production",
        article_url="#"
    )
    p4.tags.add(tags_dict["Python"], tags_dict["Classroom API"], tags_dict["Looker Studio"])


    print("Création des Articles...")
    a1 = Article.objects.create(
        title="Comment automatiser la création de rapports Google Docs avec Apps Script",
        summary="Dans ce tutoriel complet, nous allons explorer comment utiliser Google Apps Script pour générer automatiquement des rapports mensuels en PDF à partir de données extraites de Google Sheets, et les envoyer par email de manière totalement automatisée.",
        image_url="https://images.unsplash.com/photo-1516321318423-f06f85e504b3?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80",
        medium_url="http://medium.com/@abdelmfossa/ton-article-url",
        published_date="2024-03-15",
        read_time=5,
        category="Google Apps Script"
    )
    a1.tags.add(tags_dict["Automatisation"], tags_dict["Tutoriel"])

    a2 = Article.objects.create(
        title="Retour d'expérience : Gérer 80 000+ utilisateurs sur Google Workspace",
        summary="Déployer et sécuriser un environnement Google Workspace pour une université entière n'est pas une mince affaire. Voici mes stratégies, les pièges à éviter et les politiques de sécurité (2FA, MDM) que j'ai implémentées.",
        image_url="https://images.unsplash.com/photo-1550751827-4bd374c3f58b?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80",
        medium_url="http://medium.com/@abdelmfossa/ton-article-url",
        published_date="2024-02-02",
        read_time=8,
        category="Administration"
    )
    a2.tags.add(tags_dict["Sécurité"], tags_dict["Étude de cas"])

    a3 = Article.objects.create(
        title="NotebookLM : L'assistant IA ultime pour l'analyse de documents",
        summary="J'ai eu l'opportunité de présenter NotebookLM lors du DevFest Yaoundé. Dans cet article, je vous montre comment cet outil propulsé par Gemini peut révolutionner la façon dont vous interagissez avec vos sources de données complexes.",
        image_url="https://images.unsplash.com/photo-1620712943543-bcc4688e7485?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80",
        medium_url="http://medium.com/@abdelmfossa/ton-article-url",
        published_date="2024-01-28",
        read_time=6,
        category="Intelligence Artificielle"
    )
    a3.tags.add(tags_dict["Gemini"], tags_dict["NotebookLM"])

    a4 = Article.objects.create(
        title="5 bibliothèques Python indispensables pour l'automatisation IT",
        summary="Pour les administrateurs systèmes, Python est le couteau suisse par excellence. Découvrons ensemble 5 librairies méconnues mais redoutablement efficaces pour scripter vos tâches quotidiennes et gagner un temps précieux.",
        image_url="https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80",
        medium_url="http://medium.com/@abdelmfossa/ton-article-url",
        published_date="2023-12-10",
        read_time=4,
        category="Python"
    )
    a4.tags.add(tags_dict["DevOps"], tags_dict["Scripting"])


    print("Création des Événements...")
    Event.objects.create(
        title="DevFest Yaoundé 2025",
        description="En tant que Lead GDG, j'ai coordonné l'organisation globale du plus grand événement tech de la ville. J'ai également animé une keynote très suivie sur l'utilisation de NotebookLM et l'IA générative pour transformer l'analyse de documents.",
        image_url="https://images.unsplash.com/photo-1540575467063-178a50c2df87?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        date="2025-11-15",
        location="Yaoundé, Cameroun",
        role="Speaker & Lead Orga",
        role_icon="mic",
        official_site_url="#",
        linkedin_url="#",
        video_url="#"
    )
    
    Event.objects.create(
        title="Campagne \"Build with AI\"",
        description="Pilotage de l'initiative locale \"Build with AI\" propulsée par Google. Une journée entière dédiée à la formation des développeurs locaux sur les API Gemini, permettant la création de solutions basées sur l'intelligence artificielle.",
        image_url="https://images.unsplash.com/photo-1591115765373-5207764f72e7?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        date="2024-04-20",
        location="Yaoundé, Cameroun",
        role="Organisateur",
        role_icon="users",
        photos_url="#",
        linkedin_url="#"
    )
    
    Event.objects.create(
        title="Lancement du Google Developer Student Club (GDSC)",
        description="Création du tout premier club étudiant de l'Université de Yaoundé I. J'ai formé l'équipe Core (bureau), organisé des dizaines d'ateliers sur le dev Web/Mobile et aidé les étudiants à créer des solutions tech pour des ONG locales.",
        image_url="https://images.unsplash.com/photo-1522202176988-66273c2fd55f?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        date="2020-09-01",
        location="Université de Yaoundé I",
        role="Fondateur & Lead",
        role_icon="award",
        linkedin_url="#"
    )


    print("Création des Vidéos...")
    v1 = Video.objects.create(
        title="Créer une application web avec Google Apps Script de A à Z",
        description="Découvrez comment transformer une simple feuille de calcul Google Sheets en une véritable application web fonctionnelle avec interface HTML et CSS. Ce tutoriel couvre le backend (Apps Script), le frontend et le déploiement.",
        thumbnail_url="https://images.unsplash.com/photo-1611162616305-c69b3fa7fbe0?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80",
        youtube_url="#",
        duration="14:25",
        published_date=timezone.now() - timezone.timedelta(days=2),
        is_featured=True
    )
    v1.tags.add(tags_dict["Apps Script"], tags_dict["Web App"], tags_dict["HTML/CSS"])

    v2 = Video.objects.create(
        title="Automatiser l'envoi d'emails depuis Google Sheets avec Python",
        thumbnail_url="https://images.unsplash.com/photo-1551288049-bebda4e38f71?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        youtube_url="#",
        duration="08:12",
        published_date=timezone.now() - timezone.timedelta(days=14)
    )
    v2.tags.add(tags_dict["Python"], tags_dict["Gmail API"])

    v3 = Video.objects.create(
        title="Comment sécuriser un domaine Google Workspace (Tuto Admin)",
        thumbnail_url="https://images.unsplash.com/photo-1563986768494-4dee2763ff0f?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        youtube_url="#",
        duration="22:45",
        published_date=timezone.now() - timezone.timedelta(days=30)
    )
    v3.tags.add(tags_dict["Administration"], tags_dict["Sécurité"])

    v4 = Video.objects.create(
        title="Introduction à NotebookLM : Analysez vos documents avec l'IA",
        thumbnail_url="https://images.unsplash.com/photo-1620712943543-bcc4688e7485?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        youtube_url="#",
        duration="11:30",
        published_date=timezone.now() - timezone.timedelta(days=60)
    )
    v4.tags.add(tags_dict["Intelligence Artificielle"], tags_dict["NotebookLM"])

    print("Données initialisées avec succès ! 🎉")

if __name__ == '__main__':
    run()
