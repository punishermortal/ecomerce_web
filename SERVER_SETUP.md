# Server Setup Guide - Quick Reference

## Server Details
- **IP**: 21.2.23.24
- **Username**: xyzxtz
- **Password**: abcdef

## Quick Setup Commands

### 1. Connect to Server
```bash
ssh xyzxtz@21.2.23.24
```

### 2. Run Setup Script
```bash
# Copy and paste this entire block
curl -o setup.sh https://raw.githubusercontent.com/punishermortal/ecomerce_web/main/server_setup_commands.sh
chmod +x setup.sh
./setup.sh
```

### 3. Manual Setup (If script fails)

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install software
sudo apt install python3 python3-pip python3-venv nodejs postgresql nginx git openjdk-17-jdk -y

# Install Node.js 18
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Install Jenkins
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee /usr/share/keyrings/jenkins-keyring.asc > /dev/null
echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/ | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt-get update
sudo apt-get install jenkins -y

# Install Gunicorn
pip3 install gunicorn

# Setup database
sudo -u postgres psql
# In PostgreSQL:
CREATE DATABASE nextbloom;
CREATE USER nextbloom_user WITH PASSWORD 'change_this_password';
GRANT ALL PRIVILEGES ON DATABASE nextbloom TO nextbloom_user;
\q

# Create app directory
sudo mkdir -p /var/www/nextbloom
sudo chown xyzxtz:xyzxtz /var/www/nextbloom
cd /var/www/nextbloom
git clone https://github.com/punishermortal/ecomerce_web.git .
```

### 4. Configure Backend

```bash
cd /var/www/nextbloom/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create .env file
nano .env
```

Add to `.env`:
```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=21.2.23.24
DATABASE_URL=postgresql://nextbloom_user:change_this_password@localhost:5432/nextbloom
RAZORPAY_KEY_ID=your_key
RAZORPAY_KEY_SECRET=your_secret
DELHIVERY_API_TOKEN=your_token
DELHIVERY_ENABLED=True
```

```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### 5. Configure Frontend

```bash
cd /var/www/nextbloom/frontend
npm install

# Create .env.local
echo "NEXT_PUBLIC_API_URL=http://21.2.23.24/api" > .env.local

npm run build
```

### 6. Setup Systemd Service

```bash
sudo nano /etc/systemd/system/nextbloom.service
```

Paste:
```ini
[Unit]
Description=NextBloom Django Application
After=network.target

[Service]
User=xyzxtz
Group=xyzxtz
WorkingDirectory=/var/www/nextbloom/backend
Environment="PATH=/var/www/nextbloom/backend/venv/bin"
ExecStart=/var/www/nextbloom/backend/venv/bin/gunicorn nextbloom.wsgi:application --bind 127.0.0.1:8000 --workers 3
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable nextbloom
sudo systemctl start nextbloom
```

### 7. Setup Nginx

```bash
sudo nano /etc/nginx/sites-available/nextbloom
```

Paste:
```nginx
upstream django {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name 21.2.23.24;

    location / {
        root /var/www/nextbloom/frontend/out;
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /admin {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /media {
        alias /var/www/nextbloom/backend/media;
    }

    location /static {
        alias /var/www/nextbloom/backend/staticfiles;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/nextbloom /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
```

### 8. Setup Firewall

```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 8080/tcp
sudo ufw enable
```

### 9. Setup Jenkins Sudo Access

```bash
sudo visudo
# Add this line:
jenkins ALL=(ALL) NOPASSWD: /bin/systemctl restart nextbloom, /bin/systemctl restart nginx
```

### 10. Access Jenkins

```bash
# Get password
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

Open: http://21.2.23.24:8080

## Jenkins Configuration

1. Install recommended plugins
2. Create admin user
3. Install: Git, Pipeline, SSH, NodeJS plugins
4. Create pipeline job:
   - Name: `nextbloom-deploy`
   - Pipeline from SCM
   - Repository: https://github.com/punishermortal/ecomerce_web.git
   - Branch: `*/main`
   - Script: `Jenkinsfile`

## Test

1. Application: http://21.2.23.24
2. API: http://21.2.23.24/api/products/
3. Admin: http://21.2.23.24/admin
4. Jenkins: http://21.2.23.24:8080

## Troubleshooting

```bash
# Check services
sudo systemctl status nextbloom
sudo systemctl status nginx
sudo systemctl status jenkins

# View logs
sudo journalctl -u nextbloom -f
sudo tail -f /var/log/nginx/error.log
```

