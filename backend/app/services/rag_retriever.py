from typing import List
from app.services.vector_index import search_index


def get_relevant_context(query: str, top_k: int = 5) -> List[str]:
    results = search_index(query, top_k=top_k)
    chunks: List[str] = []
    for item in results:
        text = item.get("job_text", "")
        score = item.get("score", 0.0)
        chunks.append(f"[score={score:.3f}] {text}")
    return chunks


def build_context_string(query: str, top_k: int = 5) -> str:
    chunks = get_relevant_context(query, top_k=top_k)
    if not chunks:
        return "No highly relevant job or skill context was found."
    return "\n\n".join(chunks)
