"""Streamlit frontend for ORBIT Beraterprofil Generator (v3)."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import streamlit as st
import yaml

from app.services.cv_parser import extract_cv_text
from ui.pipeline import (
    apply_feedback_sync,
    cleanup_temp,
    export_pptx,
    generate_sync,
    import_from_pptx,
    llm_status,
    profile_from_json,
    profile_to_json,
    save_upload_temporarily,
    validate_for_export,
)
from ui.preview import render_hero, render_llm_badge, render_preview, render_stepper
from ui.settings_panel import render_settings_panel
from ui.styles import inject_styles

PROJECT_ROOT = Path(__file__).resolve().parent
CONFIG_PATH = PROJECT_ROOT / "config" / "domains.yaml"


def load_config() -> dict:
    if CONFIG_PATH.exists():
        return yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))
    return {"domains": [], "position_levels": ["Consultant"]}


def reset_session() -> None:
    for key in list(st.session_state.keys()):
        del st.session_state[key]


def init_session_state() -> None:
    defaults = {
        "profile_json": "",
        "pptx_path": "",
        "profile_source": "",
        "cv_raw_text": "",
        "manager_history": [],
        "photo_temp_path": None,
        "_export_done": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def clear_profile_state() -> None:
    st.session_state.profile_json = ""
    st.session_state.pptx_path = ""
    st.session_state.profile_source = ""
    st.session_state.cv_raw_text = ""
    st.session_state.manager_history = []
    st.session_state._export_done = False


def render_main_workflow(opts: dict, status: dict) -> None:
    st.markdown('<div class="orbit-main-panel">', unsafe_allow_html=True)

    render_hero()

    active_step = (
        "export"
        if st.session_state.get("_export_done")
        else ("review" if st.session_state.profile_json else "upload")
    )
    render_stepper(active_step)
    render_llm_badge(status["active"], status.get("provider"))

    st.markdown(
        '<div class="orbit-card"><div class="orbit-card-title">Schritt 1 - Profil laden</div>',
        unsafe_allow_html=True,
    )

    source_mode = st.radio(
        "Quelle",
        ["Neues Profil aus CV", "Bestehendes Beraterprofil (PPTX)"],
        horizontal=True,
        label_visibility="collapsed",
    )

    uploaded_cv = None
    uploaded_pptx = None

    if source_mode == "Neues Profil aus CV":
        uploaded_cv = st.file_uploader(
            "Lebenslauf hochladen (PDF oder DOCX)",
            type=["pdf", "docx"],
            label_visibility="collapsed",
            key="cv_upload",
        )
    else:
        uploaded_pptx = st.file_uploader(
            "Beraterprofil PowerPoint hochladen (.pptx)",
            type=["pptx"],
            label_visibility="collapsed",
            key="pptx_upload",
        )
        st.caption("Laden Sie ein bestehendes ORBIT-Beraterprofil zum Bearbeiten und Export.")

    st.markdown("</div>", unsafe_allow_html=True)

    col_action, col_new = st.columns([3, 1])
    with col_action:
        if source_mode == "Neues Profil aus CV":
            action_clicked = st.button(
                "Profil generieren",
                type="primary",
                disabled=uploaded_cv is None,
                use_container_width=True,
            )
        else:
            action_clicked = st.button(
                "Profil aus PPTX laden",
                type="primary",
                disabled=uploaded_pptx is None,
                use_container_width=True,
            )
    with col_new:
        if st.button("Neue Session", use_container_width=True, type="secondary"):
            reset_session()
            st.rerun()

    if action_clicked and uploaded_cv:
        clear_profile_state()
        cv_path = save_upload_temporarily(uploaded_cv)
        photo_path = None
        try:
            if opts["photo"]:
                photo_path = save_upload_temporarily(opts["photo"])
                st.session_state.photo_temp_path = str(photo_path)

            st.session_state.cv_raw_text = extract_cv_text(cv_path)
            st.session_state.profile_source = "cv"

            spinner = f"LLM extrahiert Profil ({opts['provider']}) ..."
            with st.spinner(spinner):
                out_path, profile = generate_sync(
                    cv_path,
                    photo_path=photo_path,
                    provider=opts["provider"],
                    position_override=opts["position_override"],
                )
                st.session_state.profile_json = profile_to_json(profile)
                st.session_state.pptx_path = str(out_path)
            st.success("Profil erstellt - bitte pruefen und exportieren.")
        except Exception as exc:
            st.error(f"Profil-Generierung fehlgeschlagen: {exc}")
        finally:
            cleanup_temp(cv_path)

    if action_clicked and uploaded_pptx:
        clear_profile_state()
        pptx_path = save_upload_temporarily(uploaded_pptx)
        try:
            with st.spinner("Beraterprofil aus PowerPoint wird gelesen ..."):
                profile = import_from_pptx(pptx_path)
                st.session_state.profile_json = profile_to_json(profile)
                st.session_state.profile_source = "pptx"
                st.session_state.cv_raw_text = ""
                st.session_state.pptx_path = str(pptx_path)
            st.success("Profil aus PPTX geladen.")
        except Exception as exc:
            st.error(f"PPTX konnte nicht gelesen werden: {exc}")
        finally:
            cleanup_temp(pptx_path)

    if st.session_state.profile_json:
        _render_results(opts, status)

    st.markdown("</div>", unsafe_allow_html=True)


def _render_manager_feedback(opts: dict, status: dict) -> None:
    st.markdown("---")
    st.markdown("#### Schritt 2 - Feedback (optional)")
    st.caption("Manager kann Kommentare geben. Bei CV-Profilen wird das CV als Quelle genutzt.")

    manager_comment = st.text_area(
        "Manager-Kommentar",
        placeholder="z.B. Schwerpunkte staerker auf 5G legen, Summary kuerzer formulieren ...",
        height=100,
        key="manager_comment_input",
    )

    can_revise = bool(st.session_state.profile_json) and status["active"]
    if st.session_state.profile_source == "cv" and not st.session_state.cv_raw_text:
        can_revise = False

    if st.button(
        "Profil mit Feedback aktualisieren",
        type="primary",
        disabled=not manager_comment.strip() or not can_revise,
        use_container_width=True,
    ):
        try:
            current = profile_from_json(st.session_state.profile_json)
            cv_text = st.session_state.cv_raw_text if st.session_state.profile_source == "cv" else None
            with st.spinner("LLM aktualisiert das Profil nach Feedback ..."):
                revised = apply_feedback_sync(
                    current,
                    manager_comment,
                    cv_text=cv_text,
                    provider=opts["provider"],
                )
                st.session_state.profile_json = profile_to_json(revised)
                st.session_state.manager_history.append(
                    {
                        "time": datetime.now().strftime("%H:%M:%S"),
                        "comment": manager_comment.strip(),
                    }
                )
                st.session_state._export_done = False
            st.success("Profil aktualisiert.")
            st.rerun()
        except Exception as exc:
            st.error(f"Feedback-Update fehlgeschlagen: {exc}")

    if not status["active"]:
        st.info("Feedback-Aktualisierung benoetigt einen konfigurierten LLM API-Key.")

    if st.session_state.manager_history:
        with st.expander(f"Feedback-Verlauf ({len(st.session_state.manager_history)})"):
            for entry in st.session_state.manager_history:
                st.markdown(
                    f'<div class="orbit-feedback-entry">'
                    f'<span class="orbit-feedback-time">{entry["time"]}</span>'
                    f"<span>{entry['comment']}</span></div>",
                    unsafe_allow_html=True,
                )


def _render_results(opts: dict, status: dict) -> None:
    st.markdown("---")
    try:
        profile = profile_from_json(st.session_state.profile_json)
    except json.JSONDecodeError as exc:
        st.error(f"JSON ungueltig: {exc}")
        return

    render_preview(profile)
    _render_manager_feedback(opts, status)

    with st.expander("JSON bearbeiten", expanded=False):
        edited = st.text_area(
            "Profil-JSON",
            st.session_state.profile_json,
            height=420,
            label_visibility="collapsed",
        )
        st.session_state.profile_json = edited
        try:
            profile = profile_from_json(edited)
        except json.JSONDecodeError as exc:
            st.error(f"JSON ungueltig: {exc}")
            return

    st.markdown("#### Schritt 3 - PowerPoint exportieren")
    can_export, issues = validate_for_export(profile)
    if can_export:
        st.success("Validierung bestanden - bereit fuer Export")
    else:
        st.error("Validierung fehlgeschlagen")
        for issue in issues:
            st.write(f"- {issue}")

    if st.button("PowerPoint erstellen", type="primary", disabled=not can_export):
        photo = (
            Path(st.session_state.photo_temp_path)
            if st.session_state.photo_temp_path
            else None
        )
        output = export_pptx(
            profile,
            photo_path=photo if photo and photo.exists() else None,
        )
        st.session_state.pptx_path = str(output)
        st.session_state._export_done = True
        st.success(f"Erstellt: {output.name}")

    pptx_path = Path(st.session_state.pptx_path) if st.session_state.pptx_path else None
    if pptx_path and pptx_path.exists():
        st.download_button(
            "PowerPoint herunterladen",
            data=pptx_path.read_bytes(),
            file_name=pptx_path.name,
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            use_container_width=True,
        )


def main() -> None:
    st.set_page_config(
        page_title="Beraterprofil Generator | ORBIT",
        page_icon="◆",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    inject_styles()
    init_session_state()
    config = load_config()
    status = llm_status()

    col_settings, col_main = st.columns([1, 2.4], gap="large")

    with col_settings:
        opts = render_settings_panel(config)

    with col_main:
        render_main_workflow(opts, status)


if __name__ == "__main__":
    main()
