"""
retriever.py

Non-technical explanation:
- This file is responsible for SEARCH.
- When the user asks a question, we find the most relevant document chunks.

How it works:
1) Convert the question into an embedding vector (numbers)
2) Ask Qdrant for the most similar vectors (top results)
3) Return those chunks as "evidence"
"""

from app.core.config import settings
from app.rag.embeddings import embed_texts
from app.storage.qdrant_store import get_qdrant_client


def retrieve_relevant_chunks(question: str, top_k: int | None = None) -> list[dict]:
    """
    Retrieve the most relevant chunks from Qdrant for a given question.

    Uses Qdrant's newer API: query_points()
    """

    k = top_k or settings.top_k

    # 1) Convert question to embedding vector
    query_vector = embed_texts([question])[0]

    # 2) Query Qdrant for nearest vectors
    client = get_qdrant_client()
    response = client.query_points(
        collection_name=settings.qdrant_collection,
        query=query_vector,
        limit=k,
        with_payload=True,
    )

    results = []
    for p in response.points:
        payload = p.payload or {}
        results.append(
            {
                "file": payload.get("file", ""),
                "chunk_index": payload.get("chunk_index", -1),
                "text": payload.get("text", ""),
                "score": p.score,
            }
        )

    return results