#!/bin/bash

# NextBloom Server Setup Commands
# Run these commands on your Linux server (21.2.23.24)

echo "=========================================="
echo "NextBloom Server Setup"
echo "=========================================="

# 1. Update system
echo "1. Updating system..."
sudo apt update && sudo apt upgrade -y

# 2. Install Python
echo "2. Installing Python..."
sudo apt install python3 python3-pip python3-venv -y

# 3. Install Node.js
echo "3. Installing Node.js..."
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# 4. Install PostgreSQL
echo "4. Installing PostgreSQL..."
sudo apt install postgresql postgresql-contrib -y

# 5. Install Nginx
echo "5. Installing Nginx..."
sudo apt install nginx -y

# 6. Install Git
echo "6. Installing Git..."
sudo apt install git -y

# 7. Install Java
echo "7. Installing Java..."
sudo apt install openjdk-17-jdk -y

# 8. Install Jenkins
echo "8. Installing Jenkins..."
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee /usr/share/keyrings/jenkins-keyring.asc > /dev/null
echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/ | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt-get update
sudo apt-get install jenkins -y

# 9. Install Gunicorn
echo "9. Installing Gunicorn..."
pip3 install gunicorn

# 10. Setup PostgreSQL Database
echo "10. Setting up database..."
sudo -u postgres psql <<EOF
CREATE DATABASE nextbloom;
CREATE USER nextbloom_user WITH PASSWORD 'change_this_password';
GRANT ALL PRIVILEGES ON DATABASE nextbloom TO nextbloom_user;
\q
EOF

# 11. Create application directory
echo "11. Creating application directory..."
sudo mkdir -p /var/www/nextbloom
sudo chown xyzxtz:xyzxtz /var/www/nextbloom

# 12. Clone repository
echo "12. Cloning repository..."
cd /var/www/nextbloom
git clone https://github.com/punishermortal/ecomerce_web.git .

# 13. Setup backend
echo "13. Setting up backend..."
cd /var/www/nextbloom/backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 14. Setup frontend
echo "14. Setting up frontend..."
cd /var/www/nextbloom/frontend
npm install

# 15. Configure firewall
echo "15. Configuring firewall..."
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 8080/tcp
sudo ufw --force enable

# 16. Make deploy script executable
echo "16. Making deploy script executable..."
chmod +x /var/www/nextbloom/deploy.sh

echo "=========================================="
echo "Server setup completed!"
echo "=========================================="
echo "Next steps:"
echo "1. Configure backend .env file: cd /var/www/nextbloom/backend && nano .env"
echo "2. Configure frontend .env.local: cd /var/www/nextbloom/frontend && nano .env.local"
echo "3. Run migrations: cd /var/www/nextbloom/backend && source venv/bin/activate && python manage.py migrate"
echo "4. Create superuser: python manage.py createsuperuser"
echo "5. Build frontend: cd /var/www/nextbloom/frontend && npm run build"
echo "6. Setup systemd service: sudo nano /etc/systemd/system/nextbloom.service"
echo "7. Setup Nginx: sudo nano /etc/nginx/sites-available/nextbloom"
echo "8. Get Jenkins password: sudo cat /var/lib/jenkins/secrets/initialAdminPassword"
echo "9. Access Jenkins: http://21.2.23.24:8080"

