"""LLM agent: CV text -> structured Beraterprofil JSON."""

from __future__ import annotations

import json
import re
from pathlib import Path

import httpx

from app.config import PROMPT_PATH, settings
from app.schemas.profile import BeraterprofilData
from app.services.content_fit import LIMITS, fit_profile


def _load_system_prompt() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8")


def _extract_json(text: str) -> dict:
    text = text.strip()
    # Strip markdown fences if present
    fence = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if fence:
        text = fence.group(1)
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("LLM response did not contain JSON object")
    return json.loads(text[start : end + 1])


async def _call_deepseek(system: str, user: str) -> str:
    if not settings.deepseek_api_key:
        raise RuntimeError("DEEPSEEK_API_KEY not configured in .env")
    url = f"{settings.deepseek_base_url.rstrip('/')}/chat/completions"
    payload = {
        "model": settings.deepseek_model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.2,
        "response_format": {"type": "json_object"},
    }
    headers = {
        "Authorization": f"Bearer {settings.deepseek_api_key}",
        "Content-Type": "application/json",
    }
    async with httpx.AsyncClient(timeout=120.0) as client:
        resp = await client.post(url, json=payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()
    return data["choices"][0]["message"]["content"]


async def _call_mistral(system: str, user: str) -> str:
    if not settings.mistral_api_key:
        raise RuntimeError("MISTRAL_API_KEY not configured in .env")
    url = f"{settings.mistral_base_url.rstrip('/')}/chat/completions"
    payload = {
        "model": settings.mistral_model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.2,
        "response_format": {"type": "json_object"},
    }
    headers = {
        "Authorization": f"Bearer {settings.mistral_api_key}",
        "Content-Type": "application/json",
    }
    async with httpx.AsyncClient(timeout=120.0) as client:
        resp = await client.post(url, json=payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()
    return data["choices"][0]["message"]["content"]


async def extract_profile(cv_text: str, provider: str | None = None) -> BeraterprofilData:
    provider = (provider or settings.llm_provider).lower()
    system = _load_system_prompt()
    user = f"Lebenslauf (Rohtext):\n\n{cv_text[:50000]}"

    if provider == "deepseek":
        raw = await _call_deepseek(system, user)
    elif provider == "mistral":
        raw = await _call_mistral(system, user)
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}. Use deepseek or mistral.")

    parsed = _extract_json(raw)
    parsed = _normalize_payload(parsed)
    profile = BeraterprofilData.model_validate(parsed)
    return fit_profile(profile)


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

    provider = (provider or settings.llm_provider).lower()
    system = _load_revision_prompt()
    payload = {
        "current_profile": json.loads(profile.model_dump_json()),
        "manager_comment": comment,
        "cv_text": (cv_text or "")[:50000],
    }
    user = json.dumps(payload, ensure_ascii=False, indent=2)

    if provider == "deepseek":
        raw = await _call_deepseek(system, user)
    elif provider == "mistral":
        raw = await _call_mistral(system, user)
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")

    parsed = _extract_json(raw)
    parsed = _normalize_payload(parsed)
    revised = BeraterprofilData.model_validate(parsed)
    return fit_profile(revised)


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
    return data


def _call_deepseek_sync(system: str, user: str) -> str:
    if not settings.deepseek_api_key:
        raise RuntimeError("DEEPSEEK_API_KEY not configured in .env")
    url = f"{settings.deepseek_base_url.rstrip('/')}/chat/completions"
    payload = {
        "model": settings.deepseek_model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.2,
        "response_format": {"type": "json_object"},
    }
    headers = {
        "Authorization": f"Bearer {settings.deepseek_api_key}",
        "Content-Type": "application/json",
    }
    with httpx.Client(timeout=120.0) as client:
        resp = client.post(url, json=payload, headers=headers)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]


def _call_mistral_sync(system: str, user: str) -> str:
    if not settings.mistral_api_key:
        raise RuntimeError("MISTRAL_API_KEY not configured in .env")
    url = f"{settings.mistral_base_url.rstrip('/')}/chat/completions"
    payload = {
        "model": settings.mistral_model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.2,
        "response_format": {"type": "json_object"},
    }
    headers = {
        "Authorization": f"Bearer {settings.mistral_api_key}",
        "Content-Type": "application/json",
    }
    with httpx.Client(timeout=120.0) as client:
        resp = client.post(url, json=payload, headers=headers)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]


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

    provider = (provider or settings.llm_provider).lower()
    system = _load_revision_prompt()
    payload = {
        "current_profile": json.loads(profile.model_dump_json()),
        "manager_comment": comment,
        "cv_text": (cv_text or "")[:50000],
    }
    user = json.dumps(payload, ensure_ascii=False, indent=2)

    if provider == "deepseek":
        raw = _call_deepseek_sync(system, user)
    elif provider == "mistral":
        raw = _call_mistral_sync(system, user)
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")

    parsed = _extract_json(raw)
    parsed = _normalize_payload(parsed)
    revised = BeraterprofilData.model_validate(parsed)
    return fit_profile(revised)
