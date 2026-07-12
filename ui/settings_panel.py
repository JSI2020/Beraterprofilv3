"""Settings panel for Streamlit app."""

from __future__ import annotations

import streamlit as st

from ui.pipeline import llm_status


def render_settings_panel(config: dict) -> dict:
    provider_names = {"deepseek": "DeepSeek", "mistral": "Mistral"}

    st.markdown('<div class="orbit-settings-column">', unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("### Einstellungen")
        st.caption("Profil-Optionen fuer diesen Lebenslauf")

        status = llm_status()
        if status["active"]:
            st.success(f"LLM aktiv - {provider_names.get(status['provider'], status['provider'])}")
        else:
            st.warning("Kein LLM API-Key in .env gefunden.")

        st.markdown("**Profil**")
        domain_options = ["Automatisch erkennen"] + config.get("domains", [])
        domain_choice = st.selectbox("Fachgebiet (optional)", domain_options)
        domain = None if domain_choice == "Automatisch erkennen" else domain_choice

        position_levels = config.get("position_levels", ["Consultant", "Senior Consultant"])
        position_override = st.selectbox("Position (optional)", ["Aus CV ableiten"] + position_levels)

        st.markdown("**Generierung**")
        provider = st.selectbox(
            "LLM Provider",
            ["deepseek", "mistral"],
            format_func=lambda p: provider_names.get(p, p),
        )

        st.markdown("**Optional**")
        photo = st.file_uploader("Beraterfoto", type=["jpg", "jpeg", "png", "webp"])
    st.markdown("</div>", unsafe_allow_html=True)

    return {
        "domain": domain,
        "position_override": position_override,
        "provider": provider,
        "photo": photo,
    }
