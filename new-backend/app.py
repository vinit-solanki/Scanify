import logging
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict
import uvicorn

# Ensure environment variables are loaded regardless of launch directory
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(dotenv_path=BASE_DIR / ".env", override=False)

from pipeline import analyze_text, analyze_image

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Scanify Backend",
    description="Food label analysis API with OCR and nutrition scoring",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TextAnalysisRequest(BaseModel):
    """Request model for text-based analysis."""
    label_text: str
    mode: str = "general"

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "label_text": "Nutrition Facts\nServing Size: 100g\nCalories: 250\nFat: 5g\nProtein: 10g",
                "mode": "weight_loss",
            }
        }
    )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": "Scanify Backend"}


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "service": "Scanify Backend",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "analyze_text": "/analyze (POST with JSON)",
            "analyze_image": "/analyze (POST with form data)",
        }
    }


@app.post("/analyze")
async def analyze(request: Request, image: UploadFile | None = File(None)):
    """
    Analyze a food product label.
    
    Accepts either:
    1. JSON body with label_text and optional mode
    2. Multipart form with image file and optional mode
    
    Returns structured analysis with nutrition, health score, and recommendations.
    """
    try:
        # Image upload path
        if image is not None:
            body = await request.form()
            mode = (body.get("mode") or "general").strip()
            
            if not mode:
                mode = "general"
            
            # Validate image
            if not image.file:
                raise HTTPException(
                    status_code=400,
                    detail="Image file is empty"
                )
            
            # Check file size (max 10MB)
            file_size = image.file.seek(0, 2)  # Seek to end
            if file_size > 10 * 1024 * 1024:
                raise HTTPException(
                    status_code=413,
                    detail="Image file too large (max 10MB)"
                )
            
            image.file.seek(0)  # Reset to start
            file_data = await image.read()
            
            logger.info(f"Analyzing image with mode: {mode}, size: {file_size} bytes")
            result = analyze_image(file_data, mode=mode)
            return result
        
        # JSON text path
        payload = await request.json()
        
        if not isinstance(payload, dict):
            raise HTTPException(
                status_code=400,
                detail="Request body must be a JSON object"
            )
        
        label_text = (payload.get("label_text") or "").strip()
        mode = (payload.get("mode") or "general").strip()
        
        if not mode:
            mode = "general"
        
        if not label_text:
            raise HTTPException(
                status_code=400,
                detail="label_text is required and cannot be empty"
            )
        
        if len(label_text) > 10000:
            raise HTTPException(
                status_code=413,
                detail="label_text too long (max 10000 characters)"
            )
        
        logger.info(f"Analyzing text with mode: {mode}, length: {len(label_text)}")
        result = analyze_text(label_text, mode=mode)
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Unexpected error in /analyze: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@app.get("/modes")
async def get_modes():
    """Get available analysis modes."""
    return {
        "modes": [
            {
                "id": "general",
                "name": "General",
                "description": "Standard nutrition analysis"
            },
            {
                "id": "weight_loss",
                "name": "Weight Loss",
                "description": "Optimized for weight loss (focuses on calories, protein, fiber)"
            },
            {
                "id": "diabetes",
                "name": "Diabetes",
                "description": "Optimized for diabetes management (focuses on sugars and carbs)"
            }
        ]
    }


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Custom HTTP exception handler."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=5000,
        log_level="info"
    )
