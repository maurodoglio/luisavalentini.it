# Deployment Plan

## Overview
Deploy the Django site to **DigitalOcean App Platform** with:
- GitHub auto-deploy (built-in, no Actions needed for deploy itself)
- Custom domain (luisavalentini.it)
- Free Let's Encrypt SSL certificate (automatic via DO)

## Why DigitalOcean App Platform
- **Reputable**: Established cloud provider since 2011, publicly traded (NYSE: DOCN)
- **Cost**: ~$5/month (Basic plan, 1 container)
- **Dev-friendly**: Native GitHub integration, auto-deploy on push
- **Built-in SSL**: Automatic Let's Encrypt certificate provisioning
- **Custom domains**: Simple configuration in dashboard
- **Docker-based**: Uses our Dockerfile directly

## Architecture
```
GitHub repo → DigitalOcean App Platform (auto-deploy on push)
                  ├── Django app (gunicorn, Docker container)
                  ├── Managed Database or SQLite on volume
                  ├── Media files (DO Spaces / volume)
                  └── Static files (whitenoise, served from container)
```

## Steps

### 1. Prepare the app for production ✅
- [x] Add `gunicorn` to requirements
- [x] Add `whitenoise` for static files
- [x] Create `Dockerfile`
- [x] Update settings.py for production (env-based config)
- [x] Create `.github/workflows/deploy.yml` (optional CI/test)

### 2. Deploy to DigitalOcean App Platform
- [ ] Sign up at https://cloud.digitalocean.com
- [ ] Create New App → choose GitHub repo
- [ ] Select "Dockerfile" as build method
- [ ] Configure environment variables:
  - `SECRET_KEY` = (generate random key)
  - `DEBUG` = False
  - `ALLOWED_HOSTS` = luisavalentini.it,www.luisavalentini.it,.ondigitalocean.app
  - `CSRF_TRUSTED_ORIGINS` = https://luisavalentini.it,https://www.luisavalentini.it
  - `DATA_DIR` = /data
  - `MEDIA_ROOT` = /data/media
  - `CONTACT_EMAIL` = mauro.doglio@gmail.com
- [ ] Choose Basic plan ($5/mo)
- [ ] Deploy
- [ ] Run one-time console command: `python manage.py migrate`
- [ ] Run: `python manage.py createsuperuser`
- [ ] Upload media files via console or DO Spaces

### 3. Configure custom domain
- [ ] In DO App settings → Domains → Add Domain
- [ ] Add `luisavalentini.it` and `www.luisavalentini.it`
- [ ] Update DNS records at registrar:
  - `A` record for `@` → DigitalOcean's provided IP
  - `CNAME` for `www` → `<app-name>.ondigitalocean.app`
- [ ] DO automatically provisions Let's Encrypt SSL certificate

### 4. GitHub integration (automatic)
- DigitalOcean App Platform watches your GitHub repo
- Any push to `master` triggers automatic redeploy
- No GitHub Actions needed for deployment (but kept for CI/tests)

## Domain Migration Checklist
1. Deploy and verify new site works on `<app-name>.ondigitalocean.app`
2. Lower DNS TTL on current domain (set to 300s, wait 24h for propagation)
3. Add custom domain in DigitalOcean dashboard
4. Update DNS A/CNAME records to point to DigitalOcean
5. SSL certificate auto-provisions (usually < 10 minutes)
6. Verify site works on https://luisavalentini.it
7. Shut down old hosting

## Alternative: GitHub Actions CI
The `.github/workflows/deploy.yml` can be used for running tests before
DigitalOcean's auto-deploy picks up the changes. DO deploys from the branch
directly — no API token needed for deployment.

