import faiss
import numpy as np
import pickle
import os

from app.services.embeddings_engine import encode_text

# Get backend directory (2 levels up from services/)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))

# Correct embeddings directory: backend/data/embeddings
EMBED_DIR = os.path.join(BASE_DIR, "data", "embeddings")

# Correct file paths
INDEX_PATH = os.path.join(EMBED_DIR, "faiss.index")
META_PATH = os.path.join(EMBED_DIR, "metadata.pkl")


def build_index(texts: list):
    print("Encoding job_text column into vectors...")
    vectors = np.array([encode_text(t) for t in texts], dtype="float32")

    print("Normalizing vectors...")
    faiss.normalize_L2(vectors)

    dim = vectors.shape[1]

    print("Creating FAISS index...")
    index = faiss.IndexFlatIP(dim)
    index.add(vectors)

    os.makedirs(EMBED_DIR, exist_ok=True)

    faiss.write_index(index, INDEX_PATH)

    with open(META_PATH, "wb") as f:
        pickle.dump(texts, f)

    print("FAISS index built successfully!")


def load_index():
    index = faiss.read_index(INDEX_PATH)

    with open(META_PATH, "rb") as f:
        meta = pickle.load(f)

    return index, meta


def search_index(query_text: str, top_k: int = 10):
    print("Searching FAISS index...")

    index, meta = load_index()

    q_vec = np.array([encode_text(query_text)], dtype="float32")
    faiss.normalize_L2(q_vec)

    scores, ids = index.search(q_vec, top_k)

    results = []
    for idx, score in zip(ids[0], scores[0]):
        results.append({
            "job_id": int(idx),
            "job_text": meta[idx],
            "score": float(score)
        })

    return results
