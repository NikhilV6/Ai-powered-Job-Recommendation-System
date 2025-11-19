from sentence_transformers import SentenceTransformer
import numpy as np
import torch

MODEL_NAME = "all-MiniLM-L6-v2"

# Lazy-load model so it's not loaded on import
_model = None

def get_model():
    global _model
    if _model is None:
        print("Loading SentenceTransformer model...")
        # Use GPU if available
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {device}")
        _model = SentenceTransformer(MODEL_NAME, device=device)
    return _model

def encode_text(text: str):
    """Single text encoding - for search queries"""
    model = get_model()
    vec = model.encode(text, show_progress_bar=False, convert_to_numpy=True)
    return np.array(vec, dtype="float32")

def encode_batch(texts: list, batch_size: int = 128):
    """
    Batch encoding for multiple texts - MUCH FASTER!
    
    Args:
        texts: List of text strings to encode
        batch_size: Number of texts to encode at once (default 128)
                   Increase if you have more GPU memory
    
    Returns:
        numpy array of embeddings
    """
    model = get_model()
    
    print(f"Encoding {len(texts)} texts in batches of {batch_size}...")
    
    embeddings = model.encode(
        texts,
        batch_size=batch_size,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=False  # We'll normalize in FAISS
    )
    
    return np.array(embeddings, dtype="float32")