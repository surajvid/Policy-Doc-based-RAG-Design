"""
config.py

This file is the "settings room" of our app.

Non-technical explanation:
- Think of this like the app's control panel.
- It reads values from environment variables (like OPENAI_API_KEY).
- We use these values so we don't hardcode secrets or paths in code.
"""

import os
from pydantic import BaseModel


class Settings(BaseModel):
    """
    A simple container for all settings used by the app.
    """

    # Where uploaded files will be stored on your machine
    upload_dir: str = os.getenv("UPLOAD_DIR", "./data/uploads")

    # We will use these later (kept here early so code stays organized)
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    qdrant_url: str = os.getenv("QDRANT_URL", "http://localhost:6333")
    qdrant_collection: str = os.getenv("QDRANT_COLLECTION", "docs_rag")

    chunk_size: int = int(os.getenv("CHUNK_SIZE", "1200"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "200"))
    top_k: int = int(os.getenv("TOP_K", "6"))

    model_chat: str = os.getenv("MODEL_CHAT", "gpt-4o-mini")
    model_embed: str = os.getenv("MODEL_EMBED", "text-embedding-3-small")


# Create one shared settings object the whole app can use
settings = Settings()
