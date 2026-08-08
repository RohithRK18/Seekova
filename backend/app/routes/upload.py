import os
import uuid

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.file_parser import extract_text
from app.search_engine import search_engine


router = APIRouter(
    prefix="/api/upload",
    tags=["Upload"]
)

UPLOAD_DIRECTORY = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "uploads")

os.makedirs(
    UPLOAD_DIRECTORY,
    exist_ok=True
)

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".txt",
    ".docx",
    ".md"
}


@router.post("")
async def upload_file(
    file: UploadFile = File(...)
):
    extension = os.path.splitext(
        file.filename
    )[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file format"
        )

    file_id = str(uuid.uuid4())
    filename = f"{file_id}{extension}"
    file_path = os.path.join(
        UPLOAD_DIRECTORY,
        filename
    )

    content = await file.read()

    with open(file_path, "wb") as output:
        output.write(content)

    extracted_text = extract_text(file_path)

    if not extracted_text.strip():
        raise HTTPException(
            status_code=400,
            detail="Could not extract text from file"
        )

    search_engine.add_document(
        document_id=file_id,
        title=file.filename,
        content=extracted_text,
        file_type=extension
    )

    return {
        "success": True,
        "message": "Document indexed successfully",
        "document": {
            "id": file_id,
            "name": file.filename,
            "type": extension,
            "characters": len(extracted_text)
        }
    }
