# Seed Sample Data

This guide explains how to populate your NextBloom database with sample products and categories.

## Prerequisites

1. Make sure migrations have been run:
   ```bash
   python manage.py migrate
   ```

2. Make sure the Django server is stopped (or run this in a separate terminal)

## Running the Seed Command

To add sample data (categories and products) to your database, run:

```bash
python manage.py seed_data
```

This will create:
- **8 Categories**: Fresh Fruits, Fresh Vegetables, Dairy & Eggs, Bakery, Organic Foods, Beverages, Snacks, Meat & Seafood
- **27 Products**: A variety of products across all categories with prices, descriptions, ratings, and some with discounts

## What Gets Created

### Categories
- Fresh Fruits
- Fresh Vegetables  
- Dairy & Eggs
- Bakery
- Organic Foods
- Beverages
- Snacks
- Meat & Seafood

### Products Include
- Organic fruits and vegetables
- Fresh dairy products
- Baked goods
- Organic foods and snacks
- Beverages
- Fresh meat and seafood

Many products have:
- Prices and discount prices
- Descriptions
- Stock quantities
- Ratings and review counts
- Featured products (marked for homepage display)

## Running Multiple Times

The command is safe to run multiple times. It will:
- Create categories if they don't exist
- Create products if they don't exist
- Update existing products with new data

## Adding Your Own Data

You can modify `products/management/commands/seed_data.py` to add your own products and categories.

## Viewing the Data

After seeding:
1. Start your Django server: `python manage.py runserver`
2. Visit the admin panel: http://localhost:8000/admin
3. View products on the frontend: http://localhost:3000/products

