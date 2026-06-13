#!/bin/bash
# Deploy script - runs on the server after code is pushed.
# Called by GitHub Actions or manually.
set -e

APP_DIR="/opt/luisavalentini"
REPO_DIR="$APP_DIR/app"

cd $REPO_DIR

# Install/update dependencies
$APP_DIR/venv/bin/pip install --quiet -r requirements.txt

# Run migrations
$APP_DIR/venv/bin/python manage.py migrate --noinput

# Collect static files
$APP_DIR/venv/bin/python manage.py collectstatic --noinput

# Restart the app
sudo systemctl restart luisavalentini

echo "Deploy complete!"
