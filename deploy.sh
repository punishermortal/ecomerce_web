#!/bin/bash

# NextBloom Deployment Script
# This script automates the deployment process

set -e  # Exit on error

PROJECT_DIR="/var/www/nextbloom"
BACKEND_DIR="${PROJECT_DIR}/backend"
FRONTEND_DIR="${PROJECT_DIR}/frontend"
VENV_PATH="${BACKEND_DIR}/venv"

echo "=========================================="
echo "NextBloom Deployment Script"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    print_error "Please do not run as root. Use a user with sudo privileges."
    exit 1
fi

# Navigate to project directory
cd $PROJECT_DIR || exit 1

print_status "Pulling latest code from GitHub..."
git pull origin main

# Backend Setup
print_status "Setting up backend..."
cd $BACKEND_DIR

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    print_status "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
print_status "Installing backend dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Run migrations
print_status "Running database migrations..."
python manage.py migrate --noinput

# Collect static files
print_status "Collecting static files..."
python manage.py collectstatic --noinput

# Frontend Setup
print_status "Setting up frontend..."
cd $FRONTEND_DIR

# Install dependencies
print_status "Installing frontend dependencies..."
npm install

# Build frontend
print_status "Building frontend..."
npm run build

# Restart services
print_status "Restarting services..."
sudo systemctl restart nextbloom || print_warning "Failed to restart nextbloom service"
sudo systemctl restart nextbloom-frontend || print_warning "Failed to restart nextbloom-frontend service (may not exist in dev)"
sudo systemctl restart nginx || print_warning "Failed to restart nginx"
sleep 3

# Wait for service to start
print_status "Waiting for services to start..."
sleep 5

# Health check
print_status "Performing health check..."
if curl -f http://localhost:8000/api/products/ > /dev/null 2>&1; then
    print_status "Health check passed!"
else
    print_error "Health check failed! Please check the logs."
    sudo journalctl -u nextbloom -n 50
    exit 1
fi

print_status "=========================================="
print_status "Deployment completed successfully!"
print_status "=========================================="

