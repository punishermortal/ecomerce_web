# Debug API Issues - Categories and Products Not Fetching

## Issue
Categories and products are not fetching in the frontend.

## Backend API Status
✅ **Working**: Backend API is responding correctly:
- Categories: `http://localhost:8000/api/products/categories/` - Returns 200 OK
- Products: `http://localhost:8000/api/products/` - Returns 200 OK
- Featured Products: `http://localhost:8000/api/products/featured/` - Should work

## Possible Causes

### 1. API URL Configuration
Check if `NEXT_PUBLIC_API_URL` is set correctly in frontend.

**Check:**
```bash
# In frontend directory
cat .env.local
# Should contain:
# NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

**Fix:**
```bash
cd frontend
echo "NEXT_PUBLIC_API_URL=http://localhost:8000/api" > .env.local
```

### 2. CORS Issues
Backend CORS is configured for `localhost:3000`. Check if frontend is running on correct port.

**Check:**
- Frontend should run on `http://localhost:3000`
- Backend should run on `http://localhost:8000`

### 3. Backend Server Not Running
Make sure Django backend is running.

**Check:**
```bash
cd backend
python manage.py runserver
# Should show: Starting development server at http://127.0.0.1:8000/
```

### 4. Network Errors
Check browser console for network errors.

**Check:**
1. Open browser DevTools (F12)
2. Go to Network tab
3. Reload page
4. Look for failed requests to `/api/products/` or `/api/products/categories/`

### 5. Environment Variable Not Loaded
Next.js might not be reading the environment variable.

**Fix:**
1. Restart Next.js dev server after creating/updating `.env.local`
2. Make sure `.env.local` is in `frontend/` directory
3. Variable name must start with `NEXT_PUBLIC_`

## Debugging Steps

### Step 1: Check API URL
```javascript
// In browser console, check:
console.log(process.env.NEXT_PUBLIC_API_URL)
// Should output: http://localhost:8000/api
```

### Step 2: Test API Directly
```bash
# Test categories endpoint
curl http://localhost:8000/api/products/categories/

# Test products endpoint
curl http://localhost:8000/api/products/

# Test featured products endpoint
curl http://localhost:8000/api/products/featured/
```

### Step 3: Check Browser Console
1. Open browser DevTools (F12)
2. Go to Console tab
3. Look for error messages
4. Check Network tab for failed requests

### Step 4: Check Backend Logs
Check Django server console for errors:
```bash
# In backend terminal, look for:
# - Request logs
# - Error messages
# - CORS errors
```

## Added Debug Logging

I've added console.log statements to help debug:
- `fetchFeaturedProducts()` - Logs API URL and response
- `fetchCategories()` - Logs API URL and response
- `fetchProducts()` - Logs API URL, params, and response

**Check browser console for:**
- API URLs being called
- Response data
- Error messages

## Common Fixes

### Fix 1: Create .env.local
```bash
cd frontend
echo "NEXT_PUBLIC_API_URL=http://localhost:8000/api" > .env.local
# Restart Next.js dev server
```

### Fix 2: Restart Servers
```bash
# Stop both servers (Ctrl+C)
# Start backend
cd backend
python manage.py runserver

# Start frontend (in new terminal)
cd frontend
npm run dev
```

### Fix 3: Check CORS
Make sure backend `settings.py` has:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

### Fix 4: Clear Browser Cache
- Clear browser cache
- Hard refresh (Ctrl+Shift+R)
- Try incognito mode

## Testing

After fixes, test:
1. Home page - Should show categories and featured products
2. Products page - Should show all products and categories
3. Browser console - Should show API calls and responses
4. Network tab - Should show successful API requests

## Next Steps

1. ✅ Check `.env.local` exists and has correct API URL
2. ✅ Restart Next.js dev server
3. ✅ Check browser console for errors
4. ✅ Check Network tab for failed requests
5. ✅ Verify backend is running
6. ✅ Test API endpoints directly with curl

## Expected Behavior

After fixes:
- Categories should load on home page
- Featured products should load on home page
- All products should load on products page
- Categories should load in sidebar filter
- No errors in browser console
- Successful API requests in Network tab

