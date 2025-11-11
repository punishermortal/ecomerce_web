# Fix: Categories and Products Not Fetching

## Issue
Categories and products are not loading in the frontend, even though the backend API is working correctly.

## Root Cause Analysis

### Backend API Status
✅ **Working**: All API endpoints are responding correctly:
- `http://localhost:8000/api/products/categories/` - Returns 200 OK with category data
- `http://localhost:8000/api/products/` - Returns 200 OK with product data
- `http://localhost:8000/api/products/featured/` - Returns 200 OK with featured products

### Possible Issues

1. **Environment Variable Not Set**
   - `NEXT_PUBLIC_API_URL` might not be set correctly
   - Next.js needs environment variables to be prefixed with `NEXT_PUBLIC_`
   - Environment variables need to be available at build/runtime

2. **CORS Issues**
   - Backend CORS is configured for `localhost:3000`
   - Frontend should be running on `http://localhost:3000`
   - Check if CORS headers are being sent correctly

3. **Network Errors**
   - Browser might be blocking requests
   - Check browser console for CORS or network errors
   - Check Network tab in DevTools

4. **API URL Configuration**
   - Frontend might be using wrong API URL
   - Check if `process.env.NEXT_PUBLIC_API_URL` is being read correctly

## Solutions Applied

### 1. Added Debug Logging
Added console.log statements to track:
- API URLs being called
- Response data
- Error messages and details

### 2. Improved Error Handling
- Better error messages in console
- Error status codes
- Response data logging

### 3. Fixed API URL Configuration
- Simplified API URL definition
- Using `process.env.NEXT_PUBLIC_API_URL` with fallback
- Default to `http://localhost:8000/api`

## Debugging Steps

### Step 1: Check Browser Console
1. Open browser DevTools (F12)
2. Go to Console tab
3. Look for:
   - API URLs being called
   - Response data
   - Error messages

### Step 2: Check Network Tab
1. Open browser DevTools (F12)
2. Go to Network tab
3. Reload page
4. Look for requests to:
   - `/api/products/categories/`
   - `/api/products/`
   - `/api/products/featured/`
5. Check status codes (should be 200)
6. Check response data

### Step 3: Verify Backend is Running
```bash
# Check if Django server is running
curl http://localhost:8000/api/products/categories/
# Should return category data
```

### Step 4: Verify Frontend Configuration
```bash
# Check .env.local file
cd frontend
cat .env.local
# Should contain: NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

### Step 5: Restart Servers
```bash
# Stop both servers (Ctrl+C)

# Start backend
cd backend
python manage.py runserver

# Start frontend (in new terminal)
cd frontend
npm run dev
```

## Expected Console Output

After fixes, you should see in browser console:
```
Fetching categories from: http://localhost:8000/api/products/categories/
Categories response: [{id: 1, name: "Category 1", ...}, ...]
Fetching featured products from: http://localhost:8000/api/products/featured/
Featured products response: [{id: 1, name: "Product 1", ...}, ...]
```

## Common Fixes

### Fix 1: Create .env.local
```bash
cd frontend
echo "NEXT_PUBLIC_API_URL=http://localhost:8000/api" > .env.local
# Restart Next.js dev server
```

### Fix 2: Check CORS Configuration
Make sure `backend/nextbloom/settings.py` has:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

### Fix 3: Restart Next.js Dev Server
After making changes:
1. Stop the dev server (Ctrl+C)
2. Restart: `npm run dev`
3. Clear browser cache
4. Hard refresh (Ctrl+Shift+R)

### Fix 4: Check API Response Format
The API should return:
- Categories: Array of category objects
- Products: Object with `results` array (paginated) or array directly
- Featured Products: Array of product objects

## Testing

1. **Home Page**:
   - Should show categories
   - Should show featured products
   - Check browser console for API calls

2. **Products Page**:
   - Should show all products
   - Should show categories in sidebar
   - Check browser console for API calls

3. **Network Tab**:
   - Should show successful API requests (200 status)
   - Should see response data
   - No CORS errors

## Next Steps

If still not working:
1. Check browser console for specific error messages
2. Check Network tab for failed requests
3. Verify backend is running on port 8000
4. Verify frontend is running on port 3000
5. Check CORS configuration in backend
6. Verify environment variable is set correctly

## Files Changed

- ✅ `frontend/app/page.tsx` - Added debug logging and improved error handling
- ✅ `frontend/app/products/page.tsx` - Added debug logging and improved error handling
- ✅ `frontend/app/products/[slug]/page.tsx` - Fixed API URL configuration

## Status

✅ **Backend**: Working correctly
✅ **API Endpoints**: Responding correctly
✅ **Debug Logging**: Added
⬜ **Frontend**: Need to verify with browser console

