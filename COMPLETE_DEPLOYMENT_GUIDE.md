# Complete Deployment Guide - NextBloom

## Overview
This guide covers:
1. Pushing code to GitHub
2. Setting up Linux server
3. Configuring Jenkins for CI/CD
4. Deploying the application

## Part 1: Push Code to GitHub

### Step 1: Authenticate with GitHub

You need to authenticate with GitHub to push code. Choose one method:

#### Method A: Personal Access Token (Easiest)

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Name: "NextBloom Deployment"
4. Select scope: `repo`
5. Generate and copy the token

#### Method B: SSH Key (More Secure)

1. Generate SSH key:
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```

2. Add to GitHub:
   - Copy: `cat ~/.ssh/id_ed25519.pub`
   - GitHub → Settings → SSH and GPG keys → New SSH key
   - Paste and save

### Step 2: Push Code

```bash
# If using token:
git remote set-url origin https://YOUR_TOKEN@github.com/punishermortal/ecomerce_web.git
git push origin main

# If using SSH:
git remote set-url origin git@github.com:punishermortal/ecomerce_web.git
git push origin main
```

## Part 2: Server Setup

### Step 1: Connect to Server

```bash
ssh xyzxtz@21.2.23.24
# Password: abcdef
```

### Step 2: Run Setup Script

```bash
# Download setup script
curl -o setup_server.sh https://raw.githubusercontent.com/punishermortal/ecomerce_web/main/setup_server.sh
chmod +x setup_server.sh
./setup_server.sh
```

Or run commands manually (see `server_setup_commands.sh`)

### Step 3: Clone Repository

```bash
sudo mkdir -p /var/www/nextbloom
sudo chown xyzxtz:xyzxtz /var/www/nextbloom
cd /var/www/nextbloom
git clone https://github.com/punishermortal/ecomerce_web.git .
```

### Step 4: Configure Backend

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
SECRET_KEY=generate-a-secret-key-here
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

### Step 5: Configure Frontend

```bash
cd /var/www/nextbloom/frontend

# Install dependencies
npm install

# Create .env.local
nano .env.local
```

Add to `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://21.2.23.24/api
```

```bash
# Build frontend
npm run build
```

### Step 6: Create Systemd Service

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
sudo systemctl status nextbloom
```

### Step 7: Configure Nginx

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

    client_max_body_size 100M;

    # Frontend
    location / {
        root /var/www/nextbloom/frontend/out;
        try_files $uri $uri/ /index.html;
        index index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }

    # Admin
    location /admin {
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

```bash
sudo ln -s /etc/nginx/sites-available/nextbloom /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
```

### Step 8: Configure Firewall

```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 8080/tcp  # Jenkins
sudo ufw enable
```

## Part 3: Jenkins Setup

### Step 1: Access Jenkins

```bash
# Get initial password
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

Open browser: `http://21.2.23.24:8080`

### Step 2: Install Plugins

1. Install recommended plugins
2. Create admin user
3. Install additional plugins:
   - Git plugin
   - Pipeline plugin
   - SSH plugin
   - NodeJS plugin

### Step 3: Configure SSH Access

```bash
# Generate SSH key for Jenkins
sudo -u jenkins ssh-keygen -t rsa -b 4096 -C "jenkins@nextbloom"
# Press Enter for all prompts

# Add Jenkins public key to authorized_keys
sudo -u jenkins cat /var/lib/jenkins/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys

# Test SSH connection
sudo -u jenkins ssh xyzxtz@localhost
```

### Step 4: Configure Sudo Access for Jenkins

```bash
sudo visudo
```

Add this line:
```
jenkins ALL=(ALL) NOPASSWD: /bin/systemctl restart nextbloom, /bin/systemctl restart nginx, /bin/systemctl status nextbloom
```

### Step 5: Configure Node.js in Jenkins

1. Go to **Manage Jenkins** → **Global Tool Configuration**
2. Find **NodeJS**
3. Add NodeJS installation:
   - **Name**: NodeJS-18
   - **Version**: 18.x
   - **Install automatically**: Yes
4. Save

### Step 6: Create Pipeline Job

1. Click **New Item**
2. Name: `nextbloom-deploy`
3. Select **Pipeline**
4. Click **OK**

### Step 7: Configure Pipeline

1. **Pipeline Definition**: Pipeline script from SCM
2. **SCM**: Git
3. **Repository URL**: `https://github.com/punishermortal/ecomerce_web.git`
4. **Credentials**: None (if public) or add credentials
5. **Branch**: `*/main`
6. **Script Path**: `Jenkinsfile`
7. Click **Save**

### Step 8: Configure Build Triggers

1. Check **GitHub hook trigger for GITScm polling**
2. Or use **Poll SCM** with: `H/5 * * * *` (every 5 minutes)

### Step 9: Test Pipeline

1. Click **Build Now**
2. Check console output
3. Verify deployment

## Part 4: GitHub Webhook (Optional)

### Setup Webhook for Automatic Deployment

1. Go to GitHub repository
2. Settings → Webhooks → Add webhook
3. **Payload URL**: `http://21.2.23.24:8080/github-webhook/`
4. **Content type**: application/json
5. **Events**: Just the push event
6. Click **Add webhook**

## Part 5: Verify Deployment

### Check Services

```bash
# Check Django service
sudo systemctl status nextbloom

# Check Nginx
sudo systemctl status nginx

# Check Jenkins
sudo systemctl status jenkins
```

### Test Application

1. Frontend: http://21.2.23.24
2. Backend API: http://21.2.23.24/api/products/
3. Admin: http://21.2.23.24/admin
4. Jenkins: http://21.2.23.24:8080

## Troubleshooting

### Git Push Issues

- **403 Error**: Need to authenticate with GitHub
- **Solution**: Use Personal Access Token or SSH key

### Service Not Starting

- Check logs: `sudo journalctl -u nextbloom -f`
- Check database connection
- Verify environment variables

### Jenkins Pipeline Fails

- Check Jenkins logs: `sudo tail -f /var/log/jenkins/jenkins.log`
- Verify SSH access
- Check sudo permissions
- Verify paths in Jenkinsfile

### Nginx 502 Error

- Check Django service is running
- Verify upstream configuration
- Check firewall settings

## Security Recommendations

1. **Change Default Passwords**:
   - PostgreSQL password
   - Django SECRET_KEY
   - Server password (use SSH keys)

2. **Setup SSL**:
   ```bash
   sudo apt install certbot python3-certbot-nginx -y
   sudo certbot --nginx -d yourdomain.com
   ```

3. **Firewall**:
   - Only open necessary ports
   - Use fail2ban for SSH protection

4. **Backup**:
   - Setup database backups
   - Backup media files
   - Backup configuration files

## Maintenance

### Manual Deployment

```bash
cd /var/www/nextbloom
./deploy.sh
```

### Update Code

```bash
cd /var/www/nextbloom
git pull origin main
./deploy.sh
```

### View Logs

```bash
# Django logs
sudo journalctl -u nextbloom -f

# Nginx logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log

# Jenkins logs
sudo tail -f /var/log/jenkins/jenkins.log
```

## Support

For issues:
1. Check logs
2. Verify services are running
3. Check Jenkins pipeline console
4. Verify GitHub webhook (if configured)

## Next Steps

1. ✅ Push code to GitHub
2. ✅ Setup server
3. ✅ Configure Jenkins
4. ✅ Test deployment
5. ⬜ Setup SSL certificate
6. ⬜ Configure domain name
7. ⬜ Setup monitoring
8. ⬜ Configure backups

