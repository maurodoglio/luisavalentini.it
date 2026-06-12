# Luisa Valentini - Portfolio Website

Modern Django 5.x rewrite of the artist portfolio, migrated from Django 1.3 / Python 2.7.

## Setup

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py import_legacy_data db_backup.json
python manage.py createsuperuser
python manage.py runserver
```

## Data Import

The `db_backup.json` file contains the legacy database dump (from Django `dumpdata`).
Run the custom management command to import the `opere` app data:

```bash
python manage.py import_legacy_data db_backup.json
```

This imports:
- **72 Mostre** (exhibitions)
- **210 Opere** (artworks: sculptures, jewelry, drawings)

## Project Structure

```
luisavalentini/     # Django project settings
opere/              # Main app (artworks & exhibitions)
templates/          # HTML templates
static/             # CSS, images, JS
media/              # User-uploaded files (not in git)
db_backup.json      # Legacy data dump
```

## What Changed from the Legacy Version

- **Django 1.3 → Django 5.x** (Python 2.7 → Python 3.12)
- **MySQL → SQLite** (simpler for development, easily switchable)
- **Removed django-cms** - replaced with simple template-based pages
- **Removed**: south, photologue, tagging, tinymce, filebrowser, admin_tools
- **Modernized**: templates (HTML5), URLs (path-based), views (function-based with shortcuts)
- **Added**: proper migrations, management command for data import
