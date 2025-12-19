# Scanify Backend - Vercel Deployment

## Important Notes for Vercel Deployment

### ⚠️ OCR Limitations
Tesseract OCR is **not available** on Vercel's serverless environment. The image upload feature will **NOT work** on Vercel.

**Recommended Solutions:**
1. **Use text input only** - The JSON endpoint works perfectly
2. **Deploy backend to a different platform** that supports system packages:
   - Railway.app
   - Render.com
   - Fly.io
   - DigitalOcean App Platform
   - AWS EC2 / Lambda with layers

### Deployment Steps

1. **Set environment variable in Vercel**
   ```bash
   vercel env add GEMINI_API_KEY
   # Paste your API key when prompted
   ```

2. **Deploy to Vercel**
   ```bash
   vercel --prod
   ```

3. **Update frontend API URL**
   - Update `frontend/src/lib/api.js`
   - Replace `http://localhost:5000` with your Vercel URL

### What Works on Vercel
✅ Text-based analysis (`/api/analyze` with JSON)
✅ Health scoring
✅ AI insights with Gemini
✅ All nutrition and ingredient analysis

### What Doesn't Work on Vercel
❌ Image upload with OCR (Tesseract not available)

### Alternative: Full-Stack Deployment

**Option 1: Backend on Railway, Frontend on Vercel**
- Deploy backend to Railway (supports Tesseract)
- Deploy frontend to Vercel
- Update CORS settings to allow Vercel domain

**Option 2: Everything on Railway**
- Deploy both frontend and backend on Railway
- Supports all features including OCR

### Railway Deployment (Recommended)

1. Create `railway.toml`:
```toml
[build]
builder = "nixpacks"

[deploy]
startCommand = "cd backend && python app.py"
```

2. Add `Aptfile` for Tesseract:
```
tesseract-ocr
tesseract-ocr-eng
```

3. Push to GitHub and connect to Railway

Railway URL will be something like: `https://your-app.railway.app`
