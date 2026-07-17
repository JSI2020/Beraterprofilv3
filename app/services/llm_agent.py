"""LLM agent: CV text -> structured Beraterprofil JSON."""

from __future__ import annotations

import json
import re
from pathlib import Path

from app.config import PROMPT_PATH
from app.schemas.profile import BeraterprofilData
from app.services.content_fit import (
    LIMITS,
    profile_validation_issues,
    sanitize_profile_dict,
    fit_profile,
)
from app.services.llm_providers import call_llm_with_fallback, call_llm_with_fallback_sync


def _load_system_prompt() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8")


def _extract_json(text: str) -> dict:
    text = text.strip()
    fence = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if fence:
        text = fence.group(1)
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("LLM response did not contain JSON object")
    return json.loads(text[start : end + 1])


def _unwrap_profile_dict(data: dict) -> dict:
    """LLM may return the profile nested or echo the input envelope."""
    if not isinstance(data, dict):
        return data
    if "title_domain" in data and "kompetenzen" in data:
        return data
    for key in ("current_profile", "beraterprofil", "updated_profile", "profile"):
        nested = data.get(key)
        if isinstance(nested, dict) and "title_domain" in nested:
            return nested
    return data


def _normalize_payload(data: dict) -> dict:
    """Pre-trim list counts before schema validation."""
    data = _unwrap_profile_dict(data)
    data["kompetenzen"] = (data.get("kompetenzen") or [])[: LIMITS["kompetenzen_count"]]
    data["relevante_erfahrungen"] = (data.get("relevante_erfahrungen") or [])[
        : LIMITS["relevante_count"]
    ]
    data["ausbildung_karriere"] = (data.get("ausbildung_karriere") or [])[
        : LIMITS["ausbildung_count"]
    ]
    data["abschluss_zertifikate"] = (data.get("abschluss_zertifikate") or [])[
        : LIMITS["abschluss_count"]
    ]
    return sanitize_profile_dict(data)


def _build_repair_prompt(missing: list[str]) -> str:
    return (
        "Die vorherige JSON-Antwort war unvollständig oder ungültig.\n"
        f"Fehlende Pflichtfelder: {', '.join(missing)}\n\n"
        "Extrahiere das vollständige Profil ERNEUT ausschließlich aus dem Lebenslauf-Rohtext.\n"
        "Verwende KEINE Platzhalter, KEINE generischen Sätze und KEINE erfundenen Inhalte.\n"
        "Jedes Feld muss direkt aus dem CV stammen."
    )


async def _parse_and_validate(raw: str) -> BeraterprofilData:
    parsed = _normalize_payload(_extract_json(raw))
    issues = profile_validation_issues(parsed)
    if issues:
        raise ValueError(", ".join(issues))
    profile = BeraterprofilData.model_validate(parsed)
    return fit_profile(profile)


async def extract_profile(cv_text: str, provider: str | None = None) -> BeraterprofilData:
    system = _load_system_prompt()
    user = f"Lebenslauf (Rohtext):\n\n{cv_text[:50000]}"
    raw, used = await call_llm_with_fallback(system, user, provider=provider)
    try:
        return await _parse_and_validate(raw)
    except ValueError as first_error:
        missing = [part.strip() for part in str(first_error).split(",") if part.strip()]
        repair_user = (
            f"{_build_repair_prompt(missing)}\n\n"
            f"Lebenslauf (Rohtext):\n\n{cv_text[:50000]}"
        )
        raw_retry, _ = await call_llm_with_fallback(system, repair_user, provider=used)
        try:
            return await _parse_and_validate(raw_retry)
        except ValueError as second_error:
            raise ValueError(
                f"Profil konnte nicht vollständig aus dem CV extrahiert werden: {second_error}"
            ) from second_error


_REVISION_PROMPT_PATH = PROMPT_PATH.parent / "MANAGER_REVISION_PROMPT.md"


def _load_revision_prompt() -> str:
    return _REVISION_PROMPT_PATH.read_text(encoding="utf-8")


async def revise_profile_with_feedback(
    profile: BeraterprofilData,
    manager_comment: str,
    *,
    cv_text: str | None = None,
    provider: str | None = None,
) -> BeraterprofilData:
    comment = manager_comment.strip()
    if not comment:
        raise ValueError("Feedback-Kommentar ist leer")

    system = _load_revision_prompt()
    payload = {
        "current_profile": json.loads(profile.model_dump_json()),
        "manager_comment": comment,
        "cv_text": (cv_text or "")[:50000],
    }
    user = json.dumps(payload, ensure_ascii=False, indent=2)
    raw, _used = await call_llm_with_fallback(system, user, provider=provider)
    parsed = _normalize_payload(_extract_json(raw))
    issues = profile_validation_issues(parsed)
    if issues:
        raise ValueError(
            "Feedback-Profil unvollständig — fehlende Felder: " + ", ".join(issues)
        )
    revised = BeraterprofilData.model_validate(parsed)
    return fit_profile(revised)


def _parse_and_validate_sync(raw: str) -> BeraterprofilData:
    parsed = _normalize_payload(_extract_json(raw))
    issues = profile_validation_issues(parsed)
    if issues:
        raise ValueError(", ".join(issues))
    profile = BeraterprofilData.model_validate(parsed)
    return fit_profile(profile)


def revise_profile_with_feedback_sync(
    profile: BeraterprofilData,
    manager_comment: str,
    *,
    cv_text: str | None = None,
    provider: str | None = None,
) -> BeraterprofilData:
    """Sync revision for Streamlit (avoids asyncio.run issues)."""
    comment = manager_comment.strip()
    if not comment:
        raise ValueError("Feedback-Kommentar ist leer")

    system = _load_revision_prompt()
    payload = {
        "current_profile": json.loads(profile.model_dump_json()),
        "manager_comment": comment,
        "cv_text": (cv_text or "")[:50000],
    }
    user = json.dumps(payload, ensure_ascii=False, indent=2)
    raw, _used = call_llm_with_fallback_sync(system, user, provider=provider)
    return _parse_and_validate_sync(raw)
