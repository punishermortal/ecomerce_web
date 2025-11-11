# Payment and Delivery Setup Guide

## Razorpay Setup

### 1. Get Razorpay Credentials

1. Sign up at https://razorpay.com
2. Go to Settings > API Keys
3. Generate API keys (Key ID and Key Secret)
4. Use Test keys for development, Live keys for production

### 2. Configure Environment Variables

Add to your `.env` file in the backend directory:

```env
RAZORPAY_KEY_ID=rzp_test_xxxxxxxxxxxxx
RAZORPAY_KEY_SECRET=your-secret-key-here
```

### 3. Test Mode

- Use test keys for development
- Test card: 4111 1111 1111 1111
- Any future expiry date
- Any CVV

## Delivery Partner Setup

### 1. Configure Delivery Partner

Add to your `.env` file:

```env
DELIVERY_PARTNER_API_URL=https://api.deliverypartner.com
DELIVERY_PARTNER_API_KEY=your-api-key
DELIVERY_PARTNER_ENABLED=True
```

### 2. Update Delivery Partner API

The delivery integration is in `backend/orders/delivery.py`. Update the API endpoint and payload structure according to your delivery partner's API documentation.

### 3. Delivery Partner API Expected Format

The code expects the delivery partner API to:
- Accept POST requests to `/api/orders`
- Return JSON with `order_id`, `tracking_id`, and `status`
- Accept tracking GET requests to `/api/track/{tracking_id}`

## Database Migration

After updating the models, run:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Frontend Setup

1. Install dependencies (already added):
   ```bash
   npm install
   ```

2. Razorpay script loads automatically from CDN
3. Payment method selection is available in checkout

## Testing

### Test Razorpay Payment

1. Use test mode keys
2. Use test card: 4111 1111 1111 1111
3. Complete payment flow
4. Verify payment in Razorpay dashboard

### Test COD

1. Select COD as payment method
2. Place order
3. Order should be created with payment_status='pending'
4. Cart should be cleared immediately

## Order Flow

### Razorpay Flow:
1. User selects Razorpay
2. Order created with payment_status='pending'
3. Razorpay order created
4. Payment modal opens
5. User completes payment
6. Payment verified on backend
7. Order status updated to 'paid'
8. Cart cleared
9. Delivery order created

### COD Flow:
1. User selects COD
2. Order created with payment_status='pending'
3. Cart cleared immediately
4. Delivery order created
5. Payment collected on delivery

## Troubleshooting

### Razorpay not loading
- Check internet connection
- Verify Razorpay script URL
- Check browser console for errors

### Payment verification fails
- Check Razorpay keys in .env
- Verify signature verification logic
- Check Razorpay dashboard for payment status

### Delivery partner not working
- Set DELIVERY_PARTNER_ENABLED=True
- Verify API URL and key
- Check API response format
- Review delivery.py for API structure

