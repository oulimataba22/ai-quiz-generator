from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

router = APIRouter(prefix="/documents", tags=["documents"])

UPLOAD_DIR = Path(__file__).resolve().parents[3] / "data" / "uploads"
MAX_SIZE = 20 * 1024 * 1024  # 20 Mo


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Seuls les fichiers PDF sont acceptés.")

    content = await file.read()

    if len(content) > MAX_SIZE:
        raise HTTPException(status_code=413, detail="Fichier trop volumineux (20 Mo max).")

    if not content.startswith(b"%PDF"):
        raise HTTPException(status_code=400, detail="Ce fichier n'est pas un vrai PDF.")

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    safe_name = Path(file.filename).name
    (UPLOAD_DIR / safe_name).write_bytes(content)

    return {"filename": safe_name, "status": "uploaded"}