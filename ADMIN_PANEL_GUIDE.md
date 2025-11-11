# NextBloom Admin Panel Guide

## Overview

The NextBloom admin panel is a comprehensive management system that allows administrators to manage products, orders, users, and deliveries efficiently.

## Accessing the Admin Panel

1. **URL**: `http://localhost:8000/admin/`
2. **Login**: Use your superuser credentials
3. **Create Superuser**: 
   ```bash
   python manage.py createsuperuser
   ```

## Admin Panel Features

### 1. Products Management

#### Adding Products
1. Go to **Products** > **Products**
2. Click **Add Product**
3. Fill in product details:
   - Name, Slug (auto-generated), Category, Description
   - Price, Discount Price (optional)
   - Stock quantity
   - Active status, Featured status
   - Rating
4. Add product images in the inline section
5. Click **Save**

#### Product Features
- **Bulk Actions**: 
  - Mark as featured/unfeatured
  - Activate/deactivate products
  - Restock products (+10 units)
- **Stock Status**: Visual indicators for:
  - Out of Stock (red)
  - Low Stock < 10 (orange)
  - In Stock (green)
- **Price Display**: Shows original price with strikethrough and discount price
- **Image Preview**: Thumbnail preview in list view
- **Quick Edit**: Edit stock, active status, and featured status directly from list view

#### Categories
- Add/edit categories
- View product count per category
- Manage category images
- Activate/deactivate categories

### 2. Orders Management

#### Order Features
- **Status Badges**: Color-coded status indicators
  - Pending (gray)
  - Processing (blue)
  - Shipped (purple)
  - Delivered (green)
  - Cancelled (red)
- **Payment Status**: Color-coded payment indicators
  - Pending (orange)
  - Paid (green)
  - Failed (red)
  - Refunded (gray)
- **Bulk Actions**:
  - Mark as processing
  - Mark as shipped
  - Mark as delivered
  - Mark as cancelled
  - Refresh delivery status from Delhivery
- **Tracking Links**: Click tracking ID to open Delhivery tracking page
- **Order Details**: View order items, shipping info, payment info, delivery info

#### Order Items
- View all order items
- Click on order/product to navigate to detail page
- See quantity, price, and total for each item

### 3. User Management

#### User Features
- View all users
- See user order count (clickable link)
- Filter by staff status, active status, email verification
- Search by email, username, name, phone
- View user details including address, phone, etc.

### 4. Cart Management

#### Cart Features
- View all carts
- See cart items inline
- View total items and total price
- Search by user email/name
- Filter by date

### 5. Delivery Management

#### Delhivery Integration
- **Automatic Shipment Creation**: Orders automatically create Delhivery shipments
- **Tracking IDs**: Stored and displayed in order details
- **Status Refresh**: Bulk action to refresh delivery status from Delhivery
- **Tracking Links**: Direct links to Delhivery tracking page

## Admin Panel Best Practices

### Product Management
1. **Add Products**: Always add product images for better display
2. **Stock Management**: Regularly check low stock items
3. **Featured Products**: Mark best-selling products as featured
4. **Categories**: Organize products into categories for better navigation

### Order Management
1. **Status Updates**: Update order status as it progresses
2. **Delivery Tracking**: Refresh delivery status regularly
3. **Payment Verification**: Verify payments for Razorpay orders
4. **COD Orders**: Mark as delivered after delivery confirmation

### User Management
1. **User Verification**: Verify user emails
2. **Staff Access**: Grant staff access to trusted users
3. **User Support**: Help users with order issues

## Admin Actions

### Products
- **Make Featured**: Mark selected products as featured
- **Make Unfeatured**: Unmark selected products as featured
- **Activate Products**: Activate selected products
- **Deactivate Products**: Deactivate selected products
- **Restock Products**: Add 10 units to selected products

### Orders
- **Mark as Processing**: Update order status to processing
- **Mark as Shipped**: Update order status to shipped
- **Mark as Delivered**: Update order status to delivered and mark payment as paid
- **Mark as Cancelled**: Cancel selected orders
- **Refresh Delivery Status**: Fetch latest status from Delhivery

## Search and Filters

### Products
- Search by: name, description, category name
- Filter by: category, active status, featured status, rating, stock, date

### Orders
- Search by: order number, user email/username, tracking ID, payment ID, phone, city, address
- Filter by: status, payment status, payment method, delivery status, date

### Users
- Search by: email, username, first name, last name, phone number
- Filter by: staff status, active status, email verification, date

## Tips and Tricks

1. **Quick Navigation**: Use the search bar to quickly find products/orders/users
2. **Bulk Operations**: Select multiple items and use bulk actions
3. **Date Hierarchy**: Use date hierarchy to filter by date ranges
4. **List Editable**: Edit stock, active status, and featured status directly from list view
5. **Inline Editing**: Add/edit product images directly in product form
6. **Tracking Links**: Click tracking ID to open Delhivery tracking page in new tab

## Security

1. **Superuser Access**: Only grant superuser access to trusted administrators
2. **Staff Access**: Grant staff access to users who need admin access
3. **Password Security**: Use strong passwords for admin accounts
4. **Session Management**: Log out when done with admin tasks

## Troubleshooting

### Can't Access Admin Panel
- Check if superuser account exists
- Verify credentials
- Check if server is running

### Products Not Showing
- Check if products are active
- Verify category is active
- Check stock availability

### Orders Not Updating
- Verify Delhivery integration is enabled
- Check API credentials
- Refresh delivery status manually

### Images Not Uploading
- Check MEDIA_ROOT and MEDIA_URL settings
- Verify file permissions
- Check file size limits

## Support

For issues or questions:
1. Check this guide
2. Review Django admin documentation
3. Check Delhivery integration setup
4. Contact support team

