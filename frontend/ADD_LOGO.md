# Add Your NextBloom Logo

## Quick Setup

1. **Save your NEX BLOOMS logo** as `logo.png` in the `frontend/public/` folder
   - Location: `frontend/public/logo.png`
   - Recommended: 512x512px or larger (square format)
   - Format: PNG with transparent background (best) or JPG

2. **Restart your Next.js server:**
   ```bash
   npm run dev
   ```

3. **The logo will automatically appear in:**
   - ✅ Navbar (top left, 48x48px circular)
   - ✅ Footer (64x64px circular)
   - ✅ Homepage hero section (128-160px circular with white border)

## Logo Specifications

- **Navbar**: 48x48px circular with light border
- **Footer**: 64x64px circular with accent border
- **Hero**: 128-160px circular with white border and shadow
- **Style**: All logos are displayed in circular frames
- **Background**: White background for better visibility

## File Structure

```
frontend/
  └── public/
      └── logo.png  ← Place your logo here
```

## Alternative Formats

If your logo is in a different format:
- `logo.jpg` - Update `src="/logo.png"` to `src="/logo.jpg"` in components
- `logo.svg` - Best for scalability, update image source in components

## Testing

After adding the logo:
1. The logo should appear automatically
2. If the image doesn't load, check the browser console for errors
3. Make sure the file is named exactly `logo.png` (case-sensitive on some systems)

## Current Implementation

The logo is integrated using Next.js Image component with:
- ✅ Optimized loading
- ✅ Responsive sizing
- ✅ Circular display
- ✅ Proper borders and styling
- ✅ Priority loading on homepage

Enjoy your branded NextBloom website! 🎉

