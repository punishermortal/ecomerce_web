# Script to reset database and run migrations

Write-Host "Stopping Django server if running..."
Write-Host "Please stop the Django server (CTRL+C) before continuing." -ForegroundColor Yellow
Write-Host ""
Read-Host "Press Enter to continue after stopping the server"

Write-Host "Deleting old database..."
if (Test-Path db.sqlite3) { Remove-Item db.sqlite3 -Force }
if (Test-Path db.sqlite3-journal) { Remove-Item db.sqlite3-journal -Force }

Write-Host "Running migrations..."
.\venv\Scripts\Activate.ps1
python manage.py migrate

Write-Host ""
Write-Host "Database reset complete!" -ForegroundColor Green
Write-Host "You can now start the server with: python manage.py runserver"

