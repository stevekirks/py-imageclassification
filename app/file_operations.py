from pathlib import Path

def read_file(file_path: Path) -> str:
    """Reads content from a file in the volume."""
    with open(file_path, "r") as f:
        return f.read()
