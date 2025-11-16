# backend/app/api/v1/resume.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import shutil
import tempfile
import os
from typing import Dict

from app.services.resume_parser import parse_resume

router = APIRouter()


@router.post("/resume/upload")
async def upload_resume(file: UploadFile = File(...)) -> Dict:
    """
    Upload a resume (.pdf, .docx, .doc, .txt) and return the parsed profile JSON.
    Uses the system temporary directory (cross-platform) and removes the temp file after parsing.
    """
    # basic filename validation to avoid path traversal
    filename = Path(file.filename).name
    if not filename:
        raise HTTPException(status_code=400, detail="Filename missing")

    ext = Path(filename).suffix.lower()
    if ext not in [".pdf", ".docx", ".doc", ".txt"]:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    # save to OS temp dir (works on Windows, Linux, macOS)
    tmp_dir = Path(tempfile.gettempdir())
    save_path = tmp_dir / filename

    try:
        with save_path.open("wb") as buffer:
            # copyfileobj works with UploadFile.file (a SpooledTemporaryFile-like object)
            shutil.copyfileobj(file.file, buffer)

        # parse resume (raise if parser fails)
        profile = parse_resume(str(save_path))

        # optionally, you could store the profile into DB here

        return {"profile": profile}

    except HTTPException:
        # re-raise FastAPI HTTPExceptions unchanged
        raise
    except Exception as e:
        # generic error -> 500
        raise HTTPException(status_code=500, detail=f"Failed to parse resume: {e}")
    finally:
        # cleanup temp file if it exists
        try:
            if save_path.exists():
                os.remove(save_path)
        except Exception:
            # ignore cleanup errors
            pass
