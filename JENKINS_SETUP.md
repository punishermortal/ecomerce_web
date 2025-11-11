# Jenkins CI/CD Setup Guide

## Overview

Jenkins is configured to automatically deploy the NextBloom application when code is pushed to the GitHub repository.

## Jenkins Installation

### 1. Access Jenkins

After installation, access Jenkins at:
```
http://21.2.23.24:8080
```

### 2. Get Initial Password

```bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

### 3. Install Plugins

Install the following plugins:
- Git plugin
- Pipeline plugin
- SSH plugin
- NodeJS plugin
- Blue Ocean (optional, for better UI)

## Jenkins Configuration

### 1. Configure SSH Access

1. Go to **Manage Jenkins** → **Configure System**
2. Scroll to **SSH Servers**
3. Add SSH server:
   - **Hostname**: localhost
   - **Port**: 22
   - **Username**: xyzxtz
   - **Credentials**: Add SSH private key

### 2. Generate SSH Key for Jenkins

```bash
sudo -u jenkins ssh-keygen -t rsa -b 4096 -C "jenkins@nextbloom"
sudo -u jenkins cat /var/lib/jenkins/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
```

### 3. Configure Node.js

1. Go to **Manage Jenkins** → **Global Tool Configuration**
2. Add Node.js installation:
   - **Name**: NodeJS-18
   - **Version**: 18.x
   - **Install automatically**: Yes

## Create Jenkins Pipeline

### 1. Create New Pipeline Job

1. Click **New Item**
2. Enter name: `nextbloom-deploy`
3. Select **Pipeline**
4. Click **OK**

### 2. Configure Pipeline

1. **Pipeline Definition**: Pipeline script from SCM
2. **SCM**: Git
3. **Repository URL**: `https://github.com/punishermortal/ecomerce_web.git`
4. **Credentials**: None (public repo) or add credentials for private repo
5. **Branch**: `*/main`
6. **Script Path**: `Jenkinsfile`

### 3. Configure Build Triggers

1. Check **GitHub hook trigger for GITScm polling**
2. Or use **Poll SCM** with schedule: `H/5 * * * *` (every 5 minutes)

## GitHub Webhook Setup (Optional)

### 1. Create Webhook in GitHub

1. Go to repository settings
2. Click **Webhooks** → **Add webhook**
3. **Payload URL**: `http://21.2.23.24:8080/github-webhook/`
4. **Content type**: application/json
5. **Events**: Just the push event
6. Click **Add webhook**

### 2. Configure Jenkins for Webhook

1. Go to **Manage Jenkins** → **Configure System**
2. Check **GitHub** section
3. Add GitHub server
4. Configure webhook URL

## Jenkinsfile Configuration

The Jenkinsfile is located in the repository root and contains:

1. **Checkout**: Clones code from GitHub
2. **Backend Setup**: Installs Python dependencies
3. **Migrations**: Runs database migrations
4. **Frontend Setup**: Installs Node.js dependencies
5. **Frontend Build**: Builds Next.js application
6. **Restart Services**: Restarts Django and Nginx
7. **Health Check**: Verifies deployment success

## Manual Pipeline Execution

1. Go to Jenkins dashboard
2. Click on `nextbloom-deploy`
3. Click **Build Now**
4. View build progress in console output

## Troubleshooting

### Pipeline Fails at Checkout

- Verify repository URL is correct
- Check GitHub credentials (if private repo)
- Verify Jenkins has internet access

### Pipeline Fails at Backend Setup

- Check Python version (should be 3.9+)
- Verify virtual environment creation
- Check requirements.txt exists

### Pipeline Fails at Frontend Build

- Check Node.js version (should be 18+)
- Verify npm install completes
- Check for build errors in console

### Services Not Restarting

- Verify user has sudo privileges
- Check systemd service name
- Verify service files exist

### Health Check Fails

- Check Django service is running
- Verify database connection
- Check API endpoint is accessible

## Security Considerations

### 1. Jenkins Security

1. Enable authentication
2. Create user accounts
3. Restrict access to pipeline
4. Use credentials for sensitive data

### 2. SSH Key Security

- Use SSH keys instead of passwords
- Restrict key permissions
- Use dedicated deployment user

### 3. Environment Variables

- Store secrets in Jenkins credentials
- Use .env files for configuration
- Never commit secrets to repository

## Monitoring

### 1. Build History

- View build history in Jenkins
- Check build status and duration
- Review console output for errors

### 2. Notifications

Configure notifications for:
- Build failures
- Deployment success
- Service restarts

### 3. Logs

- Jenkins logs: `/var/log/jenkins/jenkins.log`
- Application logs: `sudo journalctl -u nextbloom`
- Nginx logs: `/var/log/nginx/`

## Best Practices

1. **Test Before Deploy**: Run tests in pipeline
2. **Rollback Plan**: Keep previous version for rollback
3. **Backup**: Backup database before deployment
4. **Monitoring**: Monitor application after deployment
5. **Notifications**: Notify team of deployment status

## Advanced Configuration

### 1. Multi-Stage Deployment

- Add staging environment
- Test in staging before production
- Use different branches for environments

### 2. Blue-Green Deployment

- Deploy to separate directory
- Switch after verification
- Keep previous version for rollback

### 3. Database Migrations

- Run migrations separately
- Backup before migrations
- Test migrations in staging

## Support

For issues:
1. Check Jenkins console output
2. Review application logs
3. Verify service status
4. Check network connectivity

## Useful Commands

```bash
# Check Jenkins status
sudo systemctl status jenkins

# Restart Jenkins
sudo systemctl restart jenkins

# View Jenkins logs
sudo tail -f /var/log/jenkins/jenkins.log

# Check pipeline status
curl http://localhost:8080/job/nextbloom-deploy/lastBuild/api/json
```

