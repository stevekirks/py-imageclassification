from pathlib import Path
from PIL import Image

def get_image_size(file_path: Path) -> tuple:
    """Returns the width and height of an image file."""
    with Image.open(file_path) as img:
        return img.size
