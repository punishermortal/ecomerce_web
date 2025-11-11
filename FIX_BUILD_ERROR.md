# Fix: Module not found '@/lib/axios'

## Error
```
Module not found: Can't resolve '@/lib/axios'
```

## Solution

The file exists at `frontend/lib/axios.ts`, but Next.js can't resolve it. This is usually a caching issue.

### Step 1: Clear Next.js Cache

```bash
cd frontend
rm -rf .next
# Or on Windows:
# Remove-Item -Recurse -Force .next
```

### Step 2: Restart Dev Server

```bash
# Stop the server (Ctrl+C)
# Then restart
npm run dev
```

### Step 3: Verify File Exists

```bash
# Check if file exists
ls lib/axios.ts
# Or on Windows:
# Test-Path lib/axios.ts
```

### Step 4: Verify TypeScript Config

Make sure `tsconfig.json` has:
```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./*"]
    }
  }
}
```

## Alternative: Use Relative Import (Temporary Fix)

If the alias still doesn't work, you can use a relative import:

```typescript
// Change from:
import api from '@/lib/axios'

// To:
import api from '../../lib/axios'
```

## Verification

After clearing cache and restarting, the build should succeed. The file `frontend/lib/axios.ts` exists and is correctly configured.

## Status

✅ File exists: `frontend/lib/axios.ts`
✅ TypeScript config: Path alias configured
✅ Other files: Using same import pattern successfully
⬜ Build cache: Cleared
⬜ Dev server: Needs restart

