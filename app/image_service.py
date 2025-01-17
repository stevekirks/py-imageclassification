import logging
from pathlib import Path
from sentence_transformers import SentenceTransformer, util
from PIL import Image
import torch

# define the model used
model_name = 'clip-ViT-B-32'

# set categories for the model to use
labels = [
    'public amenity',
    'tree', 
    'road',
    'road hazard or pothole',
    'street sign', 
    'graffiti', 
    'park',
    'long grass',
    'playground',
    'vehicle parking',
    'waste or rubbish',
    'animal',
    'deceased animal'
    ]

def load_model(model_path) -> tuple[SentenceTransformer, torch.Tensor]:
    # Load the model globally to avoid reloading on each function call
    en_model = SentenceTransformer(str(model_path / model_name))

    # Define the labels once for simplicity
    en_emb = en_model.encode(labels, convert_to_tensor=True)

    return en_model, en_emb
    
def classify_image(image: Image, en_model: SentenceTransformer, en_emb: torch.Tensor) -> list[tuple[str, float]]:
    # Compute embedding for the image
    img_emb = en_model.encode([image], convert_to_tensor=True)

    # Compute cosine similarity
    cos_scores = util.cos_sim(img_emb, en_emb)
    cos_scores = cos_scores.squeeze(0)  # Remove batch dimension

    # Get the top 2 predicted labels and their confidence
    top_2_indices = torch.topk(cos_scores, 2).indices.tolist()
    result = [(labels[idx], round(cos_scores[idx].item(), 3)) for idx in top_2_indices]

    return result

def save_model():
    en_model, en_emb = load_model()
    model_path = f"/volume/models/{model_name}"
    logging.info(f"Saving model to {model_path}")
    en_model.save(model_path)