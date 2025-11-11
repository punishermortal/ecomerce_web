# Fix Migration Issue - Run this script after stopping the Django server

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "NextBloom Database Migration Fix" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if server is running (database file is locked)
Write-Host "Step 1: Checking if database file exists..." -ForegroundColor Yellow
if (Test-Path db.sqlite3) {
    Write-Host "Database file found: db.sqlite3" -ForegroundColor Green
    
    # Try to delete it
    Write-Host "Step 2: Attempting to delete old database..." -ForegroundColor Yellow
    try {
        Remove-Item db.sqlite3 -Force -ErrorAction Stop
        Write-Host "✓ Database file deleted successfully" -ForegroundColor Green
    } catch {
        Write-Host "✗ ERROR: Cannot delete database file!" -ForegroundColor Red
        Write-Host "  The Django server is still running. Please stop it first (CTRL+C)" -ForegroundColor Red
        Write-Host "  Then run this script again." -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
} else {
    Write-Host "No database file found. Creating fresh database..." -ForegroundColor Green
}

# Delete journal file if exists
if (Test-Path db.sqlite3-journal) {
    Remove-Item db.sqlite3-journal -Force -ErrorAction SilentlyContinue
    Write-Host "✓ Journal file deleted" -ForegroundColor Green
}

Write-Host ""
Write-Host "Step 3: Running migrations..." -ForegroundColor Yellow

# Activate virtual environment and run migrations
& .\venv\Scripts\Activate.ps1
python manage.py migrate

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "✓ Migrations applied successfully!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "You can now start the server with:" -ForegroundColor Cyan
    Write-Host "  python manage.py runserver" -ForegroundColor White
    Write-Host ""
    Write-Host "Optional: Create a superuser with:" -ForegroundColor Cyan
    Write-Host "  python manage.py createsuperuser" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "✗ ERROR: Migrations failed!" -ForegroundColor Red
    Write-Host "Please check the error messages above." -ForegroundColor Red
}

Read-Host "Press Enter to exit"

