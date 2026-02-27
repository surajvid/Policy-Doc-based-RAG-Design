"""
main.py

This is the entry point of the application.

Non-technical explanation:
- This starts a small web server.
- A web server exposes "endpoints" (URLs) that someone can call.
- Example endpoint: GET /health
  This is used to confirm the app is running.
"""

from pathlib import Path
import logging
from fastapi import FastAPI
from fastapi import UploadFile, File, HTTPException


from app.core.config import settings
from app.core.logging import setup_logging
from app.ingest.loaders import load_text_from_file
from app.ingest.chunking import chunk_text
from app.rag.indexer import index_document_chunks

import uuid
from app.rag.retriever import retrieve_relevant_chunks
from app.rag.generator import generate_answer
from app.rag.schemas import ChatRequest, ChatResponse, Source

from app.core.middleware import request_logging_middleware

from fastapi import Request


# Setup basic logging
setup_logging()
logger = logging.getLogger("newpage-docs-rag")

# Create the FastAPI application
app = FastAPI(title="Newpage Option 1 - Docs RAG (MVP)")
app.middleware("http")(request_logging_middleware)

@app.on_event("startup")
def on_startup():
    """
    This runs automatically when the API starts.

    Non-technical explanation:
    - We ensure the uploads folder exists.
    - This avoids errors later when someone uploads a file.
    """
    Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)
    logger.info("Uploads folder ready at: %s", settings.upload_dir)


@app.get("/health")
def health():
    """
    Health check endpoint.

    Non-technical explanation:
    - This is like asking: "Are you alive?"
    - If it returns status 'ok', the service is running.
    """
    return {"status": "ok"}

@app.post("/documents/upload")

async def upload_document(file: UploadFile = File(...)):
    """
    Upload a document to the server.

    Non-technical explanation:
    - This is like a "dropbox" where you can upload a file.
    - The server receives the file and saves it in our uploads folder.

    What this endpoint does:
    1) Checks if the file type is allowed (PDF, TXT, MD)
    2) Saves the file to our upload folder
    3) Returns a message confirming the save
    """

    # 1) Check file extension (example: ".pdf", ".txt")
    filename = file.filename or ""
    extension = Path(filename).suffix.lower()

    allowed_extensions = [".pdf", ".txt", ".md"]
    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {extension}. Allowed: {allowed_extensions}",
        )

    # 2) Decide where to save it on disk
    save_path = Path(settings.upload_dir) / filename

    # 3) Read the uploaded file content (bytes)
    file_bytes = await file.read()

    # 4) Write the bytes to disk
    save_path.write_bytes(file_bytes)

    # 5) Return a success response
    return {
        "message": "File uploaded successfully",
        "saved_as": str(save_path),
        "size_bytes": len(file_bytes),
    }
@app.get("/documents/preview-chunks")
def preview_chunks(filename: str):
    """
    Preview how a document gets split into chunks.

    Non-technical explanation:
    - This endpoint does NOT use AI.
    - It just shows:
        1) the extracted text length
        2) how many chunks were created
        3) first 2 chunks as a sample
    """

    file_path = Path(settings.upload_dir) / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found in uploads folder")

    # 1) Extract text
    full_text = load_text_from_file(file_path)

    # 2) Split into chunks
    chunks = chunk_text(full_text, settings.chunk_size, settings.chunk_overlap)

    # 3) Return small preview (first 2 chunks only)
    preview = [{"chunk_index": c.index, "text_preview": c.text[:300]} for c in chunks[:2]]

    return {
        "filename": filename,
        "text_length_chars": len(full_text),
        "chunks_created": len(chunks),
        "first_chunks_preview": preview,
    }

@app.post("/index/rebuild")
def rebuild_index():
    """
    Index all uploaded documents into Qdrant.

    Fix included:
    - We only index supported file types (.pdf, .txt, .md)
    - We skip files like .keep or files without extensions
    """

    upload_dir = Path(settings.upload_dir)
    if not upload_dir.exists():
        raise HTTPException(status_code=400, detail="Uploads folder not found.")

    allowed_extensions = {".pdf", ".txt", ".md"}

    # Only pick files with allowed extensions
    files = [
        f for f in upload_dir.iterdir()
        if f.is_file() and f.suffix.lower() in allowed_extensions
    ]

    if not files:
        raise HTTPException(
            status_code=400,
            detail="No supported files found to index. Upload a PDF/TXT/MD first.",
        )

    results = []
    for f in files:
        # 1) Extract text
        text = load_text_from_file(f)
        if not text.strip():
            # Skip empty files
            continue

        # 2) Chunk it
        chunks = chunk_text(text, settings.chunk_size, settings.chunk_overlap)

        # 3) Store in Qdrant (chunk_index, chunk_text)
        out = index_document_chunks(f.name, [(c.index, c.text) for c in chunks])
        results.append(out)

    return {"indexed": results, "total_files_considered": len(files)}

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest, request: Request):
    trace_id = getattr(request.state, "trace_id", "unknown")
    try:
        evidence = retrieve_relevant_chunks(req.question)
        answer_text = generate_answer(req.question, evidence)
        sources = [Source(file=c["file"], chunk_index=c["chunk_index"], score=c["score"]) for c in evidence]

        if "don’t have enough information" in answer_text.lower() or "don't have enough information" in answer_text.lower():
            sources = []

        return ChatResponse(answer=answer_text, sources=sources, trace_id=trace_id)

    except RuntimeError as e:
        # user-friendly errors for config/network/auth issues
        raise HTTPException(status_code=400, detail=str(e))