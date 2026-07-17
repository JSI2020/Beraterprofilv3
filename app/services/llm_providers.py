"""LLM provider resolution and chat calls with fallback."""

from __future__ import annotations

import logging
from collections.abc import Callable

import httpx

from app.config import settings

logger = logging.getLogger(__name__)

PROVIDER_ORDER: tuple[str, ...] = ("openai", "deepseek", "mistral")

PROVIDER_LABELS = {
    "openai": "OpenAI",
    "deepseek": "DeepSeek",
    "mistral": "Mistral",
}


def _has_key(provider: str) -> bool:
    if provider == "openai":
        return bool(settings.openai_api_key.strip())
    if provider == "deepseek":
        return bool(settings.deepseek_api_key.strip())
    if provider == "mistral":
        return bool(settings.mistral_api_key.strip())
    return False


def available_providers() -> list[str]:
    return [provider for provider in PROVIDER_ORDER if _has_key(provider)]


def model_for_provider(provider: str) -> str:
    if provider == "openai":
        return settings.openai_model
    if provider == "deepseek":
        return settings.deepseek_model
    if provider == "mistral":
        return settings.mistral_model
    raise ValueError(f"Unknown provider: {provider}")


def resolve_provider(preferred: str | None = None) -> str:
    """Pick provider: UI choice if configured, else OpenAI -> DeepSeek -> Mistral."""
    preferred_norm = (preferred or "").strip().lower()
    if preferred_norm in PROVIDER_ORDER and _has_key(preferred_norm):
        return preferred_norm
    for provider in PROVIDER_ORDER:
        if _has_key(provider):
            return provider
    raise RuntimeError(
        "No LLM API key configured. Set OPENAI_API_KEY, DEEPSEEK_API_KEY, or MISTRAL_API_KEY in .env"
    )


def providers_to_try(preferred: str | None = None) -> list[str]:
    primary = resolve_provider(preferred)
    return [primary] + [p for p in PROVIDER_ORDER if p != primary and _has_key(p)]


def llm_status(preferred: str | None = None) -> dict:
    available = available_providers()
    if not available:
        return {
            "active": False,
            "provider": None,
            "model": None,
            "fallback_chain": [],
        }
    primary = resolve_provider()
    return {
        "active": True,
        "provider": primary,
        "model": model_for_provider(primary),
        "fallback_chain": [p for p in available if p != primary],
    }


def _chat_payload(model: str, system: str, user: str) -> dict:
    return {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.2,
        "response_format": {"type": "json_object"},
    }


def _auth_headers(api_key: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


async def _call_openai(system: str, user: str) -> str:
    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY not configured in .env")
    url = f"{settings.openai_base_url.rstrip('/')}/chat/completions"
    payload = _chat_payload(settings.openai_model, system, user)
    async with httpx.AsyncClient(timeout=180.0) as client:
        resp = await client.post(url, json=payload, headers=_auth_headers(settings.openai_api_key))
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]


async def _call_deepseek(system: str, user: str) -> str:
    if not settings.deepseek_api_key:
        raise RuntimeError("DEEPSEEK_API_KEY not configured in .env")
    url = f"{settings.deepseek_base_url.rstrip('/')}/chat/completions"
    payload = _chat_payload(settings.deepseek_model, system, user)
    async with httpx.AsyncClient(timeout=120.0) as client:
        resp = await client.post(url, json=payload, headers=_auth_headers(settings.deepseek_api_key))
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]


async def _call_mistral(system: str, user: str) -> str:
    if not settings.mistral_api_key:
        raise RuntimeError("MISTRAL_API_KEY not configured in .env")
    url = f"{settings.mistral_base_url.rstrip('/')}/chat/completions"
    payload = _chat_payload(settings.mistral_model, system, user)
    async with httpx.AsyncClient(timeout=120.0) as client:
        resp = await client.post(url, json=payload, headers=_auth_headers(settings.mistral_api_key))
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]


def _call_openai_sync(system: str, user: str) -> str:
    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY not configured in .env")
    url = f"{settings.openai_base_url.rstrip('/')}/chat/completions"
    payload = _chat_payload(settings.openai_model, system, user)
    with httpx.Client(timeout=180.0) as client:
        resp = client.post(url, json=payload, headers=_auth_headers(settings.openai_api_key))
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]


def _call_deepseek_sync(system: str, user: str) -> str:
    if not settings.deepseek_api_key:
        raise RuntimeError("DEEPSEEK_API_KEY not configured in .env")
    url = f"{settings.deepseek_base_url.rstrip('/')}/chat/completions"
    payload = _chat_payload(settings.deepseek_model, system, user)
    with httpx.Client(timeout=120.0) as client:
        resp = client.post(url, json=payload, headers=_auth_headers(settings.deepseek_api_key))
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]


def _call_mistral_sync(system: str, user: str) -> str:
    if not settings.mistral_api_key:
        raise RuntimeError("MISTRAL_API_KEY not configured in .env")
    url = f"{settings.mistral_base_url.rstrip('/')}/chat/completions"
    payload = _chat_payload(settings.mistral_model, system, user)
    with httpx.Client(timeout=120.0) as client:
        resp = client.post(url, json=payload, headers=_auth_headers(settings.mistral_api_key))
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]


_ASYNC_CALLS: dict[str, Callable[[str, str], object]] = {
    "openai": _call_openai,
    "deepseek": _call_deepseek,
    "mistral": _call_mistral,
}

_SYNC_CALLS: dict[str, Callable[[str, str], str]] = {
    "openai": _call_openai_sync,
    "deepseek": _call_deepseek_sync,
    "mistral": _call_mistral_sync,
}


async def call_llm_with_fallback(system: str, user: str, *, provider: str | None = None) -> tuple[str, str]:
    errors: list[str] = []
    chain = providers_to_try(provider)
    for candidate in chain:
        try:
            raw = await _ASYNC_CALLS[candidate](system, user)
            if candidate != chain[0]:
                logger.warning("LLM fallback used: %s", candidate)
            return raw, candidate
        except Exception as exc:
            logger.warning("LLM provider %s failed: %s", candidate, exc)
            errors.append(f"{candidate}: {exc}")
    raise RuntimeError("All LLM providers failed. " + " | ".join(errors))


def call_llm_with_fallback_sync(system: str, user: str, *, provider: str | None = None) -> tuple[str, str]:
    errors: list[str] = []
    chain = providers_to_try(provider)
    for candidate in chain:
        try:
            raw = _SYNC_CALLS[candidate](system, user)
            if candidate != chain[0]:
                logger.warning("LLM fallback used: %s", candidate)
            return raw, candidate
        except Exception as exc:
            logger.warning("LLM provider %s failed: %s", candidate, exc)
            errors.append(f"{candidate}: {exc}")
    raise RuntimeError("All LLM providers failed. " + " | ".join(errors))
