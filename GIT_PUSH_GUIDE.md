# Git Push Guide - Fix Authentication Issue

## Problem
```
remote: Permission to punishermortal/ecomerce_web.git denied to rupashreeroy.
fatal: unable to access 'https://github.com/punishermortal/ecomerce_web.git/': The requested URL returned error: 403
```

## Solution: Use Personal Access Token

### Step 1: Generate Personal Access Token

1. Go to GitHub: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Give it a name: "NextBloom Deployment"
4. Select scope: `repo` (Full control of private repositories)
5. Click "Generate token"
6. **IMPORTANT**: Copy the token immediately (you won't see it again!)

### Step 2: Push Using Token

**Option A: Update Remote URL with Token**

```bash
# Replace YOUR_TOKEN with your actual token
git remote set-url origin https://YOUR_TOKEN@github.com/punishermortal/ecomerce_web.git
git push origin main
```

**Option B: Use Token as Password**

```bash
# When prompted for password, use the token
git push origin main
# Username: punishermortal
# Password: YOUR_TOKEN (not your GitHub password!)
```

**Option C: Use GitHub CLI**

```bash
# Install GitHub CLI first
# Then authenticate
gh auth login
# Then push
git push origin main
```

### Step 3: Verify Push

```bash
# Check remote URL
git remote -v

# Should show:
# origin  https://github.com/punishermortal/ecomerce_web.git (fetch)
# origin  https://github.com/punishermortal/ecomerce_web.git (push)

# Check if code is on GitHub
# Go to: https://github.com/punishermortal/ecomerce_web
```

## Alternative: Use SSH Key

### Step 1: Generate SSH Key

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
# Press Enter for all prompts
```

### Step 2: Add to GitHub

1. Copy your public key:
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```

2. Go to GitHub → Settings → SSH and GPG keys → New SSH key
3. Paste your public key
4. Click "Add SSH key"

### Step 3: Update Remote URL

```bash
git remote set-url origin git@github.com:punishermortal/ecomerce_web.git
git push origin main
```

## Windows PowerShell Commands

```powershell
# Method 1: Use token in URL
$token = "your_token_here"
git remote set-url origin "https://$token@github.com/punishermortal/ecomerce_web.git"
git push origin main

# Method 2: Use credential manager
git config --global credential.helper manager
git push origin main
# When prompted, use token as password

# Method 3: Use GitHub Desktop
# Install GitHub Desktop and sign in with punishermortal account
```

## After Successful Push

Once code is pushed successfully:

1. ✅ Code is on GitHub
2. ⬜ Setup server (see SERVER_SETUP.md)
3. ⬜ Configure Jenkins (see JENKINS_SETUP.md)
4. ⬜ Deploy application (see DEPLOYMENT.md)

## Troubleshooting

### Still Getting 403 Error?

1. **Check token permissions**: Must have `repo` scope
2. **Check token expiration**: Generate new token if expired
3. **Check repository access**: Ensure you have access to the repository
4. **Try SSH**: Use SSH key instead of HTTPS

### Token Not Working?

1. **Regenerate token**: Old token might be invalid
2. **Check token scope**: Must include `repo`
3. **Verify repository URL**: Check if URL is correct
4. **Check GitHub account**: Ensure you're using correct account

### SSH Key Not Working?

1. **Check SSH key**: `ssh -T git@github.com`
2. **Verify key is added**: Check GitHub SSH keys page
3. **Check key permissions**: `chmod 600 ~/.ssh/id_ed25519`

## Security Notes

⚠️ **Important**:
- Never share your token
- Never commit tokens to git
- Use SSH keys for better security
- Rotate tokens regularly
- Use token with minimum required permissions

## Next Steps

After successfully pushing code:

1. Follow `SERVER_SETUP.md` for server setup
2. Follow `JENKINS_SETUP.md` for Jenkins configuration
3. Follow `DEPLOYMENT.md` for deployment steps

