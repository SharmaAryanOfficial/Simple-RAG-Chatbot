from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import shutil

from src.services.rag_service import rag_service

router = APIRouter(prefix="/rag", tags=["RAG"])

UPLOAD_DIR = Path("data/uploads")


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a document and build RAG index.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")

    file_path = UPLOAD_DIR / file.filename

    # Save uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Build (placeholder) index
    rag_service.build_index(str(file_path))

    return {
        "status": "success",
        "filename": file.filename,
        "index_ready": True
    }
