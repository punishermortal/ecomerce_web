# Quick Instructions to Add Sample Data

## Step 1: Stop Django Server (if running)
Press `CTRL+C` in the terminal where the server is running.

## Step 2: Run the Seed Command

Open a terminal in the backend directory and run:

```powershell
cd C:\Users\rupas\Music\next\backend
.\venv\Scripts\Activate.ps1
python manage.py seed_data
```

## Step 3: Start the Server Again

```powershell
python manage.py runserver
```

## What You'll Get

✅ 8 Categories (Fresh Fruits, Vegetables, Dairy, Bakery, etc.)
✅ 27 Products with prices, descriptions, and ratings
✅ Featured products for the homepage
✅ Products with discounts
✅ Realistic e-commerce data

## View Your Data

- **Frontend**: http://localhost:3000
- **Admin Panel**: http://localhost:8000/admin

The homepage will show featured products, and you can browse all products in the products page!

