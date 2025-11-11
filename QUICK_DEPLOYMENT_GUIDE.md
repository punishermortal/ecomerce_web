# Quick Deployment Guide - NextBloom

## Step 1: Push Code to GitHub ✅

Code is already pushed to: https://github.com/punishermortal/ecomerce_web.git

## Step 2: Server Setup

### Connect to Server

```bash
ssh xyzxtz@21.2.23.24
# Password: abcdef
```

### Run Initial Setup Script

```bash
# Download and run setup script
curl -o setup_server.sh https://raw.githubusercontent.com/punishermortal/ecomerce_web/main/setup_server.sh
chmod +x setup_server.sh
./setup_server.sh
```

Or manually:

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required software
sudo apt install python3 python3-pip python3-venv nodejs postgresql nginx git openjdk-17-jdk -y

# Install Node.js 18
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Install Jenkins
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee /usr/share/keyrings/jenkins-keyring.asc > /dev/null
echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/ | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt-get update
sudo apt-get install jenkins -y
```

## Step 3: Setup Database

```bash
sudo -u postgres psql

# In PostgreSQL console:
CREATE DATABASE nextbloom;
CREATE USER nextbloom_user WITH PASSWORD 'change_this_password';
GRANT ALL PRIVILEGES ON DATABASE nextbloom TO nextbloom_user;
\q
```

## Step 4: Clone Repository

```bash
sudo mkdir -p /var/www/nextbloom
sudo chown xyzxtz:xyzxtz /var/www/nextbloom
cd /var/www/nextbloom
git clone https://github.com/punishermortal/ecomerce_web.git .
```

## Step 5: Configure Backend

```bash
cd /var/www/nextbloom/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
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

RAZORPAY_KEY_ID=your_razorpay_key
RAZORPAY_KEY_SECRET=your_razorpay_secret

DELHIVERY_API_TOKEN=your_delhivery_token
DELHIVERY_ENABLED=True
DELHIVERY_PICKUP_NAME=NextBloom
DELHIVERY_PICKUP_PHONE=+919876543210
DELHIVERY_PICKUP_ADDRESS=Your Address
DELHIVERY_PICKUP_CITY=Mumbai
DELHIVERY_PICKUP_STATE=Maharashtra
DELHIVERY_PICKUP_PINCODE=400001
```

```bash
# Run migrations
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

## Step 6: Configure Frontend

```bash
cd /var/www/nextbloom/frontend

# Install dependencies
npm install

# Create .env.local
nano .env.local
```

Add to `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://21.2.23.24:8000/api
```

```bash
# Build frontend
npm run build
```

## Step 7: Setup Systemd Service

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

```bash
sudo systemctl daemon-reload
sudo systemctl enable nextbloom
sudo systemctl start nextbloom
```

## Step 8: Configure Nginx

```bash
sudo nano /etc/nginx/sites-available/nextbloom
```

Add:
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
sudo nginx -t
sudo systemctl restart nginx
```

## Step 9: Setup Jenkins

### Access Jenkins

```bash
# Get initial password
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

Open: http://21.2.23.24:8080

### Configure Jenkins

1. Install recommended plugins
2. Create admin user
3. Install additional plugins:
   - Git plugin
   - Pipeline plugin
   - SSH plugin
   - NodeJS plugin

### Setup SSH Access

```bash
# Generate SSH key for Jenkins
sudo -u jenkins ssh-keygen -t rsa -b 4096
sudo -u jenkins cat /var/lib/jenkins/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
```

### Create Pipeline Job

1. New Item → Pipeline
2. Name: `nextbloom-deploy`
3. Pipeline script from SCM
4. Repository: https://github.com/punishermortal/ecomerce_web.git
5. Branch: `*/main`
6. Script Path: `Jenkinsfile`

### Configure Sudo Access

```bash
# Allow Jenkins user to restart services
sudo visudo

# Add this line:
jenkins ALL=(ALL) NOPASSWD: /bin/systemctl restart nextbloom, /bin/systemctl restart nginx
```

## Step 10: Make Deploy Script Executable

```bash
chmod +x /var/www/nextbloom/deploy.sh
```

## Step 11: Test Deployment

1. Make a small change in code
2. Push to GitHub
3. Jenkins will automatically deploy
4. Check application at: http://21.2.23.24

## Troubleshooting

### Check Backend Status
```bash
sudo systemctl status nextbloom
sudo journalctl -u nextbloom -f
```

### Check Nginx Status
```bash
sudo systemctl status nginx
sudo nginx -t
```

### Check Jenkins Status
```bash
sudo systemctl status jenkins
```

### View Jenkins Logs
```bash
sudo tail -f /var/log/jenkins/jenkins.log
```

## Security Notes

⚠️ **IMPORTANT**: 
1. Change default PostgreSQL password
2. Change Django SECRET_KEY
3. Set up SSL certificate (Let's Encrypt)
4. Configure firewall properly
5. Use SSH keys instead of passwords
6. Never commit .env files to git

## Next Steps

1. Set up SSL certificate
2. Configure domain name
3. Set up monitoring
4. Configure backups
5. Set up email service

## Useful Commands

```bash
# Restart services
sudo systemctl restart nextbloom
sudo systemctl restart nginx

# View logs
sudo journalctl -u nextbloom -f
sudo tail -f /var/log/nginx/error.log

# Manual deployment
cd /var/www/nextbloom
./deploy.sh

# Check service status
sudo systemctl status nextbloom
sudo systemctl status nginx
sudo systemctl status jenkins
```

