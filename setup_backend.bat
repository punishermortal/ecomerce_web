@echo off
REM NextBloom Backend Setup Script for Windows

echo Setting up NextBloom Backend...

REM Create virtual environment
python -m venv venv
call venv\Scripts\activate.bat

REM Install dependencies
pip install -r backend\requirements.txt

REM Create .env file if it doesn't exist
if not exist backend\.env (
    echo Creating .env file...
    echo SECRET_KEY=django-insecure-change-in-production > backend\.env
    echo DEBUG=True >> backend\.env
    echo ALLOWED_HOSTS=localhost,127.0.0.1 >> backend\.env
)

REM Navigate to backend directory
cd backend

REM Run migrations
python manage.py makemigrations
python manage.py migrate

echo Backend setup complete!
echo Run 'python manage.py runserver' to start the development server

pause

