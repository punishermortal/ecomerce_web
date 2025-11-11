# GitHub Push Instructions

## Issue
The git push is failing because you need to authenticate with GitHub using the correct credentials for the `punishermortal` account.

## Solution Options

### Option 1: Use Personal Access Token (Recommended)

1. **Generate Personal Access Token**:
   - Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Click "Generate new token (classic)"
   - Give it a name: "NextBloom Deployment"
   - Select scopes: `repo` (full control of private repositories)
   - Click "Generate token"
   - Copy the token (you'll only see it once!)

2. **Push using token**:
   ```bash
   git push https://YOUR_TOKEN@github.com/punishermortal/ecomerce_web.git main
   ```
   Replace `YOUR_TOKEN` with your actual token.

3. **Or configure remote with token**:
   ```bash
   git remote set-url origin https://YOUR_TOKEN@github.com/punishermortal/ecomerce_web.git
   git push origin main
   ```

### Option 2: Use SSH Key (More Secure)

1. **Generate SSH key** (if you don't have one):
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```

2. **Add SSH key to GitHub**:
   - Copy your public key: `cat ~/.ssh/id_ed25519.pub`
   - Go to GitHub → Settings → SSH and GPG keys → New SSH key
   - Paste your public key
   - Click "Add SSH key"

3. **Change remote URL to SSH**:
   ```bash
   git remote set-url origin git@github.com:punishermortal/ecomerce_web.git
   git push origin main
   ```

### Option 3: Use GitHub CLI

1. **Install GitHub CLI**:
   ```bash
   # Windows: Download from https://cli.github.com
   # Or use: winget install GitHub.cli
   ```

2. **Authenticate**:
   ```bash
   gh auth login
   ```

3. **Push**:
   ```bash
   git push origin main
   ```

## Quick Fix (Windows PowerShell)

```powershell
# Method 1: Use Personal Access Token
$token = "your_github_token_here"
git remote set-url origin "https://$token@github.com/punishermortal/ecomerce_web.git"
git push origin main

# Method 2: Use GitHub Credential Manager
git config --global credential.helper manager
git push origin main
# It will prompt for username and password (use token as password)
```

## Verify Remote URL

```bash
git remote -v
```

Should show:
```
origin  https://github.com/punishermortal/ecomerce_web.git (fetch)
origin  https://github.com/punishermortal/ecomerce_web.git (push)
```

## After Successful Push

Once the code is pushed, you can proceed with server setup using the deployment guides.

