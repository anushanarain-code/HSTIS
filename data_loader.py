import json
from pathlib import Path

LIBRARY_DIR = Path("libraries")

def load_library(filename: str):
    path = LIBRARY_DIR / filename
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)