"""Generation pipeline bridge for Streamlit UI."""

from __future__ import annotations

import asyncio
import json
import os
import tempfile
import uuid
from datetime import datetime
from pathlib import Path

from app.config import OUTPUT_DIR, TEMPLATE_PATH, settings
from app.pipeline import generate_beraterprofil
from app.schemas.profile import BeraterprofilData
from app.services.llm_agent import revise_profile_with_feedback_sync
from app.services.pptx_parser import parse_beraterprofil_pptx


def llm_status() -> dict:
    provider = settings.llm_provider
    if provider == "deepseek" and settings.deepseek_api_key:
        return {"active": True, "provider": "deepseek", "model": settings.deepseek_model}
    if provider == "mistral" and settings.mistral_api_key:
        return {"active": True, "provider": "mistral", "model": settings.mistral_model}
    if settings.deepseek_api_key:
        return {"active": True, "provider": "deepseek", "model": settings.deepseek_model}
    if settings.mistral_api_key:
        return {"active": True, "provider": "mistral", "model": settings.mistral_model}
    return {"active": False, "provider": None, "model": None}


def save_upload_temporarily(uploaded_file) -> Path:
    suffix = Path(uploaded_file.name).suffix.lower()
    handle = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    handle.write(uploaded_file.getbuffer())
    handle.close()
    return Path(handle.name)


def cleanup_temp(path: Path | None) -> None:
    if path and path.exists() and os.getenv("STORE_UPLOADS", "false").lower() != "true":
        path.unlink(missing_ok=True)


async def _generate(cv_path: Path, photo_path: Path | None, provider: str) -> tuple[Path, BeraterprofilData]:
    return await generate_beraterprofil(
        cv_path=cv_path,
        photo_path=photo_path,
        provider=provider,
        output_name=f"Beraterprofil_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}.pptx",
    )


def generate_sync(
    cv_path: Path,
    *,
    photo_path: Path | None = None,
    provider: str = "deepseek",
    position_override: str | None = None,
) -> tuple[Path, BeraterprofilData]:
    out_path, profile = asyncio.run(_generate(cv_path, photo_path, provider))
    if position_override and position_override != "Aus CV ableiten":
        profile.position = position_override
    return out_path, profile


def profile_to_json(profile: BeraterprofilData) -> str:
    return json.dumps(json.loads(profile.model_dump_json()), ensure_ascii=False, indent=2)


def profile_from_json(text: str) -> BeraterprofilData:
    return BeraterprofilData.model_validate_json(text)


def validate_for_export(profile: BeraterprofilData) -> tuple[bool, list[str]]:
    issues: list[str] = []
    if not profile.schwerpunkte.strip():
        issues.append("Schwerpunkte fehlen")
    if not profile.summary.strip():
        issues.append("Summary fehlt")
    if len(profile.kompetenzen) < 3:
        issues.append("Mindestens 3 Kompetenzen erforderlich")
    if not profile.relevante_erfahrungen:
        issues.append("Relevante Erfahrungen fehlen")
    if not profile.ausbildung_karriere:
        issues.append("Ausbildung/Karriere fehlt")
    if not profile.abschluss_zertifikate:
        issues.append("Abschluss/Zertifikate fehlen")
    if not TEMPLATE_PATH.exists():
        issues.append(f"Template fehlt: {TEMPLATE_PATH}")
    return len(issues) == 0, issues


def import_from_pptx(pptx_path: Path) -> BeraterprofilData:
    return parse_beraterprofil_pptx(pptx_path)


def apply_feedback_sync(
    profile: BeraterprofilData,
    manager_comment: str,
    *,
    cv_text: str | None = None,
    provider: str = "deepseek",
) -> BeraterprofilData:
    return revise_profile_with_feedback_sync(
        profile,
        manager_comment,
        cv_text=cv_text,
        provider=provider,
    )


def export_pptx(profile: BeraterprofilData, photo_path: Path | None = None) -> Path:
    from app.services.cv_parser import load_photo
    from app.services.pptx_builder import build_pptx

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = OUTPUT_DIR / f"Beraterprofil_{stamp}_{uuid.uuid4().hex[:8]}.pptx"
    photo_bytes = load_photo(photo_path)
    build_pptx(profile, TEMPLATE_PATH, out_path, photo_bytes=photo_bytes)
    return out_path
