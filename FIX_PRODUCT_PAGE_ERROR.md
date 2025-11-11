# Fix: Product Page Error

## Error
```
Error: Page "/products/[slug]/page" is missing exported function "generateStaticParams()", which is required with "output: export" config.
```

## Cause
The `next.config.js` had `output: 'export'` which requires Next.js to pre-generate all pages at build time. For dynamic routes like `/products/[slug]`, Next.js needs a `generateStaticParams()` function to know which pages to generate.

Since products are added dynamically through the admin panel, we can't pre-generate all product pages.

## Solution
Removed `output: 'export'` from `next.config.js`. Since all pages use `'use client'` (client-side rendering), they don't need static generation.

## Changes Made

### 1. Updated `frontend/next.config.js`
- ✅ Removed `output: 'export'`
- ✅ Removed `trailingSlash: true` (not needed without static export)
- ✅ Changed `unoptimized: false` (images can be optimized now)
- ✅ Kept client-side rendering configuration

### 2. Updated Deployment Documentation
- ✅ Updated `DEPLOYMENT.md` to use Next.js as a server
- ✅ Added Next.js systemd service configuration
- ✅ Updated Nginx configuration to proxy to Next.js server
- ✅ Updated deployment scripts

### 3. Created Deployment Guide
- ✅ Created `NEXTJS_DEPLOYMENT_OPTIONS.md` with deployment options

## Development
✅ **Fixed**: The error is now resolved. Product pages work correctly in development.

```bash
cd frontend
npm run dev
```

## Production Deployment

Since we removed static export, Next.js needs to run as a server in production.

### Option 1: Next.js as Server (Recommended)

1. **Build Next.js**:
   ```bash
   cd frontend
   npm run build
   ```

2. **Create systemd service** (see `DEPLOYMENT.md`):
   ```bash
   sudo nano /etc/systemd/system/nextbloom-frontend.service
   ```

3. **Update Nginx** to proxy to Next.js server (see `DEPLOYMENT.md`)

4. **Start services**:
   ```bash
   sudo systemctl start nextbloom-frontend
   sudo systemctl restart nginx
   ```

### Option 2: Static Export (Alternative)

If you prefer static export, you can:
1. Add `output: 'export'` back to `next.config.js`
2. Add `generateStaticParams()` to product pages (returns empty array)
3. Handle 404s client-side and fetch product data dynamically

However, Option 1 is recommended for dynamic e-commerce sites.

## Testing

1. **Development**:
   ```bash
   cd frontend
   npm run dev
   ```
   Visit: http://localhost:3000/products/organic-chicken-breast/
   ✅ Should work without errors

2. **Production**:
   - Build: `npm run build`
   - Start: `npm start`
   - Or use systemd service

## Files Changed

- ✅ `frontend/next.config.js` - Removed `output: 'export'`
- ✅ `DEPLOYMENT.md` - Updated for Next.js server deployment
- ✅ `deploy.sh` - Updated to restart Next.js service
- ✅ `Jenkinsfile` - Updated to restart Next.js service
- ✅ `NEXTJS_DEPLOYMENT_OPTIONS.md` - New deployment guide

## Next Steps

1. ✅ **Development**: Error fixed, test product pages
2. ⬜ **Production**: Set up Next.js server deployment (see `DEPLOYMENT.md`)
3. ⬜ **Testing**: Test product pages in production

## Notes

- Client-side rendered pages don't need static generation
- Dynamic routes work correctly with client-side rendering
- Next.js server deployment is better for dynamic content
- Static export is simpler but not suitable for dynamic products

