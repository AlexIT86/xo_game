#!/usr/bin/env bash
# exit on error
set -o errexit

# Instalează dependențele
pip install -r requirements.txt

# Colectează static files
python manage.py collectstatic --no-input

# Rulează migrările
python manage.py migrate

