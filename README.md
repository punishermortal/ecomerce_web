# NextBloom - E-commerce Website

A modern e-commerce platform built with Django (DRF) backend and Next.js frontend.

## Features

- ✅ User authentication with phone number and password
- ✅ Product catalog with categories
- ✅ Shopping cart
- ✅ Order management
- ✅ Razorpay payment integration
- ✅ Cash on Delivery (COD)
- ✅ Delhivery integration for delivery
- ✅ Admin panel for management
- ✅ Responsive design

## Tech Stack

### Backend
- Django 4.2+
- Django REST Framework
- PostgreSQL (production) / SQLite (development)
- JWT Authentication
- Razorpay SDK
- Delhivery API

### Frontend
- Next.js 14+
- React
- Redux Toolkit
- Tailwind CSS
- Axios

## Setup

### Prerequisites
- Python 3.9+
- Node.js 18+
- PostgreSQL (for production)
- Git

### Backend Setup

1. Clone the repository:
```bash
git clone https://github.com/punishermortal/ecomerce_web.git
cd ecomerce_web/backend
```

2. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create superuser:
```bash
python manage.py createsuperuser
```

7. Run server:
```bash
python manage.py runserver
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd ../frontend
```

2. Install dependencies:
```bash
npm install
```

3. Configure environment variables:
```bash
cp .env.example .env.local
# Edit .env.local with your API URL
```

4. Run development server:
```bash
npm run dev
```

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

### Quick Deployment

1. Server setup (one-time):
```bash
# Follow DEPLOYMENT.md for initial server setup
```

2. Automated deployment with Jenkins:
- Jenkins is configured to automatically deploy on git push
- See Jenkinsfile for pipeline configuration

3. Manual deployment:
```bash
./deploy.sh
```

## Environment Variables

### Backend (.env)
```env
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
DATABASE_URL=postgresql://user:password@localhost:5432/nextbloom
RAZORPAY_KEY_ID=your_razorpay_key
RAZORPAY_KEY_SECRET=your_razorpay_secret
DELHIVERY_API_TOKEN=your_delhivery_token
DELHIVERY_ENABLED=True
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

## API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login with phone number
- `POST /api/auth/change-password/` - Change password
- `POST /api/auth/forgot-password/` - Request OTP
- `POST /api/auth/reset-password/` - Reset password with OTP

### Products
- `GET /api/products/` - List products
- `GET /api/products/{id}/` - Get product details
- `GET /api/products/categories/` - List categories

### Cart
- `GET /api/cart/` - Get cart
- `POST /api/cart/add/` - Add item to cart
- `POST /api/cart/remove/` - Remove item from cart

### Orders
- `GET /api/orders/` - List orders
- `POST /api/orders/` - Create order
- `GET /api/orders/{id}/` - Get order details

## Admin Panel

Access admin panel at: `http://localhost:8000/admin/`

## CI/CD

Jenkins is configured for automated deployment:
- Automatic deployment on git push
- Health checks
- Service restart
- See Jenkinsfile for pipeline configuration

## Documentation

- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment guide
- [PASSWORD_AUTH_SETUP.md](PASSWORD_AUTH_SETUP.md) - Authentication setup
- [DELHIVERY_SETUP.md](backend/DELHIVERY_SETUP.md) - Delhivery integration
- [ADMIN_PANEL_GUIDE.md](ADMIN_PANEL_GUIDE.md) - Admin panel guide

## License

MIT License

## Support

For issues and questions, please open an issue on GitHub.

## Contributors

- Your Name

## Repository

https://github.com/punishermortal/ecomerce_web.git
