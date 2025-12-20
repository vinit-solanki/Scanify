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

# CORS configuration - allow all origins for now (restrict in production)
CORS(app, resources={
    r"/*": {
        "origins": ["*"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})


@app.get("/")
@app.get("/health")
def health():
    # Report basic LLM configuration status without exposing secrets
    llm_disabled = (os.getenv("DISABLE_LLM", "0") in ("1", "true", "True"))
    gemini_present = bool(os.getenv("GEMINI_API_KEY"))
    google_present = bool(os.getenv("GOOGLE_API_KEY"))
    llm_source = (
        "disabled" if llm_disabled else
        "gemini" if gemini_present else
        "google" if google_present else
        "none"
    )

    return jsonify({
        "status": "ok",
        "message": "Scanify API is running",
        "llm": {
            "configured": (not llm_disabled) and (gemini_present or google_present),
            "source": llm_source
        }
    })


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
                text_blocks = extract_text_blocks(tmp_path)
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
    app.run(host="0.0.0.0", port=port, debug=True)
