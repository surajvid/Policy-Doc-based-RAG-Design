"""
chunking.py


- A long document is too large to search and send to AI directly.
- So we split it into smaller pieces called "chunks".

Example:
- If a document has 20,000 characters,
  we may split it into chunks of 1,200 characters each.

We also add a small "overlap":
- This means chunk #2 repeats a bit of chunk #1.
- This prevents important sentences from being cut in half.
"""

from dataclasses import dataclass


@dataclass
class Chunk:
    """
    A small piece of a document.

    index:
      - Chunk number (0, 1, 2, 3...)
    text:
      - The actual chunk text
    """

    index: int
    text: str


def chunk_text(text: str, chunk_size: int, overlap: int) -> list[Chunk]:
    """
    Split a large text into smaller overlapping chunks.

    Parameters:
    - text: the full document text
    - chunk_size: how big each chunk is (example: 1200 characters)
    - overlap: how much chunk repeats from previous chunk (example: 200 characters)

    Returns:
    - List of Chunk objects
    """

    if chunk_size <= 0:
        raise ValueError("chunk_size must be > 0")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be >= 0 and < chunk_size")

    # Clean extra whitespace so chunks are nicer
    cleaned_text = " ".join(text.split())

    chunks: list[Chunk] = []

    start = 0
    chunk_index = 0

    while start < len(cleaned_text):
        end = min(len(cleaned_text), start + chunk_size)
        piece = cleaned_text[start:end].strip()

        if piece:
            chunks.append(Chunk(index=chunk_index, text=piece))
            chunk_index += 1

        # If we reached end, stop
        if end == len(cleaned_text):
            break

        # Move forward, but keep an overlap
        start = end - overlap

    return chunks
