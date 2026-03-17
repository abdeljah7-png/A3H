#!/bin/bash

# Applique toutes les migrations
python manage.py migrate --noinput

# Collecte les fichiers statiques
python manage.py collectstatic --noinput

# Démarre Gunicorn
gunicorn erp.wsgi:application --bind 0.0.0.0:$PORT