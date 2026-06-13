# Deployment Plan

## Overview
Deploy the Django site to **DigitalOcean App Platform** ($5/mo = $60/year) with:
- SQLite database on a persistent volume (no managed DB needed)
- GitHub auto-deploy (built-in, no Actions needed for deploy itself)
- Custom domain (luisavalentini.it)
- Free Let's Encrypt SSL certificate (automatic via DO)

## Architecture
```
GitHub repo → DigitalOcean App Platform (auto-deploy on push to master)
                  ├── Django app (gunicorn, Docker container)
                  ├── SQLite on persistent volume (/data)
                  ├── Media files on persistent volume (/data/media)
                  └── Static files (WhiteNoise, served from container)
```

## Cost Breakdown
- App Platform Basic ($5/mo) — 1 container, 512MB RAM
- Persistent volume (free, included up to 1GB on Basic)
- **Total: $60/year**

## Steps

### 1. Prepare the app for production ✅
- [x] Add `gunicorn` to requirements
- [x] Add `whitenoise` for static files
- [x] Create `Dockerfile` with startup script (auto-migrates on deploy)
- [x] Update settings.py for production (env-based config)
- [x] Create `.github/workflows/deploy.yml` (CI/test on PRs)

### 2. Deploy to DigitalOcean App Platform
1. Sign up at https://cloud.digitalocean.com
2. Create New App → Connect GitHub → Select this repo
3. Select "Dockerfile" as build method
4. Add a **persistent volume**:
   - Mount path: `/data`
   - Size: 1GB (plenty for SQLite + media)
5. Configure environment variables:
   - `SECRET_KEY` = (generate: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
   - `DEBUG` = False
   - `ALLOWED_HOSTS` = luisavalentini.it,www.luisavalentini.it,.ondigitalocean.app
   - `CSRF_TRUSTED_ORIGINS` = https://luisavalentini.it,https://www.luisavalentini.it
   - `DATA_DIR` = /data
   - `MEDIA_ROOT` = /data/media
   - `CONTACT_EMAIL` = mauro.doglio@gmail.com
   - `EMAIL_BACKEND` = django.core.mail.backends.smtp.EmailBackend
   - `EMAIL_HOST` = smtp.gmail.com
   - `EMAIL_PORT` = 587
   - `EMAIL_USE_TLS` = True
   - `EMAIL_HOST_USER` = (your gmail)
   - `EMAIL_HOST_PASSWORD` = (gmail app password)
6. Choose **Basic** plan ($5/mo)
7. Deploy

### 3. Post-deploy setup (one-time)
Run these via DO Console (App → Console tab):
```bash
# Create admin user
python manage.py createsuperuser

# Import legacy data
python manage.py import_legacy_data

# Copy media files (upload via scp or DO Console)
# Media goes to /data/media/
```

### 4. Upload media files
Option A — via DO Console:
```bash
# From your local machine, tar the media folder and upload
tar czf media.tar.gz media/
# Then in DO Console, download and extract to /data/media/
```

Option B — add media to git (simplest for this small site):
- The `media/` folder is ~15MB total (thumbnails + images)
- Add to repo, and in Dockerfile copy to /data/media on first run

### 5. Configure custom domain
1. In DO App settings → Domains → Add Domain
2. Add `luisavalentini.it` and `www.luisavalentini.it`
3. Update DNS records at your registrar:
   - `A` record for `@` → DigitalOcean's provided IP
   - `CNAME` for `www` → `<app-name>.ondigitalocean.app`
4. DO automatically provisions Let's Encrypt SSL certificate (~5-10 min)

### 6. GitHub integration (automatic)
- DigitalOcean watches your GitHub repo
- Any push to `master` triggers automatic redeploy
- Migrations run automatically on startup (via start.sh)
- No GitHub Actions needed for deployment

## Domain Migration Checklist
1. Deploy and verify new site works on `<app-name>.ondigitalocean.app`
2. Lower DNS TTL on current domain (set to 300s, wait 24h for propagation)
3. Add custom domain in DigitalOcean dashboard
4. Update DNS A/CNAME records to point to DigitalOcean
5. SSL certificate auto-provisions (usually < 10 minutes)
6. Verify site works on https://luisavalentini.it
7. Shut down old hosting
