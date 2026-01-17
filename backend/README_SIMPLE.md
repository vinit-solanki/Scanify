# Scanify Simple Backend

A minimal, explainable pipeline to analyze food labels from images with OCR, rule-based extraction, lightweight ontology tagging, deterministic health scoring, and optional Gemini-generated explanations.

## Overview
- OCR: Tesseract via `pytesseract` over preprocessed image.
- Extraction: Regex-based parsing of `Ingredients` and key Nutrition Facts.
- Ontology: Keyword tagging for sugars, refined grains, saturated/trans fats, sodium, etc.
- Scoring: Deterministic thresholds for `diabetes` and `weight_loss` modes, producing a 0-100 score and reasons.
- Explanation: Rule-based summary; optionally calls Gemini if `GEMINI_API_KEY` is configured.

## API
- `GET /health` → `{ status: "ok" }`
- `POST /analyze` (multipart `file`, query `mode` = `diabetes|weight_loss`)
  - Returns `{ mode, text, ingredients[], nutrition{}, tags[], risks[], score, explanation }`

## Quick Start

1. Install system Tesseract (Windows):
   - Download installer: https://github.com/UB-Mannheim/tesseract/wiki
   - After install, ensure `tesseract.exe` is in PATH or set `pytesseract.pytesseract.tesseract_cmd`.

2. Python deps (from `backend/requirements.txt`):

```bash
python -m venv .venv
. .venv/Scripts/activate
pip install -r requirements.txt
```

3. Environment (optional):
- Add to `.env` (or set in the environment):
  - `GEMINI_API_KEY=your_key`

4. Run the server:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

5. Test:

```bash
curl -X POST "http://localhost:8000/analyze?mode=diabetes" \
  -F "file=@path/to/label.jpg"
```

## Architecture
- `simple/ocr.py`: Preprocess + OCR.
- `simple/extract.py`: Parse ingredients, nutrition.
- `simple/ontology.py`: Tag ingredients by keywords.
- `simple/scoring.py`: Threshold-based scoring per mode.
- `simple/llm.py`: Rule-based or Gemini explanations.
- `pipeline.py`: Orchestrates the flow.
- `app.py`: FastAPI app exposing endpoints.

## Notes
- OCR and regex parsing are best-effort; quality depends on image clarity.
- The ontology and scoring are intentionally simple and deterministic for transparency.
- If Gemini isn't configured, explanations fall back to rule-based summaries.
