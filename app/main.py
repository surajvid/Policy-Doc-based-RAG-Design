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

# Setup basic logging
setup_logging()
logger = logging.getLogger("newpage-docs-rag")

# Create the FastAPI application
app = FastAPI(title="Newpage Option 1 - Docs RAG (MVP)")


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
