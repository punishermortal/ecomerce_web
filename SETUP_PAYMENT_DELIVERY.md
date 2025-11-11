# Payment and Delivery Setup Guide

## Overview

NextBloom now supports:
- ✅ **Razorpay** - Online payment gateway
- ✅ **Cash on Delivery (COD)** - Pay when you receive
- ✅ **Delivery Partner Integration** - Automated delivery management

## Backend Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

This will install:
- `razorpay==1.4.1` - Razorpay SDK
- `requests==2.31.0` - For delivery partner API calls

### 2. Configure Environment Variables

Add to `backend/.env`:

```env
# Razorpay Configuration
RAZORPAY_KEY_ID=rzp_test_xxxxxxxxxxxxx
RAZORPAY_KEY_SECRET=your-razorpay-secret-key

# Delivery Partner Configuration
DELIVERY_PARTNER_API_URL=https://api.deliverypartner.com
DELIVERY_PARTNER_API_KEY=your-delivery-partner-api-key
DELIVERY_PARTNER_ENABLED=False
```

### 3. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Get Razorpay Keys

1. Sign up at https://razorpay.com
2. Go to Settings > API Keys
3. Generate Test/Live keys
4. Add to `.env` file

**Test Mode Cards:**
- Card: 4111 1111 1111 1111
- Any future expiry date
- Any CVV

## Frontend Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

Razorpay script loads automatically from CDN (no npm package needed for frontend).

### 2. Environment Variables

Already configured in `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

## Delivery Partner Setup

### 1. Configure Your Delivery Partner

Update `backend/orders/delivery.py` according to your delivery partner's API:

1. Update API endpoint URL
2. Update request payload structure
3. Update response handling
4. Add authentication method if needed

### 2. Enable Delivery Partner

Set in `.env`:
```env
DELIVERY_PARTNER_ENABLED=True
```

### 3. Delivery Partner API Format

The code expects your delivery partner API to:
- **Create Order**: `POST /api/orders`
- **Track Order**: `GET /api/track/{tracking_id}`
- **Response Format**:
  ```json
  {
    "order_id": "DP123",
    "tracking_id": "TRACK123",
    "status": "pending"
  }
  ```

## How It Works

### Razorpay Flow

1. User selects Razorpay payment method
2. Order created with `payment_status='pending'`
3. Razorpay order created on Razorpay servers
4. Payment modal opens
5. User completes payment
6. Payment verified on backend
7. Order status updated to `payment_status='paid'`
8. Cart cleared
9. Delivery order created

### COD Flow

1. User selects COD payment method
2. Order created with `payment_status='pending'`
3. Order status set to `'processing'`
4. Cart cleared immediately
5. Delivery order created
6. Payment collected on delivery

### Delivery Partner Flow

1. After order creation (Razorpay or COD)
2. Delivery order created with delivery partner
3. Tracking ID stored in order
4. Delivery status updated
5. User can track order using tracking ID

## API Endpoints

### Orders
- `POST /api/orders/` - Create order
  - Body: `{ payment_method: 'razorpay' | 'cod', ... }`

### Payment
- `POST /api/orders/payment/verify/` - Verify Razorpay payment
- `GET /api/orders/payment/razorpay-key/` - Get Razorpay key ID

## Testing

### Test Razorpay

1. Use test mode keys
2. Use test card: 4111 1111 1111 1111
3. Complete payment flow
4. Check Razorpay dashboard

### Test COD

1. Select COD at checkout
2. Place order
3. Order should be created
4. Cart should be cleared
5. Order status: processing

## Order Status Flow

1. **pending** - Order created, payment pending
2. **processing** - Payment received (COD) or verified (Razorpay)
3. **shipped** - Order shipped by delivery partner
4. **delivered** - Order delivered
5. **cancelled** - Order cancelled

## Payment Status

- **pending** - Payment not received yet
- **paid** - Payment received and verified
- **failed** - Payment failed
- **refunded** - Payment refunded

## Troubleshooting

### Razorpay Issues
- Check Razorpay keys in `.env`
- Verify key format (starts with `rzp_test_` or `rzp_live_`)
- Check Razorpay dashboard for order status
- Verify payment signature

### Delivery Partner Issues
- Set `DELIVERY_PARTNER_ENABLED=True`
- Check API URL and key
- Verify API response format
- Check delivery.py for API structure
- Review API documentation

### Payment Verification Fails
- Check Razorpay keys match
- Verify signature verification
- Check order exists in Razorpay dashboard
- Review error logs

## Production Deployment

### Razorpay
1. Switch to Live keys
2. Update `RAZORPAY_KEY_ID` and `RAZORPAY_KEY_SECRET`
3. Test with real transactions

### Delivery Partner
1. Update API URL to production
2. Use production API key
3. Test order creation
4. Monitor delivery status updates

## Security Notes

- Never commit `.env` file
- Keep Razorpay secret key secure
- Use HTTPS in production
- Verify payment signatures
- Validate all payment data

## Support

For issues:
1. Check Razorpay dashboard
2. Review delivery partner API docs
3. Check Django logs
4. Check browser console for frontend errors

