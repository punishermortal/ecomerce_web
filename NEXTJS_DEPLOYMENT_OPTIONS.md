# Next.js Deployment Options

## Issue Fixed

The error `Page "/products/[slug]/page" is missing exported function "generateStaticParams()"` occurred because we had `output: 'export'` in `next.config.js`, which requires static generation for all routes.

Since all pages use `'use client'` (client-side rendering) and products are dynamically added through the admin panel, we've removed `output: 'export'`.

## Development

✅ **Fixed**: Development mode now works without errors. Just run:
```bash
npm run dev
```

## Production Deployment Options

Since we removed `output: 'export'`, you have two options for production:

### Option 1: Run Next.js as a Server (Recommended)

This allows dynamic routes to work properly.

#### Update Nginx Configuration

```nginx
upstream django {
    server 127.0.0.1:8000;
}

upstream nextjs {
    server 127.0.0.1:3000;
}

server {
    listen 80;
    server_name 21.2.23.24;

    # Frontend (Next.js)
    location / {
        proxy_pass http://nextjs;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # Backend API
    location /api {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Admin
    location /admin {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Media files
    location /media {
        alias /var/www/nextbloom/backend/media;
    }

    # Static files
    location /static {
        alias /var/www/nextbloom/backend/staticfiles;
    }
}
```

#### Create Next.js Systemd Service

```bash
sudo nano /etc/systemd/system/nextbloom-frontend.service
```

Add:
```ini
[Unit]
Description=NextBloom Next.js Application
After=network.target

[Service]
User=xyzxtz
Group=xyzxtz
WorkingDirectory=/var/www/nextbloom/frontend
Environment="PATH=/usr/bin:/usr/local/bin"
Environment="NODE_ENV=production"
Environment="NEXT_PUBLIC_API_URL=http://21.2.23.24/api"
ExecStart=/usr/bin/npm start
Restart=always

[Install]
WantedBy=multi-user.target
```

#### Update Deployment Script

The `deploy.sh` script should:
1. Build Next.js: `npm run build`
2. Start Next.js service: `sudo systemctl restart nextbloom-frontend`

### Option 2: Use Static Export with Fallback (Alternative)

If you prefer static export, you can add `output: 'export'` back but handle dynamic routes differently.

#### Update next.config.js

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: 'export',
  images: {
    domains: ['localhost', '127.0.0.1', '21.2.23.24'],
    unoptimized: true,
  },
  trailingSlash: true,
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api',
  },
  // Disable static optimization for dynamic routes
  experimental: {
    missingSuspenseWithCSRBailout: false,
  },
}
```

#### Update Product Detail Page

Since static export can't pre-render dynamic routes, the page will need to handle 404s and redirect to a client-side route handler.

## Recommended: Option 1 (Next.js as Server)

**Advantages**:
- ✅ Dynamic routes work properly
- ✅ Better for SEO (server-side rendering possible)
- ✅ No need for `generateStaticParams()`
- ✅ Works with dynamic products

**Disadvantages**:
- Requires Node.js server running
- Slightly more complex setup

## Quick Fix for Development

The error is now fixed for development. The product pages will work correctly in development mode.

For production, choose one of the options above. Option 1 is recommended for a production e-commerce site with dynamic products.

## Update Deployment Files

If using Option 1, update:
1. `DEPLOYMENT.md` - Add Next.js service setup
2. `deploy.sh` - Add Next.js service restart
3. `Jenkinsfile` - Add Next.js service management
4. Nginx configuration - Proxy to Next.js server

## Current Status

✅ **Development**: Fixed - Works without errors
⬜ **Production**: Choose deployment option above

