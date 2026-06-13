#!/bin/bash
set -e

echo "Running migrations..."
python manage.py migrate --noinput

# On first deploy, seed media files to persistent volume if empty
if [ -d "/app/media" ] && [ ! -d "/data/media/opere" ]; then
    echo "Seeding media files to persistent volume..."
    cp -r /app/media/* /data/media/ 2>/dev/null || true
fi

echo "Starting gunicorn..."
exec gunicorn luisavalentini.wsgi:application --bind 0.0.0.0:8000 --workers 2
