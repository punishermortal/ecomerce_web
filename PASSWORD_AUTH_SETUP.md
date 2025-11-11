# Password Authentication & Phone Number Login Setup

## Overview

NextBloom now uses **phone number and password** for login instead of email. The system includes:
- ✅ Phone number login
- ✅ Change password functionality
- ✅ Forgot password with OTP
- ✅ Phone number registration (required)

## Backend Changes

### 1. User Model Updates

- `phone_number` is now **unique and required**
- `USERNAME_FIELD` changed from `email` to `phone_number`
- `email` is now optional (for password recovery)
- Added `is_phone_verified` field
- Added `PasswordResetOTP` model for OTP-based password reset

### 2. New API Endpoints

#### Change Password
- **URL**: `POST /api/auth/change-password/`
- **Auth**: Required (Authenticated users)
- **Body**:
  ```json
  {
    "old_password": "current password",
    "new_password": "new password",
    "new_password2": "confirm new password"
  }
  ```

#### Forgot Password (Request OTP)
- **URL**: `POST /api/auth/forgot-password/`
- **Auth**: Not required
- **Body**:
  ```json
  {
    "phone_number": "9876543210"
  }
  ```
- **Response**: OTP sent to registered email (if available)

#### Reset Password
- **URL**: `POST /api/auth/reset-password/`
- **Auth**: Not required
- **Body**:
  ```json
  {
    "phone_number": "9876543210",
    "otp": "123456",
    "new_password": "new password",
    "new_password2": "confirm new password"
  }
  ```

### 3. Login Endpoint

- **URL**: `POST /api/auth/login/`
- **Body**:
  ```json
  {
    "phone_number": "9876543210",
    "password": "password"
  }
  ```

### 4. Registration

- Phone number is now **required**
- Email is **optional** (recommended for password recovery)
- Phone number format: 10 digits (automatically prefixed with +91)

## Frontend Changes

### 1. Login Page (`/login`)
- Changed from email to phone number input
- Phone number format: +91 prefix with 10-digit number
- Added "Forgot Password?" link

### 2. Registration Page (`/register`)
- Added phone number field (required)
- Email field is now optional
- Phone number validation (10 digits)

### 3. Change Password Page (`/change-password`)
- New page for authenticated users
- Requires current password
- Validates new password (min 8 characters)
- Password confirmation

### 4. Forgot Password Page (`/forgot-password`)
- Two-step process:
  1. Request OTP (enter phone number)
  2. Reset password (enter OTP and new password)
- OTP sent to registered email
- OTP valid for 10 minutes

## Database Migration

### Steps to Migrate:

1. **Create Migration**:
   ```bash
   cd backend
   python manage.py makemigrations accounts
   ```

2. **Apply Migration**:
   ```bash
   python manage.py migrate
   ```

3. **Update Existing Users** (if any):
   - Existing users need to have `phone_number` set
   - You can update via admin panel or Django shell:
     ```python
     from accounts.models import User
     for user in User.objects.filter(phone_number__isnull=True):
         user.phone_number = f"+91{user.id}"  # Temporary phone number
         user.save()
     ```

## Phone Number Format

- **Format**: 10-digit Indian mobile number
- **Storage**: Automatically prefixed with `+91`
- **Example**: `9876543210` → stored as `+919876543210`
- **Validation**: Only digits allowed, automatically formatted

## OTP System

### OTP Generation
- 6-digit random OTP
- Valid for 10 minutes
- One OTP per phone number (old OTPs are deleted)

### OTP Delivery
- Sent via email (if user has email)
- In development: OTP shown in response and console
- In production: Remove OTP from response

### OTP Verification
- OTP is case-sensitive
- OTP can only be used once
- Expired OTPs are automatically invalidated

## Security Features

1. **Password Validation**: Django's password validators
2. **OTP Expiration**: 10-minute validity
3. **OTP One-Time Use**: OTPs are marked as used after verification
4. **Phone Number Normalization**: Automatic formatting
5. **Password Strength**: Minimum 8 characters

## Testing

### Test Login
1. Register with phone number
2. Login with phone number and password
3. Verify authentication works

### Test Change Password
1. Login to account
2. Go to `/change-password`
3. Enter current password and new password
4. Verify password is changed

### Test Forgot Password
1. Go to `/forgot-password`
2. Enter phone number
3. Check email for OTP (or console in development)
4. Enter OTP and new password
5. Verify password is reset

## Production Setup

### Email Configuration

Update `backend/nextbloom/settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'noreply@nextbloom.com'
```

### Remove OTP from Response

In `backend/accounts/views.py`, remove OTP from response:

```python
return Response({
    'message': 'OTP sent to your registered email',
    # Remove: 'otp': otp
}, status=status.HTTP_200_OK)
```

### SMS Integration (Optional)

For production, integrate SMS service (Twilio, AWS SNS, etc.):

```python
# In forgot_password view
# Send OTP via SMS
send_sms(phone_number, f"Your OTP is: {otp}")
```

## Troubleshooting

### Issue: "Phone number is required"
- **Solution**: Ensure phone_number is provided in registration
- Check that migration was applied correctly

### Issue: "Invalid phone number format"
- **Solution**: Ensure phone number is 10 digits
- Phone number is automatically formatted

### Issue: "OTP not received"
- **Solution**: Check email configuration
- In development, check console for OTP
- Verify user has email address

### Issue: "Invalid or expired OTP"
- **Solution**: OTP expires after 10 minutes
- Request new OTP
- Ensure OTP is entered correctly

## API Response Examples

### Login Success
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "user",
    "phone_number": "+919876543210",
    "first_name": "John",
    "last_name": "Doe"
  },
  "refresh": "refresh_token",
  "access": "access_token"
}
```

### Change Password Success
```json
{
  "message": "Password changed successfully"
}
```

### Forgot Password Success
```json
{
  "message": "OTP sent to your registered email",
  "otp": "123456"  // Remove in production
}
```

### Reset Password Success
```json
{
  "message": "Password reset successfully"
}
```

## Notes

- Phone number is the primary identifier for users
- Email is optional but recommended for password recovery
- OTP system is email-based (can be extended to SMS)
- All password operations require authentication (except forgot/reset)
- Phone numbers are automatically normalized to +91 format

