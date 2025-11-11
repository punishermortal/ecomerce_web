# GitHub Push & Deployment Steps

## 🚨 IMPORTANT: Fix GitHub Authentication First!

### Step 1: Generate GitHub Personal Access Token

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Name: "NextBloom Deployment"
4. Select scope: `repo` (Full control)
5. Click "Generate token"
6. **COPY THE TOKEN** (you'll only see it once!)

### Step 2: Push Code to GitHub

```bash
# Replace YOUR_TOKEN with your actual token
git remote set-url origin https://YOUR_TOKEN@github.com/punishermortal/ecomerce_web.git
git push origin main
```

**OR** use GitHub Desktop or GitHub CLI to authenticate.

## 📦 Code is Ready

All code is committed and ready to push. Files include:
- ✅ Backend (Django + DRF)
- ✅ Frontend (Next.js)
- ✅ Jenkins pipeline (Jenkinsfile)
- ✅ Deployment scripts
- ✅ Documentation

## 🖥️ Server Setup (After GitHub Push)

### Quick Setup Commands

```bash
# 1. Connect to server
ssh xyzxtz@21.2.23.24
# Password: abcdef

# 2. Run setup (one command)
curl -o setup.sh https://raw.githubusercontent.com/punishermortal/ecomerce_web/main/server_setup_commands.sh && chmod +x setup.sh && ./setup.sh

# 3. Clone repository
sudo mkdir -p /var/www/nextbloom
sudo chown xyzxtz:xyzxtz /var/www/nextbloom
cd /var/www/nextbloom
git clone https://github.com/punishermortal/ecomerce_web.git .

# 4. Configure backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
nano .env  # Add your configuration
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser

# 5. Configure frontend
cd ../frontend
npm install
echo "NEXT_PUBLIC_API_URL=http://21.2.23.24/api" > .env.local
npm run build

# 6. Setup services (see DEPLOYMENT.md for details)
# - Systemd service
# - Nginx configuration
# - Jenkins setup
```

## 🔄 Jenkins CI/CD Setup

### After Server Setup:

1. **Access Jenkins**: http://21.2.23.24:8080
2. **Get password**: `sudo cat /var/lib/jenkins/secrets/initialAdminPassword`
3. **Install plugins**: Git, Pipeline, SSH, NodeJS
4. **Create pipeline**: 
   - Name: `nextbloom-deploy`
   - Repository: https://github.com/punishermortal/ecomerce_web.git
   - Branch: `*/main`
   - Script: `Jenkinsfile`
5. **Configure SSH**: Setup SSH key for Jenkins user
6. **Configure sudo**: Allow Jenkins to restart services

### Jenkins will automatically:
- ✅ Pull latest code from GitHub
- ✅ Install backend dependencies
- ✅ Run migrations
- ✅ Build frontend
- ✅ Restart services
- ✅ Health check

## 📋 Complete Checklist

### GitHub
- [ ] Generate Personal Access Token
- [ ] Push code to GitHub
- [ ] Verify code is on GitHub

### Server
- [ ] Connect to server (ssh xyzxtz@21.2.23.24)
- [ ] Run setup script
- [ ] Install software (Python, Node.js, PostgreSQL, Nginx, Jenkins)
- [ ] Setup PostgreSQL database
- [ ] Clone repository
- [ ] Configure backend (.env)
- [ ] Configure frontend (.env.local)
- [ ] Run migrations
- [ ] Build frontend
- [ ] Setup systemd service
- [ ] Setup Nginx
- [ ] Configure firewall

### Jenkins
- [ ] Install Jenkins
- [ ] Install plugins
- [ ] Setup SSH access
- [ ] Configure sudo permissions
- [ ] Create pipeline job
- [ ] Test pipeline
- [ ] Configure webhook (optional)

### Testing
- [ ] Test application: http://21.2.23.24
- [ ] Test API: http://21.2.23.24/api/products/
- [ ] Test admin: http://21.2.23.24/admin
- [ ] Test Jenkins: http://21.2.23.24:8080
- [ ] Test automatic deployment

## 🎯 What Happens Next?

### After GitHub Push:
1. Code is on GitHub ✅
2. Server can clone repository ✅
3. Jenkins can access repository ✅

### After Server Setup:
1. Application is deployed ✅
2. Services are running ✅
3. Application is accessible ✅

### After Jenkins Setup:
1. Automatic deployment on git push ✅
2. Health checks ✅
3. Service restarts ✅

## 📚 Documentation Files

- **START_HERE.md** - Quick start guide
- **GIT_PUSH_GUIDE.md** - GitHub authentication guide
- **COMPLETE_DEPLOYMENT_GUIDE.md** - Complete deployment guide
- **DEPLOYMENT.md** - Detailed server setup
- **JENKINS_SETUP.md** - Jenkins configuration
- **SERVER_SETUP.md** - Quick server setup reference
- **DEPLOYMENT_SUMMARY.md** - Deployment summary

## 🔐 Security Reminders

⚠️ **IMPORTANT**:
1. Change default passwords
2. Use SSH keys instead of passwords
3. Never commit .env files
4. Set up SSL certificate
5. Configure firewall properly
6. Use strong SECRET_KEY

## 🆘 Need Help?

1. **Git Push Issues**: See `GIT_PUSH_GUIDE.md`
2. **Server Setup Issues**: See `SERVER_SETUP.md`
3. **Jenkins Issues**: See `JENKINS_SETUP.md`
4. **Deployment Issues**: See `DEPLOYMENT.md`

## ✅ Success!

Once everything is set up:
- ✅ Code is on GitHub
- ✅ Server is configured
- ✅ Application is deployed
- ✅ Jenkins is working
- ✅ Automatic deployment is active

**Every time you push to GitHub, Jenkins will automatically deploy!** 🎉

