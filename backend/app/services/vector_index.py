import faiss
import numpy as np
import pickle
import os

from app.services.embeddings_engine import encode_text, encode_batch

# Base directory: backend/
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))

# embeddings directory location -> backend/data/embeddings
EMBED_DIR = os.path.join(BASE_DIR, "data", "embeddings")

# File paths
INDEX_PATH = os.path.join(EMBED_DIR, "faiss.index")
META_PATH = os.path.join(EMBED_DIR, "metadata.pkl")


# -----------------------------------------------
# 🚀 Build FAISS Index with BATCH PROCESSING
# -----------------------------------------------
def build_index_fast(records: list, batch_size: int = 128):
    """
    Fast index building using batch encoding.
    
    Args:
        records: List of job records with metadata
        batch_size: Number of texts to encode at once
                   - 128 for CPU
                   - 256-512 for GPU with good memory
    """

    print(f"Building FAISS index for {len(records)} job embeddings...")

    # 1) Extract all job texts
    job_texts = [rec["job_text"] for rec in records]

    # 2) Batch encode ALL texts at once - THIS IS THE KEY SPEEDUP!
    print(f"Encoding {len(job_texts)} embeddings in batches...")
    vectors = encode_batch(job_texts, batch_size=batch_size)

    # 3) Normalize for cosine similarity
    print("Normalizing vectors...")
    faiss.normalize_L2(vectors)

    # 4) Initialize index (inner product = cosine similarity)
    dim = vectors.shape[1]
    print(f"Creating FAISS index with dim={dim}...")
    index = faiss.IndexFlatIP(dim)
    index.add(vectors)

    # 5) Ensure directory exists
    os.makedirs(EMBED_DIR, exist_ok=True)

    # 6) Save index
    print("Saving FAISS index...")
    faiss.write_index(index, INDEX_PATH)
    print("FAISS index saved at:", INDEX_PATH)

    # 7) Save metadata (all job information)
    print("Saving metadata...")
    with open(META_PATH, "wb") as f:
        pickle.dump(records, f)

    print("Metadata saved at:", META_PATH)
    print("🎉 Index build complete!")


# -----------------------------------------------
# Legacy function for backward compatibility
# -----------------------------------------------
def build_index(records: list):
    """Legacy function - redirects to fast version"""
    build_index_fast(records)


def load_index():
    if not os.path.exists(INDEX_PATH):
        raise RuntimeError(f"FAISS index not found at: {INDEX_PATH}")

    index = faiss.read_index(INDEX_PATH)

    with open(META_PATH, "rb") as f:
        meta = pickle.load(f)

    return index, meta


def search_index(query_text: str, top_k: int = 10):
    """
    Search for jobs matching the query text.
    
    Returns:
        List of dicts containing complete job information including:
        - job_id
        - job_title
        - role
        - description
        - required_skills (list of skills needed)
        - company
        - location
        - experience_range
        - qualification_level
        - salary_range
        - posting_date
        - similarity_score
    """
    print("Searching FAISS index...")

    index, meta = load_index()

    # Encode query (single text, not batch)
    q_vec = np.array([encode_text(query_text)], dtype="float32")
    faiss.normalize_L2(q_vec)

    # Search
    scores, ids = index.search(q_vec, top_k)

    results = []
    for idx, score in zip(ids[0], scores[0]):
        job_meta = meta[idx]

        results.append({
            "job_id": int(idx),
            "job_title": job_meta.get("job_title", ""),
            "role": job_meta.get("role", ""),
            "description": job_meta.get("description", ""),
            "required_skills": job_meta.get("skills", []),
            "company": job_meta.get("company", ""),
            "location": job_meta.get("location", ""),
            "experience_range": {
                "min": job_meta.get("experience_min", 0),
                "max": job_meta.get("experience_max", 0)
            },
            "qualification_level": job_meta.get("qualification_level", ""),
            "salary_range": {
                "min": job_meta.get("salary_min", 0),
                "max": job_meta.get("salary_max", 0)
            },
            "posting_date": job_meta.get("posting_date", ""),
            "similarity_score": float(score)
        })

    return results