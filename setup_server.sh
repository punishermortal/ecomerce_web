#!/bin/bash

# NextBloom Server Initial Setup Script
# Run this script on a fresh Ubuntu/Debian server

set -e

echo "=========================================="
echo "NextBloom Server Setup Script"
echo "=========================================="

# Update system
echo "Updating system..."
sudo apt update && sudo apt upgrade -y

# Install Python and pip
echo "Installing Python..."
sudo apt install python3 python3-pip python3-venv -y

# Install Node.js
echo "Installing Node.js..."
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Install PostgreSQL
echo "Installing PostgreSQL..."
sudo apt install postgresql postgresql-contrib -y

# Install Nginx
echo "Installing Nginx..."
sudo apt install nginx -y

# Install Git
echo "Installing Git..."
sudo apt install git -y

# Install Java (required for Jenkins)
echo "Installing Java..."
sudo apt install openjdk-17-jdk -y

# Install Jenkins
echo "Installing Jenkins..."
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee \
  /usr/share/keyrings/jenkins-keyring.asc > /dev/null
echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt-get update
sudo apt-get install jenkins -y

# Setup PostgreSQL
echo "Setting up PostgreSQL..."
sudo -u postgres psql <<EOF
CREATE DATABASE nextbloom;
CREATE USER nextbloom_user WITH PASSWORD 'change_this_password';
GRANT ALL PRIVILEGES ON DATABASE nextbloom TO nextbloom_user;
\q
EOF

# Create application directory
echo "Creating application directory..."
sudo mkdir -p /var/www/nextbloom
sudo chown $USER:$USER /var/www/nextbloom

# Setup firewall
echo "Configuring firewall..."
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 8080/tcp
sudo ufw --force enable

# Install Gunicorn
echo "Installing Gunicorn..."
pip3 install gunicorn

echo "=========================================="
echo "Server setup completed!"
echo "=========================================="
echo "Next steps:"
echo "1. Clone repository: cd /var/www/nextbloom && git clone https://github.com/punishermortal/ecomerce_web.git ."
echo "2. Follow DEPLOYMENT.md for further setup"
echo "3. Get Jenkins password: sudo cat /var/lib/jenkins/secrets/initialAdminPassword"
echo "4. Access Jenkins: http://$(hostname -I | awk '{print $1}'):8080"

