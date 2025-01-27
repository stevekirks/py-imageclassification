# Save the model to the local file system

import os
import logging
from app.image_service import save_model

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

model_path = "./data"

os.makedirs(model_path, exist_ok=True)

save_model(model_path)