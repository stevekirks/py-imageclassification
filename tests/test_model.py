# Requires a locally available model (see README)

import pytest
from PIL import Image
from app.image_service import load_model_and_labels, classify_image

model_path = "./data/models"
en_model, en_emb = load_model_and_labels(model_path)

samples_path = "./tests/samples"

@pytest.mark.parametrize("image_name, expected_label", [
    ('tree.jpg', 'tree'),
    ('car_parking.jpg', 'vehicle parking'),
])
def test_model_chooses_correct_labels(image_name, expected_label):
    image = Image.open(f"{samples_path}/{image_name}")

    pred_labels = classify_image(image, en_model, en_emb)

    assert len(pred_labels) > 0
    label, confidence = pred_labels[0]
    assert label == expected_label
