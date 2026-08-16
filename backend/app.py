import sys, io as _io, os
sys.stdout = _io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = _io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import tensorflow as tf
import numpy as np
from PIL import Image
import io

# ── App setup ─────────────────────────────────────────────────────────────────
app = FastAPI(
    title="AI Image Detector API",
    description="Detects whether an uploaded image is AI-generated (FAKE) or real (REAL).",
    version="1.0.0",
)

# Allow all origins so the frontend (served from any origin/file://) can call us
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Model loading ──────────────────────────────────────────────────────────────
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "best_model.keras")
IMG_SIZE = (32, 32)   # Must match the size used during training

print(f"[startup] Loading model from {MODEL_PATH}")
model = tf.keras.models.load_model(MODEL_PATH)
print("[startup] Model loaded successfully [OK]")


from fastapi.staticfiles import StaticFiles

FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")



@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Upload an image (PNG / JPG / WEBP …) and receive a prediction.

    Returns:
        prediction  – "FAKE" or "REAL"
        confidence  – probability score (0 – 1) for the predicted class
        raw_score   – raw model output (probability of FAKE)
    """
    # Validate MIME type loosely
    if file.content_type and not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")

    try:
        image_bytes = await file.read()
        image = (
            Image.open(io.BytesIO(image_bytes))
            .convert("RGB")
            .resize(IMG_SIZE, Image.Resampling.BILINEAR)
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Could not read image: {exc}")

    # Pre-process: model architecture contains internal Rescaling(1./255) layer
    image_array = np.array(image, dtype=np.float32)
    image_array = np.expand_dims(image_array, axis=0)   # (1, 32, 32, 3)

    raw_score = float(model.predict(image_array, verbose=0)[0][0])
    prediction = "FAKE" if raw_score >= 0.5 else "REAL"
    confidence = round(raw_score if prediction == "FAKE" else 1.0 - raw_score, 4)

    return {
        "prediction": prediction,
        "confidence": confidence,
        "raw_score": round(raw_score, 6),
    }


# Serve frontend static files at root (html=True serves index.html)
if os.path.exists(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")

