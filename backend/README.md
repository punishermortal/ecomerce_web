# NextBloom Backend

Django REST Framework backend for NextBloom e-commerce platform.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file:
```bash
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

3. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. Create superuser:
```bash
python manage.py createsuperuser
```

5. Run server:
```bash
python manage.py runserver
```

## API Documentation

Once the server is running, you can access:
- API Root: http://localhost:8000/api/
- Admin Panel: http://localhost:8000/admin/

## Apps

- **accounts**: User authentication and management
- **products**: Product catalog and categories
- **cart**: Shopping cart management
- **orders**: Order processing and management

## Testing

```bash
python manage.py test
```

## Production

For production deployment:
1. Set `DEBUG = False` in settings.py
2. Configure `ALLOWED_HOSTS`
3. Set up PostgreSQL database
4. Configure static files with WhiteNoise
5. Use Gunicorn as WSGI server

