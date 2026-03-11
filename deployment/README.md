# Guide de déploiement (VPS Ubuntu)

Ce dossier contient les fichiers de configuration nécessaires pour que ton application Django tourne en permanence (Gunicorn via Systemd) et réponde sur le web (via Nginx).

**Hypothèses** :
- Le nom d'utilisateur Ubuntu est `ubuntu` (adapter dans `gunicorn_portfolio.service` si c'est `root` ou autre).
- Le projet sera cloné dans `/var/www/portfolio`.

## 1. Copie des fichiers Systemd (pour Gunicorn)
Exécute ces commandes depuis le dossier racine du projet sur ton serveur :

```bash
sudo cp deployment/gunicorn_portfolio.socket /etc/systemd/system/
sudo cp deployment/gunicorn_portfolio.service /etc/systemd/system/
```

Activer et démarrer Gunicorn :
```bash
sudo systemctl start gunicorn_portfolio.socket
sudo systemctl enable gunicorn_portfolio.socket
sudo systemctl status gunicorn_portfolio.socket
```
*(Si ça dit active/running, c'est parfait !)*

## 2. Configuration de Nginx
Toujours depuis ton serveur :

```bash
# Copie ta configuration nginx
sudo cp deployment/abdelmfossa.com /etc/nginx/sites-available/

# Crée le lien symbolique pour l'activer
sudo ln -s /etc/nginx/sites-available/abdelmfossa.com /etc/nginx/sites-enabled/

# Vérifie que tu n'as pas de conflit nginx (Syntax OK)
sudo nginx -t

# Redémarre Nginx
sudo systemctl restart nginx
```

## 3. Configuration HTTPS (Certbot)
Une fois ton nom de domaine lié à l'IP de ton serveur, lance Let's Encrypt :

```bash
sudo apt install python3-certbot-nginx
sudo certbot --nginx -d abdelmfossa.com -d www.abdelmfossa.com
```

Cerbot va automatiquement trouver ton bloc server dans le fichier /etc/nginx/sites-available/abdelmfossa.com et ajouter le HTTPS sécurisé !
