# Quick Setup: Payment & Delivery

## Step 1: Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

## Step 2: Add Razorpay Keys to .env

Edit `backend/.env`:

```env
RAZORPAY_KEY_ID=rzp_test_xxxxxxxxxxxxx
RAZORPAY_KEY_SECRET=your-secret-key
```

Get keys from: https://razorpay.com → Settings → API Keys

## Step 3: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Step 4: Install Frontend Dependencies

```bash
cd frontend
npm install
```

## Step 5: Test

1. Start backend: `python manage.py runserver`
2. Start frontend: `npm run dev`
3. Go to checkout page
4. Select payment method (Razorpay or COD)
5. Complete order

## Delivery Partner (Optional)

To enable delivery partner:

1. Add to `backend/.env`:
```env
DELIVERY_PARTNER_API_URL=https://api.deliverypartner.com
DELIVERY_PARTNER_API_KEY=your-api-key
DELIVERY_PARTNER_ENABLED=True
```

2. Update `backend/orders/delivery.py` with your delivery partner's API structure

## Features

✅ Razorpay integration
✅ Cash on Delivery (COD)
✅ Payment verification
✅ Delivery partner integration
✅ Order tracking
✅ Payment method selection in checkout

## Test Cards (Razorpay Test Mode)

- Card: 4111 1111 1111 1111
- Expiry: Any future date
- CVV: Any 3 digits

