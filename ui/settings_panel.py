"""Settings panel for Streamlit app."""

from __future__ import annotations

import streamlit as st

from app.services.llm_providers import PROVIDER_LABELS, PROVIDER_ORDER, available_providers
from ui.pipeline import llm_status


def render_settings_panel(config: dict) -> dict:
    status = llm_status()
    available = set(available_providers())

    with st.container(border=True):
        st.markdown(
            '<p style="color:#0F172A;font-weight:800;font-size:1.1rem;margin:0 0 0.25rem 0;">'
            "Einstellungen</p>",
            unsafe_allow_html=True,
        )
        st.markdown(
            '<p style="color:#475569;font-size:0.85rem;margin:0 0 1rem 0;">'
            "Profil-Optionen fuer diesen Lebenslauf</p>",
            unsafe_allow_html=True,
        )

        if status["active"]:
            label = PROVIDER_LABELS.get(status["provider"], status["provider"])
            model = status.get("model") or ""
            st.success(f"LLM aktiv - {label} ({model})")
            if status.get("fallback_chain"):
                fallbacks = ", ".join(
                    PROVIDER_LABELS.get(p, p) for p in status["fallback_chain"]
                )
                st.caption(f"Fallback: {fallbacks}")
        else:
            st.warning("Kein LLM API-Key in .env gefunden.")

        st.markdown(
            '<p style="color:#06B6D4;font-weight:700;font-size:0.75rem;'
            'letter-spacing:0.06em;text-transform:uppercase;margin:0.75rem 0 0.5rem 0;">Profil</p>',
            unsafe_allow_html=True,
        )
        domain_options = ["Automatisch erkennen"] + config.get("domains", [])
        domain_choice = st.selectbox("Fachgebiet (optional)", domain_options)
        domain = None if domain_choice == "Automatisch erkennen" else domain_choice

        position_levels = config.get("position_levels", ["Consultant", "Senior Consultant"])
        position_override = st.selectbox("Position (optional)", ["Aus CV ableiten"] + position_levels)

        st.markdown(
            '<p style="color:#06B6D4;font-weight:700;font-size:0.75rem;'
            'letter-spacing:0.06em;text-transform:uppercase;margin:0.75rem 0 0.5rem 0;">Generierung</p>',
            unsafe_allow_html=True,
        )
        provider_options = list(PROVIDER_ORDER)
        provider = st.selectbox(
            "LLM Provider",
            provider_options,
            key="llm_provider_select",
            format_func=lambda p: (
                f"{PROVIDER_LABELS.get(p, p)} (Priorität 1)"
                if p == "openai"
                else PROVIDER_LABELS.get(p, p)
            )
            + ("" if p in available else " - kein API-Key"),
        )

        st.markdown(
            '<p style="color:#06B6D4;font-weight:700;font-size:0.75rem;'
            'letter-spacing:0.06em;text-transform:uppercase;margin:0.75rem 0 0.5rem 0;">Optional</p>',
            unsafe_allow_html=True,
        )
        photo = st.file_uploader("Beraterfoto", type=["jpg", "jpeg", "png", "webp"])

    return {
        "domain": domain,
        "position_override": position_override,
        "provider": provider,
        "photo": photo,
    }
