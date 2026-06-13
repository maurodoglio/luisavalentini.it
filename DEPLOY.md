# Deployment Plan

## Overview
Deploy the Django site to a **DigitalOcean Droplet** ($6/mo = $72/year) with:
- SQLite database (persistent on disk)
- GitHub Actions auto-deploy via SSH on push to `master`
- nginx reverse proxy
- Let's Encrypt SSL certificate (auto-renewed via certbot)
- Custom domain (luisavalentini.it)

## Architecture
```
GitHub repo → GitHub Actions (test + SSH deploy)
                        ↓
DigitalOcean Droplet (Ubuntu 24.04, $6/mo)
    ├── nginx (reverse proxy + static/media serving + SSL)
    ├── gunicorn (Django app via systemd)
    ├── SQLite database (/opt/luisavalentini/data/db.sqlite3)
    └── Media files (/opt/luisavalentini/data/media/)
```

## Cost
- Droplet: $6/mo (1 vCPU, 1GB RAM, 25GB SSD) — more than enough
- **Total: $72/year**

## Steps

### 1. Create the Droplet
1. Log in to https://cloud.digitalocean.com
2. Create Droplet:
   - **Image**: Ubuntu 24.04 LTS
   - **Plan**: Basic, Regular, $6/mo (1 vCPU / 1GB / 25GB)
   - **Region**: Amsterdam (AMS3) or closest to users
   - **Authentication**: SSH key (add your public key)
3. Note the Droplet's IP address

### 2. Run server setup script
From your local machine:
```bash
ssh root@YOUR_DROPLET_IP < server_setup.sh
```
This installs nginx, Python, creates the `deploy` user, systemd service, and firewall rules.

### 3. Generate and set SECRET_KEY
```bash
ssh root@YOUR_DROPLET_IP
# Edit the systemd service file:
nano /etc/systemd/system/luisavalentini.service
# Replace CHANGE_ME with a real key (generate with):
python3 -c "import secrets; print(secrets.token_urlsafe(50))"
# Then reload:
systemctl daemon-reload
```

### 4. Clone the repo on the server
```bash
ssh deploy@YOUR_DROPLET_IP
git clone https://github.com/maurodoglio/luisavalentini.it.git /opt/luisavalentini/app
cd /opt/luisavalentini/app
bash deploy.sh
```

### 5. Import data and create admin
```bash
ssh deploy@YOUR_DROPLET_IP
cd /opt/luisavalentini/app
/opt/luisavalentini/venv/bin/python manage.py import_legacy_data
/opt/luisavalentini/venv/bin/python manage.py createsuperuser
```

### 6. Upload media files
From your local machine (where the `media/` folder exists):
```bash
scp -r media/* deploy@YOUR_DROPLET_IP:/opt/luisavalentini/data/media/
```

### 7. Configure GitHub Actions secrets
In your repo → Settings → Secrets and variables → Actions:
- `SERVER_IP` = your Droplet's IP address
- `SSH_PRIVATE_KEY` = a deploy SSH private key (generate a dedicated one)

Generate deploy key:
```bash
ssh-keygen -t ed25519 -f deploy_key -N ""
# Add deploy_key.pub to the server:
ssh root@YOUR_DROPLET_IP "cat >> /home/deploy/.ssh/authorized_keys" < deploy_key.pub
# Add deploy_key (private) as GitHub secret SSH_PRIVATE_KEY
```

### 8. Allow deploy user to restart the service
```bash
ssh root@YOUR_DROPLET_IP
echo "deploy ALL=(ALL) NOPASSWD: /bin/systemctl restart luisavalentini" >> /etc/sudoers.d/deploy
chmod 440 /etc/sudoers.d/deploy
```

### 9. Configure DNS and SSL
1. Point DNS at your registrar:
   - `A` record for `@` → Droplet IP
   - `A` record for `www` → Droplet IP (or CNAME to @)
2. Wait for propagation (check with `dig luisavalentini.it`)
3. Install SSL:
```bash
ssh root@YOUR_DROPLET_IP
certbot --nginx -d luisavalentini.it -d www.luisavalentini.it
```
Certbot auto-renews via a systemd timer (already set up on Ubuntu).

## How deploys work after setup
1. You push to `master`
2. GitHub Actions runs tests
3. If tests pass, SSHs into the server and runs `git pull` + `deploy.sh`
4. `deploy.sh` installs deps, runs migrations, collects static, restarts gunicorn
5. Site is live within ~10 seconds

## Maintenance
- **SSL renewal**: Automatic (certbot timer)
- **OS updates**: `ssh root@IP "apt update && apt upgrade -y"` monthly
- **Backups**: Download SQLite: `scp deploy@IP:/opt/luisavalentini/data/db.sqlite3 ./`
- **Logs**: `ssh deploy@IP "journalctl -u luisavalentini --since today"`
