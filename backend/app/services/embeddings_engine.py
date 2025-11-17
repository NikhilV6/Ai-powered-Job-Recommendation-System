from sentence_transformers import SentenceTransformer
import numpy as np

MODEL_NAME = "all-MiniLM-L6-v2"

# Lazy-load model so it's not loaded on import
_model = None

def get_model():
    global _model
    if _model is None:
        print("Loading SentenceTransformer model...")
        _model = SentenceTransformer(MODEL_NAME)
    return _model

def encode_text(text: str):
    model = get_model()
    vec = model.encode(text, show_progress_bar=False)
    return np.array(vec, dtype="float32")
