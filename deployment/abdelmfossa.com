server {
    listen 80;
    server_name abdelmfossa.com www.abdelmfossa.com;

    location = /favicon.ico { 
        access_log off; 
        log_not_found off; 
    }
    
    # Nginx sert les fichiers médias ajoutés par l'utilisateur plus tard.
    # Whitenoise s'occupe déjà silencieusement des fichiers statiques.
    location /media/ {
        root /var/www/abdelmfossa;
    }

    # Transfère tout le reste du trafic web à notre application Django via Gunicorn
    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn_abdelmfossa.sock;
    }
}
