# Scanify Backend

A production-ready FastAPI backend for food label analysis with OCR, nutrition parsing, and AI-powered health scoring.

## Features

- **OCR Text Extraction**: Automatically extract text from food label images using Tesseract
- **Nutrition Parsing**: Intelligently parse nutrition facts from raw text
- **Semantic Analysis**: Detect allergens, additives, and processing indicators
- **Health Scoring**: Calculate personalized health scores based on nutritional content
- **Multiple Modes**: Support for general, weight loss, and diabetes management modes
- **AI Explanations**: Generate detailed explanations using Google Gemini (optional)
- **CORS Enabled**: Works seamlessly with frontend applications
- **Error Handling**: Comprehensive error handling and validation

## Architecture

```
new-backend/
├── app.py           # FastAPI application
├── pipeline.py      # Main analysis pipeline
├── extract.py       # Nutrition and ingredient extraction
├── ocr.py          # OCR text extraction
├── ontology.py     # Semantic ingredient analysis
├── scoring.py      # Health score calculation
├── llm.py          # AI explanation generation
├── schemas.py      # Pydantic data models
└── requirement.txt # Python dependencies
```

## Installation

### Prerequisites

- Python 3.10+
- Tesseract OCR (for image analysis)

### Windows Installation

1. **Install Tesseract OCR**:
   - Download installer: https://github.com/UB-Mannheim/tesseract/wiki
   - Default installation path: `C:\Program Files\Tesseract-OCR\tesseract.exe`

2. **Clone and setup**:
   ```bash
   cd new-backend
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirement.txt
   ```

### Linux/Mac Installation

1. **Install Tesseract**:
   ```bash
   # macOS
   brew install tesseract
   
   # Ubuntu/Debian
   sudo apt-get install tesseract-ocr
   ```

2. **Setup**:
   ```bash
   cd new-backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirement.txt
   ```

## Configuration

Create a `.env` file in the project root:

```env
# Server Configuration
PORT=5000
FLASK_ENV=development

# OCR Configuration
TESSERACT_PATH=C:\Program Files\Tesseract-OCR\tesseract.exe
OCR_ENGINE=tesseract

# Google Gemini API (Optional - for AI explanations)
GEMINI_API_KEY=your_api_key_here

# Upload Configuration
UPLOAD_FOLDER=uploads
OLMOCR_MAX_NEW_TOKENS=512
```

## Running the Backend

### Development Mode
```bash
python app.py
# Server runs at http://localhost:5000
```

### With Uvicorn (Production-style)
```bash
uvicorn app:app --host 0.0.0.0 --port 5000 --reload
```

## API Endpoints

### Health Check
```
GET /health
```
Returns: `{"status": "ok", "service": "Scanify Backend"}`

### Root Endpoint
```
GET /
```
Returns service info and available endpoints.

### Analyze Product

**Text Analysis**:
```
POST /analyze
Content-Type: application/json

{
  "label_text": "Nutrition Facts\nServing Size: 100g\nCalories: 250\n...",
  "mode": "weight_loss"
}
```

**Image Analysis**:
```
POST /analyze
Content-Type: multipart/form-data

image: <binary file data>
mode: weight_loss
```

**Response**:
```json
{
  "is_valid": true,
  "mode": "weight_loss",
  "raw_text": "Nutrition Facts...",
  "semantic_ingredients": {
    "raw_ingredients": ["sugar", "wheat flour", ...],
    "canonical_ingredients": [...],
    "allergens": ["wheat"],
    "additives": [],
    "processing_indicators": ["refined"]
  },
  "nutrition_normalized": {
    "serving_size_g": 100,
    "serving_size_description": "1 cup (100g)",
    "nutrition_per_100g": {
      "calories": 250,
      "protein_g": 8,
      "sugars_g": 12,
      "dietary_fiber_g": 2,
      ...
    }
  },
  "health": {
    "health_score": 65.2,
    "health_category": "Good",
    "penalties": {
      "high_calories": 30
    },
    "recommendations": [
      "Consider lower-calorie alternatives",
      "Choose products with more protein"
    ]
  },
  "overall_confidence": 0.85,
  "explanation": "This product scores 65/100 in weight loss mode..."
}
```

### Analysis Modes
```
GET /modes
```

Returns available modes:
- **general**: Standard nutrition analysis
- **weight_loss**: Optimized for weight management (focuses on calories, protein, fiber)
- **diabetes**: Optimized for diabetes management (focuses on sugars and carbs)

## Response Format

The API returns a structured JSON response that matches the frontend expectations:

| Field | Type | Description |
|-------|------|-------------|
| `is_valid` | boolean | Whether analysis was successful |
| `mode` | string | Analysis mode used |
| `semantic_ingredients` | object | Allergens, additives, processing info |
| `nutrition_normalized` | object | Nutrition facts normalized to per 100g |
| `health` | object | Health score and recommendations |
| `overall_confidence` | float | Confidence in analysis (0-1) |
| `explanation` | string | Human-readable explanation |

## Error Handling

The API returns appropriate HTTP status codes:

- `200 OK`: Successful analysis
- `400 Bad Request`: Invalid input (missing label_text, empty image, etc.)
- `413 Payload Too Large`: File too large (max 10MB) or text too long (max 10000 chars)
- `500 Internal Server Error`: Unexpected server error

Error responses include detailed messages:
```json
{
  "error": "label_text is required and cannot be empty",
  "status_code": 400
}
```

## Development

### Running Tests (if added)
```bash
pytest tests/
```

### Code Structure

- **app.py**: FastAPI setup, route handling, CORS configuration
- **pipeline.py**: Orchestrates the analysis workflow
- **extract.py**: Parses nutrition facts and ingredients from text
- **ocr.py**: Handles image-to-text conversion
- **ontology.py**: Semantic analysis (allergens, additives, processing)
- **scoring.py**: Calculates health scores based on nutrition
- **llm.py**: Generates AI-powered explanations
- **schemas.py**: Pydantic models for type validation

## Performance Tips

1. **Optimize Images**: Send clear, well-lit images for better OCR accuracy
2. **Cache Results**: Consider caching analysis results on the frontend
3. **Async Processing**: The API uses async/await for non-blocking I/O
4. **Timeout Configuration**: OCR can take 2-5 seconds for complex labels

## Troubleshooting

### Tesseract Not Found
```
FileNotFoundError: tesseract is not installed
```
**Solution**: Install Tesseract and set `TESSERACT_PATH` in `.env`

### Poor OCR Quality
- Ensure images are clear and well-lit
- Avoid skewed or rotated text
- Use high-resolution images (300+ DPI recommended)

### Gemini API Errors
- Verify `GEMINI_API_KEY` is correct
- Check API quota and billing
- Backend falls back to rule-based explanations if API unavailable

## Integration with Frontend

The response format is designed to work with the frontend's `transformResponse.js`:

```javascript
import { transformAnalysisToScanResult } from "../lib/transformResponse";

const data = await analyzeProduct({ labelText, mode });
const transformed = transformAnalysisToScanResult(data);
```

## Deployment

### Docker (if using Docker)
```bash
docker build -t scanify-backend .
docker run -p 5000:5000 -e GEMINI_API_KEY=<key> scanify-backend
```

### Render.com / Heroku
- Ensure `Procfile` is configured
- Set environment variables in deployment settings
- Platform should handle Tesseract installation

## License

Proprietary - Scanify Project

## Support

For issues or questions, check:
1. The troubleshooting section above
2. Backend logs (set `log_level=info` in `app.py`)
3. Frontend integration with `transformResponse.js`
