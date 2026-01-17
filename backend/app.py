from fastapi import FastAPI, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from pipeline import analyze_image

app = FastAPI(title="Scanify Simple Backend", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze")
async def analyze(file: UploadFile = File(...), mode: str = Query("diabetes", enum=["diabetes", "weight_loss"])):
    data = await file.read()
    result = analyze_image(data, mode=mode)
    return result


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

import os
from pathlib import Path
from tempfile import NamedTemporaryFile

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load env BEFORE importing modules that may read it at import time
# Try loading .env.production for production, fall back to .env for development
env_file = Path(__file__).resolve().parent / (".env.production" if os.getenv("FLASK_ENV") == "production" else ".env")
if env_file.exists():
    load_dotenv(dotenv_path=env_file)

from pipeline import run_pipeline_from_text, run_pipeline_from_blocks
from vision.ocr_agent import extract_text_blocks

app = Flask(__name__)

# CORS configuration - allow all origins for development
CORS(app, resources={
    r"/*": {
        "origins": ["*", "http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})


@app.get("/")
@app.get("/health")
def health():
    return jsonify({"status": "ok", "message": "Scanify API is running"})


@app.post("/api/analyze")
@app.post("/analyze")
def analyze():
    mode = request.values.get("mode", "general")

    try:
        if request.is_json:
            payload = request.get_json(silent=True) or {}
            label_text = (payload.get("label_text") or "").strip()
            if not label_text:
                return jsonify({"error": "label_text is required in JSON body"}), 400
            result = run_pipeline_from_text(label_text, mode=mode)
            return jsonify(result)

        if "image" in request.files:
            file = request.files["image"]
            if not file or file.filename == "":
                return jsonify({"error": "image file is missing"}), 400

            # Save to a temporary file for OCR
            with NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp:
                file.save(tmp.name)
                tmp_path = tmp.name
            try:
                # Allow overriding engine via query/form param; fallback to env
                ocr_engine = request.values.get("ocr", os.getenv("OCR_ENGINE", "tesseract")).lower()
                text_blocks = extract_text_blocks(tmp_path, engine=ocr_engine)
            finally:
                try:
                    os.remove(tmp_path)
                except Exception:
                    pass

            result = run_pipeline_from_blocks(text_blocks, mode=mode)
            return jsonify(result)

        return jsonify({"error": "Unsupported request. Send JSON {label_text, mode} or multipart/form-data with image."}), 400

    except Exception as e:
        # Surface errors with a message
        return jsonify({"error": str(e)}), 500


# Vercel serverless function handler
def handler(request):
    with app.request_context(request.environ):
        return app.full_dispatch_request()


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)
