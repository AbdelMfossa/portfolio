"""
Script de population des articles Medium d'Abdel Aziz Mfossa.
Source : https://medium.com/@abdelmfossa (8 articles extraits le 15/03/2026)

Usage :
  python populate_articles.py

Ce script est idempotent : il vérifie si l'article existe déjà (par medium_url)
avant de le créer pour éviter les doublons. Tu peux le relancer sans risque.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from portfolio.models import Article, Tag
from django.utils.dateparse import parse_date

# ---------------------------------------------------------------------------
# Données des articles (extraites du flux RSS Medium le 15/03/2026)
# ---------------------------------------------------------------------------

ARTICLES = [
    {
        "title_fr": "Automatiser vos Groupes Dynamiques dans Google Workspace (Même sans licence Enterprise) avec Apps Script",
        "title_en": "Automate Dynamic Groups in Google Workspace (Even Without Enterprise License) with Apps Script",
        "summary_fr": (
            "Gérer manuellement l'appartenance aux groupes de messagerie dans Google Workspace est une "
            "tâche chronophage et source d'erreurs. Dans cet article, nous allons voir pourquoi les groupes "
            "dynamiques sont cruciaux pour votre gouvernance, et comment recréer cette fonctionnalité "
            "de toutes pièces grâce à Google Apps Script."
        ),
        "summary_en": (
            "Manually managing mailing group membership in Google Workspace is time-consuming and error-prone. "
            "In this article, we explore why dynamic groups are crucial for your governance, and how to "
            "recreate this feature from scratch using Google Apps Script."
        ),
        "medium_url": "https://medium.com/@abdelmfossa/automatiser-vos-groupes-dynamiques-dans-google-workspace-meme-sans-licence-enterprise-avec-apps-script-cc7d36f35ca8",
        "published_date": "2026-02-25",
        "read_time": 5,
        "category": "Google Workspace",
        "tags": ["Google Apps Script", "Automatisation", "Google Workspace"],
        "image_url": "https://miro.medium.com/v2/resize:fit:1200/format:webp/1*some-image.jpg",
    },
    {
        "title_fr": "5 secrets des comptes e-mail institutionnels que votre université ne vous dit pas",
        "title_en": "5 Secrets About Institutional Email Accounts Your University Never Tells You",
        "summary_fr": (
            "Recevoir son adresse e-mail universitaire est souvent perçu comme une simple formalité "
            "administrative. Pourtant, derrière cet outil se cachent des mécanismes, des avantages "
            "et des risques que la plupart des étudiants ignorent complètement."
        ),
        "summary_en": (
            "Receiving a university email address is often seen as a mere administrative formality. "
            "Yet behind this tool lie mechanisms, benefits, and risks that most students are completely unaware of."
        ),
        "medium_url": "https://medium.com/@abdelmfossa/les-5-secrets-de-votre-compte-e-mail-institutionnel-que-votre-universit%C3%A9-ne-vous-dit-pas-93f74df423dd",
        "published_date": "2025-11-30",
        "read_time": 8,
        "category": "Éducation",
        "tags": ["Google Workspace for Education", "Email", "Étudiants"],
    },
    {
        "title_fr": "Simplifiez la génération et l'envoi des Attestations aux participants avec Google Apps Script",
        "title_en": "Simplify Certificate Generation and Distribution with Google Apps Script",
        "summary_fr": (
            "L'automatisation de tâches répétitives est la clé pour gagner du temps, réduire les "
            "erreurs humaines et permettre aux organisateurs de se concentrer sur des aspects plus "
            "stratégiques de l'événement. Ce tutoriel explique comment générer et envoyer "
            "automatiquement des attestations de participation avec Apps Script."
        ),
        "summary_en": (
            "Automating repetitive tasks is the key to saving time, reducing human error, and allowing "
            "organizers to focus on more strategic aspects of the event. This tutorial explains how to "
            "automatically generate and send participation certificates with Apps Script."
        ),
        "medium_url": "https://medium.com/@abdelmfossa/simplifiez-la-g%C3%A9n%C3%A9ration-et-lenvoi-des-attestations-aux-participants-avec-google-app-script-d63d50c694b9",
        "published_date": "2025-11-21",
        "read_time": 7,
        "category": "Automatisation",
        "tags": ["Google Apps Script", "Google Slides", "Google Sheets", "Automatisation"],
    },
    {
        "title_fr": "Automatisation des réservations à un événement avec Google Forms et Apps Script",
        "title_en": "Automating Event Registrations with Google Forms and Apps Script",
        "summary_fr": (
            "Imaginez organiser un événement tech régional avec des inscriptions automatisées : "
            "code d'accès personnalisé, mail de confirmation, classement par niveau et fermeture "
            "automatique du formulaire à quota atteint. C'est exactement ce que nous allons construire "
            "avec Google Forms et Apps Script."
        ),
        "summary_en": (
            "Imagine organizing a regional tech event with automated registrations: personalized access code, "
            "confirmation email, level-based classification, and automatic form closure when capacity is reached. "
            "That's exactly what we'll build with Google Forms and Apps Script."
        ),
        "medium_url": "https://medium.com/@abdelmfossa/automatisation-des-reservations-a-un-evenement-avec-google-forms-et-apps-script-42379dddbb9c",
        "published_date": "2025-05-14",
        "read_time": 5,
        "category": "Automatisation",
        "tags": ["Google Apps Script", "Google Forms", "Automatisation", "Événements"],
    },
    {
        "title_fr": "Automatiser la création des Contacts avec Apps Script et Google Forms",
        "title_en": "Automate Contact Creation with Apps Script and Google Forms",
        "summary_fr": (
            "La gestion des contacts peut devenir une tâche fastidieuse, surtout lorsque vous devez "
            "ajouter ou mettre à jour des informations pour un grand nombre de personnes. "
            "Heureusement, Google Apps Script permet d'automatiser ce processus directement depuis "
            "un Google Forms."
        ),
        "summary_en": (
            "Managing contacts can become a tedious task, especially when you need to add or update "
            "information for a large number of people. Fortunately, Google Apps Script allows you to "
            "automate this process directly from a Google Form."
        ),
        "medium_url": "https://medium.com/@abdelmfossa/automatiser-la-sauvegarde-des-contacts-avec-apps-script-et-google-forms-2dfa4478bc3f",
        "published_date": "2024-07-30",
        "read_time": 3,
        "category": "Automatisation",
        "tags": ["Google Apps Script", "Google Forms", "Google Contacts", "Google Workspace"],
    },
    {
        "title_fr": "Introduction à Apps Script : l'outil de productivité et d'automatisation de Google Workspace",
        "title_en": "Introduction to Apps Script: Google Workspace's Productivity and Automation Tool",
        "summary_fr": (
            "Vous exploitez quotidiennement Gmail, Docs, Sheets, Slides, Forms et Drive ? "
            "Et si vous pouviez décupler la puissance de ces outils en les personnalisant à votre guise ? "
            "C'est là que Google Apps Script entre en jeu ! Découvrez comment ce langage basé sur "
            "JavaScript vous permet d'automatiser et d'étendre vos applications Google."
        ),
        "summary_en": (
            "You use Gmail, Docs, Sheets, Slides, Forms, and Drive daily? What if you could multiply "
            "the power of these tools by customizing them to your needs? That's where Google Apps Script "
            "comes in! Discover how this JavaScript-based language lets you automate and extend your "
            "Google applications."
        ),
        "medium_url": "https://medium.com/@abdelmfossa/introduction-a-apps-script-outil-de-productivite-et-d-automatisation-de-google-workspace-e7c61e9cfbb3",
        "published_date": "2024-04-08",
        "read_time": 4,
        "category": "Google Workspace",
        "tags": ["Google Apps Script", "Google Workspace", "Productivité", "Automatisation"],
    },
    {
        "title_fr": "Pourquoi choisir Python ?",
        "title_en": "Why Choose Python?",
        "summary_fr": (
            "Python est un langage de programmation très populaire et apprécié par de nombreux "
            "développeurs. Open source, syntaxe concise, communauté active, compatibilité multi-OS... "
            "Découvrez pourquoi Python s'est imposé comme le langage de référence pour le web, "
            "l'IA, l'automatisation et la data science."
        ),
        "summary_en": (
            "Python is a very popular programming language appreciated by many developers. Open source, "
            "concise syntax, active community, multi-OS compatibility... Discover why Python has become "
            "the go-to language for web development, AI, automation, and data science."
        ),
        "medium_url": "https://medium.com/@abdelmfossa/pourquoi-choisir-python-9215687a3b5c",
        "published_date": "2024-01-23",
        "read_time": 4,
        "category": "Programmation",
        "tags": ["Python", "Programmation", "Productivité"],
    },
    {
        "title_fr": "Comment profiter au maximum de son adresse e-mail universitaire ?",
        "title_en": "How to Make the Most of Your University Email Address?",
        "summary_fr": (
            "Si vous êtes étudiant, vous avez sans doute reçu une adresse e-mail universitaire ou "
            "institutionnelle de la part de votre établissement. Mais savez-vous réellement à quoi "
            "elle sert et comment l'utiliser au maximum ? Avantages exclusifs, outils gratuits, "
            "services premium... voici tout ce que vous devez savoir."
        ),
        "summary_en": (
            "If you're a student, you've likely received a university or institutional email address "
            "from your institution. But do you really know what it's for and how to use it to the "
            "fullest? Exclusive benefits, free tools, premium services... here's everything you need to know."
        ),
        "medium_url": "https://medium.com/@abdelmfossa/comment-profiter-au-maximum-de-son-adresse-e-mail-universitaire-6abdc6ce7af0",
        "published_date": "2023-10-17",
        "read_time": 6,
        "category": "Éducation",
        "tags": ["Email", "Google Workspace for Education", "Étudiants"],
    },
]


def get_or_create_tag(name):
    """Récupère ou crée un tag par son nom."""
    from django.utils.text import slugify
    slug = slugify(name)
    tag, created = Tag.objects.get_or_create(
        slug=slug,
        defaults={'name': name}
    )
    if created:
        print(f"   🏷️  Tag créé : {name}")
    return tag


def populate():
    print("=" * 60)
    print("📝 Population des articles Medium d'Abdel Aziz Mfossa")
    print("=" * 60)

    created_count = 0
    skipped_count = 0

    for data in ARTICLES:
        # Vérification idempotente : on ne crée pas si l'URL existe déjà
        if Article.objects.filter(medium_url=data["medium_url"]).exists():
            print(f"\n⏭️  Déjà existant : {data['title_fr'][:60]}...")
            skipped_count += 1
            continue

        print(f"\n✍️  Création : {data['title_fr'][:60]}...")

        article = Article(
            medium_url      = data["medium_url"],
            published_date  = parse_date(data["published_date"]),
            read_time       = data["read_time"],
            category        = data["category"],
        )

        # Champs traduits (français)
        article.title_fr   = data["title_fr"]
        article.summary_fr = data["summary_fr"]
        # Champs traduits (anglais)
        article.title_en   = data["title_en"]
        article.summary_en = data["summary_en"]
        # Champs par défaut (langue de base = fr)
        article.title      = data["title_fr"]
        article.summary    = data["summary_fr"]

        # Image URL optionnelle
        article.image_url = data.get("image_url", "")

        article.save()

        # Association des tags
        for tag_name in data.get("tags", []):
            tag = get_or_create_tag(tag_name)
            article.tags.add(tag)

        print(f"   ✅ Créé avec {len(data.get('tags', []))} tags")
        created_count += 1

    print("\n" + "=" * 60)
    print(f"✅ Terminé ! {created_count} article(s) créé(s), {skipped_count} ignoré(s) (déjà présent)")
    print("=" * 60)


if __name__ == "__main__":
    populate()
