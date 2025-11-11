# Complete Setup Script - Fix Migrations and Add Sample Data

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "NextBloom Setup & Data Seeding" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check if server is running
Write-Host "Step 1: Checking if Django server is running..." -ForegroundColor Yellow
$dbLocked = $false
try {
    $file = [System.IO.File]::Open("db.sqlite3", 'Open', 'ReadWrite', 'None')
    $file.Close()
} catch {
    $dbLocked = $true
    Write-Host "  Database file is locked. Server may be running." -ForegroundColor Red
    Write-Host "  Please stop the Django server (CTRL+C) and run this script again." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Step 2: Delete old database if it exists and has issues
Write-Host "Step 2: Cleaning up database..." -ForegroundColor Yellow
if (Test-Path db.sqlite3) {
    $delete = Read-Host "  Database exists. Delete and recreate? (y/n)"
    if ($delete -eq 'y' -or $delete -eq 'Y') {
        Remove-Item db.sqlite3 -Force -ErrorAction SilentlyContinue
        Remove-Item db.sqlite3-journal -Force -ErrorAction SilentlyContinue
        Write-Host "  ✓ Database deleted" -ForegroundColor Green
    }
}

# Step 3: Activate virtual environment
Write-Host ""
Write-Host "Step 3: Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Step 4: Run migrations
Write-Host ""
Write-Host "Step 4: Running migrations..." -ForegroundColor Yellow
python manage.py migrate

if ($LASTEXITCODE -ne 0) {
    Write-Host "  ✗ Migrations failed!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "  ✓ Migrations completed" -ForegroundColor Green

# Step 5: Seed data
Write-Host ""
Write-Host "Step 5: Seeding sample data..." -ForegroundColor Yellow
python manage.py seed_data

if ($LASTEXITCODE -ne 0) {
    Write-Host "  ✗ Seeding failed!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "✓ Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Create a superuser (optional):" -ForegroundColor White
Write-Host "     python manage.py createsuperuser" -ForegroundColor Gray
Write-Host ""
Write-Host "  2. Start the server:" -ForegroundColor White
Write-Host "     python manage.py runserver" -ForegroundColor Gray
Write-Host ""
Write-Host "  3. View your data:" -ForegroundColor White
Write-Host "     Frontend: http://localhost:3000" -ForegroundColor Gray
Write-Host "     Admin: http://localhost:8000/admin" -ForegroundColor Gray
Write-Host ""

Read-Host "Press Enter to exit"

