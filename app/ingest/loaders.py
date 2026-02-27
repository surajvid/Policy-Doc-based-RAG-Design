"""
loaders.py

Non-technical explanation:
- Our AI cannot directly "read" a PDF file like a human.
- So we first convert the file into plain text.

This file contains simple "loaders":
- A loader reads a file and returns its text.
"""

from pathlib import Path
from pypdf import PdfReader


def load_text_from_file(file_path: Path) -> str:
    """
    Convert a supported file into plain text.

    Supported files:
    - PDF (.pdf)
    - Text (.txt)
    - Markdown (.md)

    Returns:
    - A single plain text string (the full content of the file)

    Why we do this:
    - Our search + AI system works on text, not raw PDF binaries.
    """

    suffix = file_path.suffix.lower()

    # Case 1: PDF file
    if suffix == ".pdf":
        reader = PdfReader(str(file_path))
        pages_text: list[str] = []

        # PDFs contain many pages. We read each page.
        for page in reader.pages:
            pages_text.append(page.extract_text() or "")

        # Join all pages into one big text block
        return "\n".join(pages_text).strip()

    # Case 2: Normal text or markdown
    if suffix in [".txt", ".md"]:
        return file_path.read_text(encoding="utf-8", errors="ignore").strip()

    # Anything else: reject
    raise ValueError(f"Unsupported file type: {suffix}")
