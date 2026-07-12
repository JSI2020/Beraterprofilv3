"""Beraterprofil generator pipeline."""

from __future__ import annotations

import uuid
from datetime import datetime
from pathlib import Path

from app.config import OUTPUT_DIR, TEMPLATE_PATH, UPLOAD_DIR
from app.schemas.profile import BeraterprofilData
from app.services.cv_parser import extract_cv_text, load_photo
from app.services.llm_agent import extract_profile
from app.services.pptx_builder import build_pptx


async def generate_beraterprofil(
    cv_path: Path,
    photo_path: Path | None = None,
    provider: str | None = None,
    output_name: str | None = None,
) -> tuple[Path, BeraterprofilData]:
    if not TEMPLATE_PATH.exists():
        raise FileNotFoundError(f"Template missing: {TEMPLATE_PATH}")

    cv_text = extract_cv_text(cv_path)
    if len(cv_text.strip()) < 50:
        raise ValueError(
            "Could not extract enough text from CV. Try PDF/DOCX with selectable text "
            "or upload a photo separately."
        )

    profile = await extract_profile(cv_text, provider=provider)
    photo_bytes = load_photo(photo_path)

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = output_name or f"Beraterprofil_{stamp}_{uuid.uuid4().hex[:8]}"
    if not safe_name.lower().endswith(".pptx"):
        safe_name += ".pptx"

    out_path = OUTPUT_DIR / safe_name
    build_pptx(profile, TEMPLATE_PATH, out_path, photo_bytes=photo_bytes)
    return out_path, profile
