#!/bin/bash
set -e

echo "Running migrations..."
python manage.py migrate --noinput

# Ensure media directory structure exists on persistent volume
mkdir -p /data/media

echo "Starting gunicorn..."
exec gunicorn luisavalentini.wsgi:application --bind 0.0.0.0:8000 --workers 2
