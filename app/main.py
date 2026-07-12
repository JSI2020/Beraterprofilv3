"""FastAPI application for Beraterprofil generator."""

from __future__ import annotations

import json
import shutil
import uuid
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.config import OUTPUT_DIR, ROOT_DIR, TEMPLATE_PATH, UPLOAD_DIR, settings
from app.pipeline import generate_beraterprofil

app = FastAPI(
    title="ORBIT Beraterprofil Generator",
    description="CV hochladen → One-Pager Beraterprofil (PPTX) im ORBIT-Template",
    version="1.0.0",
)

STATIC_DIR = ROOT_DIR / "static"
STATIC_DIR.mkdir(exist_ok=True)


@app.get("/", response_class=HTMLResponse)
async def index():
    html_path = STATIC_DIR / "index.html"
    return html_path.read_text(encoding="utf-8")


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "template": TEMPLATE_PATH.exists(),
        "llm_provider": settings.llm_provider,
    }


@app.post("/api/generate")
async def api_generate(
    cv: UploadFile = File(..., description="CV as PDF or DOCX"),
    photo: UploadFile | None = File(None, description="Optional profile photo"),
    provider: str = Form(default=""),
):
    cv_suffix = Path(cv.filename or "").suffix.lower()
    if cv_suffix not in {".pdf", ".docx"}:
        raise HTTPException(400, "CV must be PDF or DOCX")

    job_id = uuid.uuid4().hex[:12]
    cv_path = UPLOAD_DIR / f"{job_id}_cv{cv_suffix}"
    photo_path: Path | None = None

    try:
        with cv_path.open("wb") as f:
            shutil.copyfileobj(cv.file, f)

        if photo and photo.filename:
            photo_suffix = Path(photo.filename).suffix.lower()
            if photo_suffix not in {".jpg", ".jpeg", ".png", ".webp"}:
                raise HTTPException(400, "Photo must be JPG, PNG, or WEBP")
            photo_path = UPLOAD_DIR / f"{job_id}_photo{photo_suffix}"
            with photo_path.open("wb") as f:
                shutil.copyfileobj(photo.file, f)

        llm = provider.strip() or None
        out_path, profile = await generate_beraterprofil(
            cv_path=cv_path,
            photo_path=photo_path,
            provider=llm,
            output_name=f"Beraterprofil_{job_id}.pptx",
        )

        return {
            "job_id": job_id,
            "download_url": f"/api/download/{out_path.name}",
            "profile": json.loads(profile.model_dump_json()),
        }
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(503, str(exc)) from exc
    except Exception as exc:
        raise HTTPException(500, f"Generation failed: {exc}") from exc


@app.get("/api/download/{filename}")
async def download(filename: str):
    safe = Path(filename).name
    path = OUTPUT_DIR / safe
    if not path.exists():
        raise HTTPException(404, "File not found")
    return FileResponse(
        path,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        filename=safe,
    )
