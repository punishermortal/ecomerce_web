# 🚀 NextBloom Deployment - Start Here

## Quick Start Guide

### Step 1: Push Code to GitHub ⚠️ IMPORTANT

**Issue**: You need to authenticate with GitHub first!

**Solution**: Use Personal Access Token

1. **Generate Token**:
   - Go to: https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Name: "NextBloom"
   - Select: `repo` scope
   - Click "Generate token"
   - **Copy the token** (you'll only see it once!)

2. **Push Code**:
   ```bash
   # In PowerShell or Command Prompt
   git remote set-url origin https://YOUR_TOKEN@github.com/punishermortal/ecomerce_web.git
   git push origin main
   ```

   Replace `YOUR_TOKEN` with your actual token.

### Step 2: Setup Server

1. **Connect to server**:
   ```bash
   ssh xyzxtz@21.2.23.24
   # Password: abcdef
   ```

2. **Run setup script**:
   ```bash
   curl -o setup.sh https://raw.githubusercontent.com/punishermortal/ecomerce_web/main/server_setup_commands.sh
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Clone repository**:
   ```bash
   sudo mkdir -p /var/www/nextbloom
   sudo chown xyzxtz:xyzxtz /var/www/nextbloom
   cd /var/www/nextbloom
   git clone https://github.com/punishermortal/ecomerce_web.git .
   ```

### Step 3: Configure Application

1. **Backend**:
   ```bash
   cd /var/www/nextbloom/backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   nano .env  # Add your configuration
   python manage.py migrate
   python manage.py collectstatic --noinput
   python manage.py createsuperuser
   ```

2. **Frontend**:
   ```bash
   cd /var/www/nextbloom/frontend
   npm install
   echo "NEXT_PUBLIC_API_URL=http://21.2.23.24/api" > .env.local
   npm run build
   ```

### Step 4: Setup Services

1. **Systemd Service** (see `DEPLOYMENT.md`)
2. **Nginx Configuration** (see `DEPLOYMENT.md`)
3. **Jenkins Setup** (see `JENKINS_SETUP.md`)

### Step 5: Test

- Application: http://21.2.23.24
- API: http://21.2.23.24/api/products/
- Admin: http://21.2.23.24/admin
- Jenkins: http://21.2.23.24:8080

## Documentation

- **PUSH_TO_GITHUB.md** - How to push code to GitHub
- **COMPLETE_DEPLOYMENT_GUIDE.md** - Complete deployment guide
- **DEPLOYMENT.md** - Detailed server setup
- **JENKINS_SETUP.md** - Jenkins CI/CD setup
- **SERVER_SETUP.md** - Quick server setup reference

## Need Help?

1. Check the documentation files
2. Review error logs
3. Verify services are running
4. Check Jenkins pipeline console

## Important Notes

⚠️ **Security**:
- Change default passwords
- Use SSH keys instead of passwords
- Set up SSL certificate
- Never commit .env files

⚠️ **Database**:
- Use PostgreSQL in production
- Backup database regularly
- Test migrations in staging

⚠️ **Jenkins**:
- Configure SSH access
- Setup sudo permissions
- Test pipeline manually first

## Next Steps After Deployment

1. ✅ Push code to GitHub
2. ✅ Setup server
3. ✅ Configure Jenkins
4. ⬜ Setup SSL certificate
5. ⬜ Configure domain name
6. ⬜ Setup monitoring
7. ⬜ Configure backups

