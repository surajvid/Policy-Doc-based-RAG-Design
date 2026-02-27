"""
schemas.py

Non-technical explanation:
- These are "data shapes" for API input/output.
- They help keep responses consistent and readable.
"""

from pydantic import BaseModel
from typing import Optional


class Source(BaseModel):
    """
    One citation source.
    """
    file: str
    chunk_index: int
    score: float


class ChatRequest(BaseModel):
    """
    What the user sends.
    """
    question: str
    conversation_id: Optional[str] = None  # optional; not used in MVP


class ChatResponse(BaseModel):
    """
    What the API returns.
    """
    answer: str
    sources: list[Source]
    trace_id: str
