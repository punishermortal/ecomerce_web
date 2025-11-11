# Fix Migration Issue

## Problem
The database has inconsistent migration state because Django's admin migrations were applied before the custom User model migration.

## Solution

### Step 1: Stop the Django Server
Stop the Django development server that's currently running (press `CTRL+C` in the terminal where it's running).

### Step 2: Delete the Database
Delete the existing database file to start fresh:

**Windows PowerShell:**
```powershell
cd C:\Users\rupas\Music\next\backend
Remove-Item db.sqlite3 -ErrorAction SilentlyContinue
Remove-Item db.sqlite3-journal -ErrorAction SilentlyContinue
```

**Or use the reset script:**
```powershell
.\reset_database.ps1
```

### Step 3: Run Migrations
Activate your virtual environment and run migrations:

```powershell
.\venv\Scripts\Activate.ps1
python manage.py migrate
```

### Step 4: Create Superuser (Optional)
```powershell
python manage.py createsuperuser
```

### Step 5: Start the Server
```powershell
python manage.py runserver
```

## Alternative: Quick Fix Script

You can also run the provided script:
- **Windows:** `reset_database.bat`
- **PowerShell:** `.\reset_database.ps1`

## Why This Happened
When you first ran `python manage.py migrate`, Django created the default admin migrations that depend on Django's default User model. Later, when we created the custom User model in the `accounts` app, Django detected that admin migrations were already applied, but they depend on a User model that doesn't exist yet (our custom one).

By deleting the database and running migrations fresh, all migrations will be applied in the correct order with the custom User model from the start.

