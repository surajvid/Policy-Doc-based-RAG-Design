"""
indexer.py

Non-technical explanation:
- "Indexing" means preparing documents so we can search them later.
- Steps:
  1) Take document chunks
  2) Convert each chunk into an embedding vector
  3) Store vector + metadata in Qdrant
"""

import uuid
from qdrant_client.http import models as qm

from app.rag.embeddings import embed_texts
from app.storage.qdrant_store import get_qdrant_client, ensure_collection_exists
from app.core.config import settings


def index_document_chunks(file_name: str, chunks: list[tuple[int, str]]) -> dict:
    """
    Store all chunks from a single file into Qdrant.

    chunks: list of (chunk_index, chunk_text)
    """

    if not chunks:
        return {"file": file_name, "chunks_indexed": 0}

    # 1) Create embeddings for chunk texts
    vectors = embed_texts([text for _, text in chunks])

    # 2) Connect to Qdrant
    client = get_qdrant_client()

    # 3) Ensure collection exists with correct vector size
    ensure_collection_exists(client, vector_size=len(vectors[0]))

    # 4) Prepare Qdrant points (each chunk becomes one point)
    points: list[qm.PointStruct] = []
    for (chunk_index, chunk_text), vector in zip(chunks, vectors):
        points.append(
            qm.PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={
                    # Metadata: helps with citations and debugging
                    "file": file_name,
                    "chunk_index": chunk_index,
                    "text": chunk_text,
                },
            )
        )

    # 5) Upsert = insert if new, update if exists
    client.upsert(collection_name=settings.qdrant_collection, points=points)

    return {"file": file_name, "chunks_indexed": len(points)}
