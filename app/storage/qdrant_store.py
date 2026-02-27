"""
qdrant_store.py

Non-technical explanation:
- Qdrant is our "smart database" for storing meaning-based search entries.
- Each document chunk becomes an entry in Qdrant.

This file contains:
1) How to connect to Qdrant
2) How to create a collection (like a table)
3) How to insert (upsert) chunk records
"""

from qdrant_client import QdrantClient
from qdrant_client.http import models as qm

from app.core.config import settings


def get_qdrant_client() -> QdrantClient:
    """
    Create and return a Qdrant client.

    Non-technical explanation:
    - This is like opening a connection to a database.
    - The URL comes from .env (QDRANT_URL).
    """
    return QdrantClient(url=settings.qdrant_url)


def ensure_collection_exists(client: QdrantClient, vector_size: int) -> None:
    """
    Ensure the Qdrant collection exists.

    Non-technical explanation:
    - A "collection" is like a table in a normal database.
    - We create it once and reuse it.
    - vector_size must match the embedding dimension.
    """

    existing = [c.name for c in client.get_collections().collections]
    if settings.qdrant_collection in existing:
        return

    client.create_collection(
        collection_name=settings.qdrant_collection,
        vectors_config=qm.VectorParams(
            size=vector_size,              # embedding length (example: 1536)
            distance=qm.Distance.COSINE,   # cosine similarity is standard for embeddings
        ),
    )
