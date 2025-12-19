# Scanify - Quick Deployment Guide

## 🚨 IMPORTANT: Vercel Limitations

**Vercel does NOT support Tesseract OCR** (system package). Image upload feature will NOT work.

**Recommendation:** Deploy backend to **Railway** instead.

---

## 🚂 Railway Deployment (Recommended - Full Features)

Railway supports Tesseract OCR, so **all features work** including image uploads.

### Steps:

1. **Push to GitHub** (already done)
   ```bash
   git push origin main
   ```

2. **Deploy on Railway**
   - Go to [railway.app](https://railway.app)
   - Sign in with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select `Scanify` repository
   - Railway will auto-detect and use `railway.toml`

3. **Add Environment Variable**
   - In Railway dashboard → Variables tab
   - Add: `GEMINI_API_KEY` = `your-api-key-here`

4. **Get your Railway URL**
   - Settings → Generate Domain
   - Copy URL (e.g., `https://scanify-production.up.railway.app`)

5. **Update Frontend**
   - Edit `frontend/src/lib/api.js`
   - Replace `http://localhost:5000` with Railway URL
   ```javascript
   const API_URL = "https://scanify-production.up.railway.app";
   ```

6. **Deploy Frontend to Vercel**
   ```bash
   cd frontend
   vercel --prod
   ```

---

## ⚡ Vercel Deployment (Text-Only)

If you still want Vercel (image upload won't work):

1. **Add Environment Variables in Vercel**
   ```bash
   vercel env add GEMINI_API_KEY
   ```

2. **Deploy**
   ```bash
   vercel --prod
   ```

3. **Note:** Only `/api/analyze` with JSON (text input) will work. Image uploads will fail.

---

## 🎯 Recommended Setup

**Best practice for full functionality:**

- **Backend:** Railway (supports OCR + all features)
- **Frontend:** Vercel or Netlify

**Update frontend API URL:**
```javascript
// frontend/src/lib/api.js
const API_BASE = process.env.NODE_ENV === 'production' 
  ? 'https://your-railway-app.railway.app'
  : 'http://localhost:5000';

export async function analyzeProduct({ labelText, mode = "general" }) {
  const response = await fetch(`${API_BASE}/analyze`, {
    // ... rest of code
  });
}
```

---

## 📦 Files Added for Deployment

- `vercel.json` - Vercel configuration (limited support)
- `railway.toml` - Railway configuration ✅
- `Procfile` - For platforms like Heroku
- `Aptfile` - System dependencies (Tesseract)
- `.gitignore` - Ignore sensitive/build files
- `DEPLOYMENT.md` - Detailed deployment guide

---

## 🔧 Post-Deployment Checklist

- [ ] Backend deployed and health check works (`/health`)
- [ ] Environment variable `GEMINI_API_KEY` set
- [ ] Frontend updated with production backend URL
- [ ] CORS configured (currently allows all origins - restrict in production)
- [ ] Test text analysis
- [ ] Test image upload (only works on Railway/Render/etc)

---

## 🌐 Update Frontend After Deployment

Edit `frontend/src/lib/api.js`:

```javascript
const API_BASE = "https://your-railway-app.railway.app"; // Your Railway URL

export async function analyzeProduct({ labelText, mode = "general" }) {
  const response = await fetch(`${API_BASE}/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ label_text: labelText, mode }),
  });
  return response.json();
}

export async function analyzeProductImage({ image, mode = "general" }) {
  const formData = new FormData();
  formData.append("image", image);
  formData.append("mode", mode);

  const response = await fetch(`${API_BASE}/analyze`, {
    method: "POST",
    body: formData,
  });
  return response.json();
}
```

Deploy frontend:
```bash
cd frontend
npm run build
vercel --prod
```
