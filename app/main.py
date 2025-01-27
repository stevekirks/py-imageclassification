from io import BytesIO
import os
from fastapi import FastAPI, File, UploadFile, HTTPException, Header, Depends
from pathlib import Path
from PIL import Image
import logging
from .image_service import load_model_and_labels, classify_image

async def verify_api_key(x_api_key: str = Header(...)):
    expected_api_key = os.getenv("IMGDET_API_KEY", "myapikey321")
    if x_api_key != expected_api_key:
        raise HTTPException(status_code=403, detail="Invalid API Key")

app = FastAPI()

volume_path = Path("/volume")

# Set up logging
log_path = volume_path / "logs"
if not os.path.exists(log_path):
    os.makedirs(log_path)
logging.basicConfig(
    filename=log_path / "app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Set up model once on startup
try:
    model_path = volume_path / "models"
    logger.info(f"Loading model from {model_path}")
    en_model, en_emb = load_model_and_labels(model_path)
except Exception as e:
    logger.error(f"Error loading model: {e}", exc_info=True)

@app.get("/test")
async def test_endpoint(api_key: str = Depends(verify_api_key)):
    logger.info("Test endpoint accessed.")
    return {"message": "Test endpoint working!!"}

@app.post("/image-classify")
async def image_size(file: UploadFile = File(...), api_key: str = Depends(verify_api_key)):
    logger.info("Received image. Processing...")
    try:
        # Parse image bytes from the request
        img_bytes = await file.read()
        image = Image.open(BytesIO(img_bytes))

        pred_labels = classify_image(image, en_model, en_emb)

        # Return the prediction as JSON
        return {"predicted_labels": [{"label": label, "confidence": confidence} for label, confidence in pred_labels]}
    except Exception as e:
        logger.error(f"Error processing image: {e}")
        raise HTTPException(status_code=500, detail="Failed to process image.")
