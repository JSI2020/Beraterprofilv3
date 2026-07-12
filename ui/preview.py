"""Three-column profile preview for Streamlit (v3 schema)."""

from __future__ import annotations

import html

import streamlit as st

from app.schemas.profile import BeraterprofilData


def render_hero() -> None:
    st.markdown(
        """
        <div class="orbit-hero">
            <span class="orbit-hero-eyebrow">⚡ ORBIT IT-Solutions · Beraterprofil-Generator</span>
            <h1>Aus jedem Lebenslauf in Sekunden ein Beraterprofil</h1>
            <p>Laden Sie einen Lebenslauf hoch — die KI erstellt eine personalisierte, markengerechte
            ORBIT-Einseiter-Präsentation auf Deutsch. Funktioniert für jedes Fachgebiet: Telekom, IT,
            Software, Cloud, Security, ERP/CRM, BI, Projektmanagement.</p>
            <div class="orbit-hero-chips">
                <span class="orbit-hero-chip">🌐 Jede Branche</span>
                <span class="orbit-hero-chip">🇩🇪 Deutsche Ausgabe</span>
                <span class="orbit-hero-chip">🧩 Festes ORBIT-Template</span>
                <span class="orbit-hero-chip">📐 Striktes Layout</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_stepper(active: str) -> None:
    steps = [
        ("1", "Lebenslauf laden", "upload"),
        ("2", "Prüfen", "review"),
        ("3", "Exportieren", "export"),
    ]
    order = ["upload", "review", "export"]
    active_idx = order.index(active)

    parts = ['<div class="orbit-stepper">']
    for i, (num, label, key) in enumerate(steps):
        state = "is-active" if key == active else ("is-done" if order.index(key) < active_idx else "")
        icon = "✓" if state == "is-done" else num
        parts.append(f'<div class="orbit-step {state}"><span class="orbit-step-num">{icon}</span>{label}</div>')
        if i < len(steps) - 1:
            parts.append('<span class="orbit-step-arrow">→</span>')
    parts.append("</div>")
    st.markdown("".join(parts), unsafe_allow_html=True)


def render_llm_badge(active: bool, provider: str | None = None) -> None:
    provider_names = {
        "deepseek": "DeepSeek",
        "mistral": "Mistral",
    }
    if active:
        label = f"LLM aktiv · {provider_names.get(provider or '', provider)}" if provider else "LLM aktiv"
        st.markdown(
            f'<span class="orbit-badge orbit-badge-ok"><span class="orbit-badge-dot"></span>{label}</span>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<span class="orbit-badge orbit-badge-warn"><span class="orbit-badge-dot"></span>'
            "Kein API-Key konfiguriert</span>",
            unsafe_allow_html=True,
        )


def _esc(text: str) -> str:
    return html.escape(text, quote=False)


def _chips(items: list[str]) -> str:
    if not items:
        return ""
    return (
        '<div class="orbit-chip-row">'
        + "".join(f'<span class="orbit-chip">{_esc(i)}</span>' for i in items)
        + "</div>"
    )


def render_preview(profile: BeraterprofilData) -> None:
    title = f"Beraterprofil – {profile.title_domain}"
    st.markdown(
        f"""
        <div class="orbit-preview-titlebar">
            <h3>{_esc(title)}</h3>
            <span class="orbit-preview-meta">{_esc(profile.position)}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col1, col2, col3 = st.columns(3)

    with col1:
        parts = ['<div class="orbit-preview-col">']
        parts.append('<div class="orbit-section-label">🎯 Schwerpunkte</div>')
        parts.append(_chips([s.strip() for s in profile.schwerpunkte.split(",") if s.strip()]))
        parts.append('<div class="orbit-section-label">📝 Summary</div>')
        parts.append(f"<p>{_esc(profile.summary)}</p>")
        parts.append('<div class="orbit-section-label">🧠 Kompetenzen</div>')
        if profile.kompetenzen:
            parts.append("<ul>" + "".join(f"<li>{_esc(k)}</li>" for k in profile.kompetenzen) + "</ul>")
        parts.append("</div>")
        st.markdown("".join(parts), unsafe_allow_html=True)

    with col2:
        parts = ['<div class="orbit-preview-col">']
        parts.append('<div class="orbit-section-label">📁 Relevante Erfahrungen / Projekte</div>')
        for item in profile.relevante_erfahrungen:
            parts.append(f"<p><strong>{_esc(item.label)}</strong> — {_esc(item.beschreibung)}</p>")
        parts.append('<div class="orbit-section-label">🛠️ Tool-Kenntnisse</div>')
        tools = profile.tool_kenntnisse
        tool_rows = [
            ("OSS / Command Management", tools.oss_command_management),
            ("Statistik und Analyse", tools.statistik_analyse),
            ("Planung und Optimierung", tools.planung_optimierung),
            ("Drive Test und Post-Processing", tools.drive_test_post_processing),
            ("Mapping", tools.mapping),
        ]
        for label, value in tool_rows:
            if value:
                parts.append(f"<p><strong>{_esc(label)}</strong> — {_esc(value)}</p>")
        parts.append("</div>")
        st.markdown("".join(parts), unsafe_allow_html=True)

    with col3:
        parts = ['<div class="orbit-preview-col">']
        parts.append('<div class="orbit-section-label">🌍 Ausbildung / Karriere</div>')
        if profile.ausbildung_karriere:
            parts.append(
                "<ul>"
                + "".join(f"<li>{_esc(line)}</li>" for line in profile.ausbildung_karriere)
                + "</ul>"
            )
        parts.append('<div class="orbit-section-label">🎓 Abschluss / Zertifikate</div>')
        if profile.abschluss_zertifikate:
            parts.append(
                "<ul>"
                + "".join(f"<li>{_esc(line)}</li>" for line in profile.abschluss_zertifikate)
                + "</ul>"
            )
        parts.append("</div>")
        st.markdown("".join(parts), unsafe_allow_html=True)
