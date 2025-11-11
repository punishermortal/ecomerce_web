# How to Push Code to GitHub

## Current Issue
Git push is failing with: `Permission to punishermortal/ecomerce_web.git denied to rupashreeroy`

This means you need to authenticate with the correct GitHub account.

## Quick Solution

### Option 1: Use Personal Access Token (Fastest)

1. **Generate Token**:
   - Go to: https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Name: "NextBloom"
   - Select: `repo` scope
   - Generate and **copy the token**

2. **Push with Token**:
   ```bash
   # In PowerShell or Command Prompt
   git remote set-url origin https://YOUR_TOKEN@github.com/punishermortal/ecomerce_web.git
   git push origin main
   ```

   Replace `YOUR_TOKEN` with your actual token.

### Option 2: Use GitHub Desktop

1. Install GitHub Desktop
2. Sign in with `punishermortal` account
3. Add repository
4. Push code

### Option 3: Configure Git Credentials

```bash
# Windows
git config --global credential.helper manager
git push origin main
# When prompted:
# Username: punishermortal
# Password: YOUR_PERSONAL_ACCESS_TOKEN
```

## Verify

```bash
git remote -v
```

Should show:
```
origin  https://github.com/punishermortal/ecomerce_web.git (fetch)
origin  https://github.com/punishermortal/ecomerce_web.git (push)
```

## After Successful Push

Once code is pushed, proceed with server deployment using `COMPLETE_DEPLOYMENT_GUIDE.md`

