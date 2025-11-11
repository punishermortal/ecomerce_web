# NextBloom Deployment Guide

## Server Information
- **Server IP**: 21.2.23.24
- **Username**: xyzxtz
- **Repository**: https://github.com/punishermortal/ecomerce_web.git

## Prerequisites

### Server Setup
1. Ubuntu/Debian Linux server
2. Python 3.9+
3. Node.js 18+
4. PostgreSQL or MySQL (recommended for production)
5. Nginx
6. Jenkins
7. Git

## Initial Server Setup

### 1. Connect to Server

```bash
ssh xyzxtz@21.2.23.24
```

### 2. Install Required Software

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip python3-venv -y

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# Install Nginx
sudo apt install nginx -y

# Install Git
sudo apt install git -y

# Install Jenkins
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee \
  /usr/share/keyrings/jenkins-keyring.asc > /dev/null
echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt-get update
sudo apt-get install jenkins -y

# Install Java (required for Jenkins)
sudo apt install openjdk-17-jdk -y
```

### 3. Setup PostgreSQL Database

```bash
sudo -u postgres psql

# In PostgreSQL console:
CREATE DATABASE nextbloom;
CREATE USER nextbloom_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE nextbloom TO nextbloom_user;
\q
```

### 4. Create Application Directory

```bash
sudo mkdir -p /var/www/nextbloom
sudo chown xyzxtz:xyzxtz /var/www/nextbloom
cd /var/www/nextbloom
```

### 5. Clone Repository

```bash
git clone https://github.com/punishermortal/ecomerce_web.git .
```

## Backend Setup

### 1. Setup Python Virtual Environment

```bash
cd /var/www/nextbloom/backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Configure Environment Variables

```bash
cd /var/www/nextbloom/backend
nano .env
```

Add the following:

```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=21.2.23.24,yourdomain.com
DATABASE_URL=postgresql://nextbloom_user:your_secure_password@localhost:5432/nextbloom

# Razorpay
RAZORPAY_KEY_ID=your_razorpay_key
RAZORPAY_KEY_SECRET=your_razorpay_secret

# Delhivery
DELHIVERY_API_TOKEN=your_delhivery_token
DELHIVERY_ENABLED=True
DELHIVERY_PICKUP_NAME=NextBloom
DELHIVERY_PICKUP_PHONE=+919876543210
DELHIVERY_PICKUP_ADDRESS=Your Address
DELHIVERY_PICKUP_CITY=Mumbai
DELHIVERY_PICKUP_STATE=Maharashtra
DELHIVERY_PICKUP_PINCODE=400001

# Email (for production)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@nextbloom.com
```

### 3. Run Migrations

```bash
cd /var/www/nextbloom/backend
source venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

## Frontend Setup

### 1. Install Dependencies

```bash
cd /var/www/nextbloom/frontend
npm install
```

### 2. Configure Environment Variables

```bash
cd /var/www/nextbloom/frontend
nano .env.local
```

Add:

```env
NEXT_PUBLIC_API_URL=http://21.2.23.24:8000/api
```

### 3. Build Frontend

```bash
cd /var/www/nextbloom/frontend
npm run build
```

## Nginx Configuration

### 1. Create Nginx Configuration

```bash
sudo nano /etc/nginx/sites-available/nextbloom
```

Add:

```nginx
# Backend API
upstream django {
    server 127.0.0.1:8000;
}

# Frontend
server {
    listen 80;
    server_name 21.2.23.24 yourdomain.com;

    # Frontend
    location / {
        root /var/www/nextbloom/frontend/out;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Media files
    location /media {
        alias /var/www/nextbloom/backend/media;
    }

    # Static files
    location /static {
        alias /var/www/nextbloom/backend/staticfiles;
    }
}
```

### 2. Enable Site

```bash
sudo ln -s /etc/nginx/sites-available/nextbloom /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Systemd Service for Django

### 1. Create Service File

```bash
sudo nano /etc/systemd/system/nextbloom.service
```

Add:

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

### 2. Start Service

```bash
sudo systemctl daemon-reload
sudo systemctl enable nextbloom
sudo systemctl start nextbloom
sudo systemctl status nextbloom
```

## Jenkins Setup

### 1. Access Jenkins

```bash
# Get Jenkins initial password
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

Open browser: `http://21.2.23.24:8080`

### 2. Install Required Plugins

- Git plugin
- Pipeline plugin
- SSH plugin
- NodeJS plugin

### 3. Configure Jenkins

1. Go to Manage Jenkins → Configure System
2. Add SSH server:
   - Host: localhost
   - Port: 22
   - Username: xyzxtz
   - Add SSH key

### 4. Create Pipeline Job

1. New Item → Pipeline
2. Name: nextbloom-deploy
3. Pipeline script from SCM
4. SCM: Git
5. Repository URL: https://github.com/punishermortal/ecomerce_web.git
6. Branch: main
7. Script Path: Jenkinsfile

## Jenkinsfile

The Jenkinsfile is already created in the repository root. It will:
1. Checkout code
2. Install backend dependencies
3. Run migrations
4. Build frontend
5. Restart services

## Manual Deployment Script

Create deployment script:

```bash
nano /var/www/nextbloom/deploy.sh
```

See `deploy.sh` file in repository.

## Security

### 1. Firewall

```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 8080/tcp  # Jenkins
sudo ufw enable
```

### 2. SSL Certificate (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.com
```

## Monitoring

### 1. Check Backend Logs

```bash
sudo journalctl -u nextbloom -f
```

### 2. Check Nginx Logs

```bash
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

## Troubleshooting

### Backend not starting
- Check logs: `sudo journalctl -u nextbloom -n 50`
- Check database connection
- Verify environment variables

### Frontend not loading
- Check Nginx configuration
- Verify build files exist
- Check Nginx logs

### Jenkins not deploying
- Check Jenkins logs
- Verify SSH access
- Check pipeline logs

## Backup

### Database Backup

```bash
# Create backup script
nano /var/www/nextbloom/backup.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/var/backups/nextbloom"
mkdir -p $BACKUP_DIR
pg_dump -U nextbloom_user nextbloom > $BACKUP_DIR/nextbloom_$(date +%Y%m%d_%H%M%S).sql
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
```

### Schedule Backup

```bash
crontab -e
# Add: 0 2 * * * /var/www/nextbloom/backup.sh
```

