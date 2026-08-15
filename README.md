# AI Image Detector

A full-stack AI image authenticity detector — upload any image and the trained CNN model instantly predicts whether it was AI-generated or a real photograph.

---

## Project Structure

```
AI VS REAL IMAGE/
├── best_model.keras        ← trained CNN model
├── backend/
│   ├── app.py              ← FastAPI prediction server
│   ├── requirements.txt    ← Python dependencies
│   └── start.bat           ← one-click server launcher (Windows)
├── frontend/
│   └── index.html          ← drag-and-drop UI (open in browser)
├── train/  FAKE / REAL
└── test/   FAKE / REAL
```

---

## Quick Start

### 1. Install backend dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Start the API server

```bash
# from the project root  (AI VS REAL IMAGE/)
cd backend
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Or double-click **`backend/start.bat`**.

The server will:
- Load `best_model.keras` from the project root
- Expose `http://127.0.0.1:8000/predict`

### 3. Open the frontend

Open `frontend/index.html` in any modern browser.
- Click **Test Connection** to verify the backend is running
- Drag-and-drop or click to upload any image
- Hit **Analyse Image** to get the verdict

---

## API Reference

### `GET /health`
Returns `{"status": "healthy"}` — used by the frontend to check connectivity.

### `POST /predict`
| Field | Type | Description |
|-------|------|-------------|
| `file` | `multipart/form-data` image | Image to classify |

**Response:**
```json
{
  "prediction": "FAKE",
  "confidence": 0.9312,
  "raw_score": 0.9312
}
```

---

## Deploying the Backend (Live on Internet)

| Platform | Notes |
|----------|-------|
| **Render** | Free tier — connect GitHub repo, set start command |
| **Railway** | Free tier — easy Python deployment |
| **Hugging Face Spaces** | Best for ML models; free CPU/GPU |

After deploying, update the **API Endpoint** field in the frontend to your live URL.
