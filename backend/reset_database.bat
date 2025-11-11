@echo off
REM Script to reset database and run migrations

echo Stopping Django server if running...
echo Please stop the Django server (CTRL+C) before continuing.
echo.
pause

echo Deleting old database...
if exist db.sqlite3 del db.sqlite3
if exist db.sqlite3-journal del db.sqlite3-journal

echo Running migrations...
call venv\Scripts\activate.bat
python manage.py migrate

echo.
echo Database reset complete!
echo You can now start the server with: python manage.py runserver
pause

