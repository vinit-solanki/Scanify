# Scanify - AI Food Label Analyzer

AI-powered food label analysis system that extracts nutrition facts, analyzes ingredients, and provides personalized health insights.

## Features

- 📸 **OCR Label Scanning** - Upload food label images for automatic text extraction
- 📝 **Text Analysis** - Paste ingredient lists and nutrition facts for instant analysis
- 🧠 **AI Health Insights** - Get personalized health recommendations using Gemini AI
- 🎯 **Multi-Mode Analysis** - General, Diabetes, and Weight Loss modes
- 🔬 **Ingredient Intelligence** - Identifies additives, allergens, and processing levels
- 📊 **Health Scoring** - Automated health category and score calculation

## Tech Stack

### Backend
- **Python 3.x** with Flask
- **Google Gemini AI** for health explanations
- **Tesseract OCR** for label text extraction
- **OpenCV & Pillow** for image preprocessing

### Frontend
- **React** with Vite
- **TailwindCSS** for styling
- **Aceternity UI** components
- **React Router** for navigation

## Setup Instructions

### Backend Setup

1. **Navigate to backend folder**
   ```powershell
   cd backend
   ```

2. **Install Python dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Install Tesseract OCR**
   - Download from: https://github.com/UB-Mannheim/tesseract/wiki
   - Default install path: `C:\Program Files\Tesseract-OCR\`
   - Update path in `backend/vision/ocr_agent.py` if different

4. **Configure environment variables**
   - Copy [backend/.env.example](backend/.env.example) to `backend/.env`
   - Get your Gemini API key from: https://aistudio.google.com/app/apikey
   - Set `GEMINI_API_KEY` in `backend/.env`
   - `.env` files are ignored by git; do not commit real secrets

5. **Start the backend server**
   ```powershell
   python app.py
   ```
   - Server runs at `http://localhost:5000`
   - Test with: `http://localhost:5000/health`

### Frontend Setup

1. **Navigate to frontend folder**
   ```powershell
   cd frontend
   ```

2. **Install Node.js dependencies**
   ```powershell
   npm install
   ```

3. **Start the development server**
   ```powershell
   npm run dev
   ```
   - Frontend runs at `http://localhost:5173` (or similar)
   - Open in browser to use the app

## Usage

### Image Upload Mode
1. Click "Upload Food Label Image"
2. Select or drag a clear photo of a food label
3. Wait for OCR extraction and AI analysis
4. View health insights, nutrition facts, and recommendations

### Text Input Mode
1. Click "Paste Label Text"
2. Enter ingredients list and nutrition facts
3. Click "Analyze Label"
4. Get instant health analysis

### Analysis Modes
- **General** - Standard health analysis for everyone
- **Diabetes** - Focus on sugar, carbs, and glycemic impact
- **Weight Loss** - Emphasis on calories, fats, and portion control

## API Endpoints

### `GET /health`
Health check endpoint
- Returns: `{"status": "ok"}`

### `POST /analyze`
Main analysis endpoint

**JSON Mode** (text input):
```json
{
  "label_text": "Ingredients: flour, sugar...\nNutrition: Calories 150...",
  "mode": "general"
}
```

**Multipart Mode** (image upload):
```
FormData:
  image: <file>
  mode: "general"
```

**Response**:
```json
{
  "is_valid": true,
  "ingredients": {...},
  "nutrition": {...},
  "semantic_ingredients": {...},
  "nutrition_normalized": {...},
  "health": {
    "health_score": 43,
    "health_category": "Harmful",
    "penalties": {...}
  },
  "explanation": "AI-generated health insights..."
}
```

## Project Structure

```
backend/
├── app.py                 # Flask API server
├── pipeline.py            # Analysis pipeline orchestrator
├── main.py               # CLI runner (for testing)
├── .env                  # Environment variables (Gemini API key)
├── agents/               # Classification agents
├── extraction/           # Text and nutrition extractors
├── health/              # Health scoring engine
├── intelligence/        # Ingredient classification
├── llm/                 # Gemini AI integration
├── nutrition/           # Nutrition normalization
├── ontology/            # Ingredient ontology
├── schemas/             # Data schemas
├── validation/          # Label validation
└── vision/              # OCR and image processing

frontend/
├── src/
│   ├── pages/
│   │   ├── LandingPage.jsx
│   │   └── ProductScan.jsx    # Main analysis UI
│   ├── components/            # Reusable UI components
│   ├── lib/
│   │   ├── api.js            # Backend API calls
│   │   └── transformResponse.js  # Response transformation
│   └── App.jsx
└── package.json
```

## Development

### Running Tests
```powershell
# Backend - test with sample image
cd backend
python main.py
```

### Debugging
- Backend logs errors to console
- Frontend errors appear in browser console
- Check network tab for API request/response details

## Notes

- Tesseract path may need adjustment based on your installation
- Gemini API has rate limits on free tier
- Image quality affects OCR accuracy - use clear, well-lit photos
- Text mode is faster than image mode (no OCR needed)

### Security: Removing leaked `.env` from Git history

If a `.env` was committed by mistake:

1. Stop tracking the file and add to `.gitignore`:
   ```powershell
   git rm --cached backend/.env
   git commit -m "Stop tracking backend .env and ignore env files"
   git push
   ```
2. Rotate your API key in Google AI Studio.
3. Purge the secret from repository history using one of:
   - BFG Repo-Cleaner (Windows-friendly): https://rtyley.github.io/bfg-repo-cleaner/
   - git-filter-repo (official): https://github.com/newren/git-filter-repo

Example using BFG with a mirror clone:
```powershell
git clone --mirror https://github.com/<owner>/<repo>.git
cd <repo>.git
java -jar bfg.jar --delete-files .env
git reflog expire --expire-unreachable=now --all
git gc --prune=now --aggressive
git push --force
```

## License

MIT
