# api.py
# FastAPI service that exposes the threat model with simple security.

from pathlib import Path
from typing import Dict
import time
import logging

import joblib
from fastapi import FastAPI, HTTPException, Header, Request
from pydantic import BaseModel

# Settings
API_KEY = "YOUR_KEY_HERE"
MAX_TEXT_LENGTH = 1000          # prevent very large inputs
RATE_LIMIT_MAX = 30             # max requests per window
RATE_LIMIT_WINDOW = 60          # window in seconds

# Load model
model_path = Path("models") / "threat_model.joblib"
if not model_path.exists():
    raise RuntimeError("Model file not found. Run train_threat_model.py first.")

model = joblib.load(model_path)

# Logging setup
logs_path = Path("logs")
logs_path.mkdir(exist_ok=True)
log_file = logs_path / "api.log"

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

# Basic in memory rate limiter
client_calls: Dict[str, list] = {}

# FastAPI app
app = FastAPI(title="Secure Threat Classifier API")


class ThreatRequest(BaseModel):
    text: str


class ThreatResponse(BaseModel):
    label: str
    note: str


def check_api_key(x_api_key: str | None):
    """Check that the client sent the correct API key."""
    if x_api_key is None:
        raise HTTPException(status_code=401, detail="Missing API key")
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")


def check_rate_limit(client_id: str):
    """Very simple rate limit per client id."""
    now = time.time()
    calls = client_calls.get(client_id, [])
    # Keep calls only inside the current window
    calls = [t for t in calls if now - t <= RATE_LIMIT_WINDOW]
    if len(calls) >= RATE_LIMIT_MAX:
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please slow down."
        )
    calls.append(now)
    client_calls[client_id] = calls


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_host = request.client.host if request.client else "unknown"
    try:
        check_rate_limit(client_host)
    except HTTPException as e:
        logging.warning(f"RATE_LIMIT | {client_host} | {e.detail}")
        raise
    response = await call_next(request)
    return response


@app.post("/predict", response_model=ThreatResponse)
async def predict_threat(
    body: ThreatRequest,
    x_api_key: str | None = Header(default=None),
    request: Request = None
):
    # Check key
    check_api_key(x_api_key)

    client_host = request.client.host if request and request.client else "unknown"
    text = body.text.strip()

    if not text:
        raise HTTPException(status_code=400, detail="Text is empty.")

    if len(text) > MAX_TEXT_LENGTH:
        raise HTTPException(
            status_code=400,
            detail=f"Text too long. Max length is {MAX_TEXT_LENGTH} characters."
        )

    # Make prediction
    try:
        label = model.predict([text])[0]
    except Exception as e:
        logging.error(f"PREDICT_ERROR | {client_host} | {str(e)}")
        raise HTTPException(status_code=500, detail="Prediction error.")

    # Log the request
    logging.info(f"PREDICT | {client_host} | {label} | {text[:200]}")

    return ThreatResponse(
        label=label,
        note="Demo model. Use with human review, not as the only decision maker."
    )


@app.get("/health")
async def health_check():
    return {"status": "ok"}
