#!/bin/bash
# Run this script on a fresh Ubuntu 22.04/24.04 Droplet to set up the site.
# Usage: ssh root@your-droplet-ip < server_setup.sh
set -e

APP_USER="deploy"
APP_DIR="/opt/luisavalentini"
DOMAIN="luisavalentini.it"

echo "=== Creating deploy user ==="
useradd -m -s /bin/bash $APP_USER || true
mkdir -p /home/$APP_USER/.ssh
cp /root/.ssh/authorized_keys /home/$APP_USER/.ssh/
chown -R $APP_USER:$APP_USER /home/$APP_USER/.ssh

echo "=== Installing system packages ==="
apt-get update
apt-get install -y python3 python3-pip python3-venv nginx certbot python3-certbot-nginx git ufw

echo "=== Setting up firewall ==="
ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw --force enable

echo "=== Creating app directory ==="
mkdir -p $APP_DIR
mkdir -p $APP_DIR/data
mkdir -p $APP_DIR/data/media
chown -R $APP_USER:$APP_USER $APP_DIR

echo "=== Creating virtual environment ==="
sudo -u $APP_USER python3 -m venv $APP_DIR/venv

echo "=== Creating systemd service ==="
cat > /etc/systemd/system/luisavalentini.service << 'EOF'
[Unit]
Description=Luisa Valentini Django Site
After=network.target

[Service]
User=deploy
Group=deploy
WorkingDirectory=/opt/luisavalentini/app
Environment="PATH=/opt/luisavalentini/venv/bin:/usr/bin"
Environment="SECRET_KEY=CHANGE_ME"
Environment="DEBUG=False"
Environment="ALLOWED_HOSTS=luisavalentini.it,www.luisavalentini.it"
Environment="CSRF_TRUSTED_ORIGINS=https://luisavalentini.it,https://www.luisavalentini.it"
Environment="DATA_DIR=/opt/luisavalentini/data"
Environment="MEDIA_ROOT=/opt/luisavalentini/data/media"
Environment="CONTACT_EMAIL=mauro.doglio@gmail.com"
ExecStart=/opt/luisavalentini/venv/bin/gunicorn luisavalentini.wsgi:application --bind 127.0.0.1:8000 --workers 2
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable luisavalentini

echo "=== Configuring nginx ==="
cat > /etc/nginx/sites-available/luisavalentini << EOF
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;

    client_max_body_size 10M;

    location /static/ {
        alias /opt/luisavalentini/app/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /opt/luisavalentini/data/media/;
        expires 30d;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

ln -sf /etc/nginx/sites-available/luisavalentini /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl reload nginx

echo "=== Setup complete! ==="
echo ""
echo "Next steps:"
echo "1. Update SECRET_KEY in /etc/systemd/system/luisavalentini.service"
echo "2. Clone or deploy the app to /opt/luisavalentini/app"
echo "3. Run: systemctl start luisavalentini"
echo "4. Point DNS to this server's IP"
echo "5. Run: certbot --nginx -d $DOMAIN -d www.$DOMAIN"
