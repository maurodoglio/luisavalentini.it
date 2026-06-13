# Deployment Plan

## Overview
Deploy the Django site to **Fly.io** with:
- GitHub Actions CI/CD pipeline
- Custom domain (luisavalentini.it)
- Free Let's Encrypt SSL certificate (automatic via Fly.io)

## Why Fly.io
- **Cost**: ~$3-5/month (shared CPU VM + 1GB volume for SQLite/media)
- **Dev-friendly**: Deploy with `fly deploy` or GitHub Actions
- **Built-in SSL**: Automatic Let's Encrypt certificate provisioning
- **Custom domains**: Simple DNS configuration
- **Docker-based**: Predictable, reproducible deployments

## Architecture
```
GitHub repo → GitHub Actions → Fly.io (Docker container)
                                  ├── Django app (gunicorn)
                                  ├── SQLite database (on persistent volume)
                                  ├── Media files (on persistent volume)
                                  └── Static files (whitenoise)
```

## Steps

### 1. Prepare the app for production
- [x] Add `gunicorn` to requirements
- [x] Add `whitenoise` for static files
- [x] Create `Dockerfile`
- [x] Create `fly.toml` configuration
- [x] Update settings.py for production (env-based config)
- [x] Create `.github/workflows/deploy.yml`

### 2. Deploy to Fly.io (manual first time)
- [ ] Install Fly CLI: `curl -L https://fly.io/install.sh | sh`
- [ ] Sign up: `fly auth signup`
- [ ] Create app: `fly launch` (from repo root)
- [ ] Create volume: `fly volumes create data --size 1`
- [ ] Set secrets: `fly secrets set SECRET_KEY=<random> DJANGO_SETTINGS_MODULE=luisavalentini.settings`
- [ ] First deploy: `fly deploy`
- [ ] Run migrations: `fly ssh console -C "python manage.py migrate"`
- [ ] Create superuser: `fly ssh console -C "python manage.py createsuperuser"`
- [ ] Upload media files: `fly ssh sftp shell` then put files

### 3. Configure custom domain
- [ ] Add domain: `fly certs add luisavalentini.it`
- [ ] Add domain: `fly certs add www.luisavalentini.it`
- [ ] Update DNS records at registrar:
  - `A` record → Fly.io IPv4 (shown by `fly ips list`)
  - `AAAA` record → Fly.io IPv6
  - `CNAME` for www → `luisavalentini.it`
- [ ] Fly.io automatically provisions Let's Encrypt SSL

### 4. Set up GitHub Actions
- [ ] Add `FLY_API_TOKEN` secret to GitHub repo settings
- [ ] Push to main/master triggers deploy automatically

## Domain Migration Checklist
1. Deploy and verify new site works on Fly.io URL (e.g., `luisavalentini.fly.dev`)
2. Lower DNS TTL on current domain (set to 300s, wait 24h)
3. Add custom domain to Fly.io app
4. Update DNS A/AAAA records to point to Fly.io IPs
5. SSL certificate auto-provisions (usually < 5 minutes)
6. Verify site works on luisavalentini.it
7. Shut down old hosting
