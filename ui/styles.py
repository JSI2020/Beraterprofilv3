"""Inject DESIGN.md tokens as Streamlit custom CSS."""

from __future__ import annotations

DESIGN_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500&display=swap');

:root {
    --orbit-bg: #EEF3F7;
    --orbit-surface: #FFFFFF;
    --orbit-text: #0F172A;
    --orbit-label: #0F172A;
    --orbit-muted: #64748B;
    --orbit-border: #DCE4EC;
    --orbit-input-bg: #FFFFFF;
    --orbit-accent: #0891B2;
    --orbit-accent-2: #06B6D4;
    --orbit-accent-soft: #E0F7FA;
    --orbit-navy: #0F172A;
    --orbit-navy-2: #1E3A5F;
    --orbit-glow: rgba(6, 182, 212, 0.35);
}

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', 'Segoe UI', sans-serif;
    color: #0F172A !important;
}

/* === GLOBAL READABILITY (fixes white/invisible labels) === */
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] main,
[data-testid="stAppViewContainer"] section {
    color: #0F172A !important;
}

[data-testid="stAppViewContainer"] h1,
[data-testid="stAppViewContainer"] h2,
[data-testid="stAppViewContainer"] h3,
[data-testid="stAppViewContainer"] h4,
[data-testid="stAppViewContainer"] h5,
[data-testid="stAppViewContainer"] h6,
[data-testid="stAppViewContainer"] p,
[data-testid="stAppViewContainer"] label,
[data-testid="stAppViewContainer"] span,
[data-testid="stAppViewContainer"] li,
[data-testid="stAppViewContainer"] strong,
[data-testid="stAppViewContainer"] [data-testid="stMarkdownContainer"] p,
[data-testid="stAppViewContainer"] [data-testid="stMarkdownContainer"] strong,
[data-testid="stAppViewContainer"] [data-testid="stMarkdownContainer"] h1,
[data-testid="stAppViewContainer"] [data-testid="stMarkdownContainer"] h2,
[data-testid="stAppViewContainer"] [data-testid="stMarkdownContainer"] h3,
[data-testid="stAppViewContainer"] [data-testid="stMarkdownContainer"] h4,
[data-testid="stAppViewContainer"] [data-testid="stWidgetLabel"] p,
[data-testid="stAppViewContainer"] [data-testid="stWidgetLabel"] label,
[data-testid="stAppViewContainer"] .stRadio label span,
[data-testid="stAppViewContainer"] .stCheckbox label span {
    color: #0F172A !important;
    -webkit-text-fill-color: #0F172A !important;
    opacity: 1 !important;
}

[data-testid="stAppViewContainer"] [data-testid="stCaptionContainer"] p {
    color: #475569 !important;
    -webkit-text-fill-color: #475569 !important;
}

/* Bordered settings card */
[data-testid="stAppViewContainer"] [data-testid="stVerticalBlockBorderWrapper"] {
    background: #FFFFFF !important;
    border-color: #DCE4EC !important;
}
[data-testid="stAppViewContainer"] [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stMarkdownContainer"] p,
[data-testid="stAppViewContainer"] [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stMarkdownContainer"] strong,
[data-testid="stAppViewContainer"] [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stWidgetLabel"] p,
[data-testid="stAppViewContainer"] [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stWidgetLabel"] label,
[data-testid="stAppViewContainer"] [data-testid="stVerticalBlockBorderWrapper"] label {
    color: #0F172A !important;
    -webkit-text-fill-color: #0F172A !important;
}
[data-testid="stAppViewContainer"] [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stCaptionContainer"] p {
    color: #475569 !important;
    -webkit-text-fill-color: #475569 !important;
}

/* Select / dropdown: light background, dark text */
[data-testid="stAppViewContainer"] [data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    color: #0F172A !important;
    border: 1.5px solid #DCE4EC !important;
}
[data-testid="stAppViewContainer"] [data-baseweb="select"] span,
[data-testid="stAppViewContainer"] [data-baseweb="select"] div,
[data-testid="stAppViewContainer"] [data-baseweb="select"] input {
    color: #0F172A !important;
    -webkit-text-fill-color: #0F172A !important;
    background-color: #FFFFFF !important;
}

/* File uploader */
[data-testid="stAppViewContainer"] [data-testid="stFileUploader"] section {
    background: #FFFFFF !important;
    border: 1.5px dashed #DCE4EC !important;
}
[data-testid="stAppViewContainer"] [data-testid="stFileUploader"] span,
[data-testid="stAppViewContainer"] [data-testid="stFileUploader"] small,
[data-testid="stAppViewContainer"] [data-testid="stFileUploader"] p,
[data-testid="stAppViewContainer"] [data-testid="stFileUploader"] button,
[data-testid="stAppViewContainer"] [data-testid="stFileUploader"] button p,
[data-testid="stAppViewContainer"] [data-testid="stFileUploader"] label {
    color: #0F172A !important;
    -webkit-text-fill-color: #0F172A !important;
}

/* Text areas */
[data-testid="stAppViewContainer"] textarea {
    color: #0F172A !important;
    -webkit-text-fill-color: #0F172A !important;
    background: #FFFFFF !important;
    border: 1.5px solid #DCE4EC !important;
}

/* First column (settings) - extra specificity */
.block-container div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:first-child [data-testid="stMarkdownContainer"] p,
.block-container div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:first-child [data-testid="stMarkdownContainer"] strong,
.block-container div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:first-child [data-testid="stWidgetLabel"] p,
.block-container div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:first-child [data-testid="stWidgetLabel"] label,
.block-container div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:first-child label {
    color: #0F172A !important;
    -webkit-text-fill-color: #0F172A !important;
}
.block-container div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:first-child [data-testid="stCaptionContainer"] p {
    color: #475569 !important;
    -webkit-text-fill-color: #475569 !important;
}

.stApp {
    background:
        radial-gradient(1200px 500px at 85% -10%, rgba(8, 145, 178, 0.10), transparent 60%),
        radial-gradient(900px 400px at -5% 10%, rgba(30, 58, 95, 0.08), transparent 55%),
        var(--orbit-bg);
}

.block-container {
    padding-top: 1.1rem;
    padding-bottom: 2.5rem;
    max-width: 1320px;
}

@keyframes orbitFadeUp {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes orbitDrift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
@keyframes orbitPulse {
    0%   { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.45); }
    70%  { box-shadow: 0 0 0 7px rgba(16, 185, 129, 0); }
    100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}
@keyframes orbitPulseWarn {
    0%   { box-shadow: 0 0 0 0 rgba(217, 119, 6, 0.4); }
    70%  { box-shadow: 0 0 0 7px rgba(217, 119, 6, 0); }
    100% { box-shadow: 0 0 0 0 rgba(217, 119, 6, 0); }
}

/* â”€â”€ Settings column = first column in main layout â”€â”€ */
.block-container div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:first-child {
    background: transparent;
}
.block-container div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:first-child h3,
.block-container div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:first-child strong {
    color: var(--orbit-text) !important;
}
.block-container div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:first-child [data-testid="stCaptionContainer"] p {
    color: var(--orbit-muted) !important;
}
.block-container div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:first-child label p,
.block-container div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:first-child [data-testid="stWidgetLabel"] p {
    color: var(--orbit-label) !important;
    font-weight: 600 !important;
    font-size: 0.84rem !important;
}
.block-container div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:first-child [data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    border: 1.5px solid var(--orbit-border) !important;
    border-radius: 10px !important;
    transition: border-color 0.15s ease, box-shadow 0.15s ease;
}
.block-container div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:first-child [data-baseweb="select"] > div:focus-within {
    border-color: var(--orbit-accent) !important;
    box-shadow: 0 0 0 3px var(--orbit-accent-soft) !important;
}
.block-container div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:first-child [data-baseweb="select"] * {
    color: #0F172A !important;
    -webkit-text-fill-color: #0F172A !important;
    opacity: 1 !important;
}
.block-container div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:first-child textarea {
    background: #FFFFFF !important;
    color: #0F172A !important;
    border: 1.5px solid var(--orbit-border) !important;
    border-radius: 10px !important;
}
.block-container div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:first-child textarea::placeholder {
    color: #64748B !important;
    opacity: 1 !important;
}
.block-container div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:first-child .stCheckbox label span {
    color: #0F172A !important;
    font-weight: 500 !important;
}
.block-container div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:first-child [data-testid="stFileUploader"] section {
    background: #FFFFFF !important;
    border: 1.5px dashed var(--orbit-border) !important;
}
.block-container div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:first-child [data-testid="stFileUploader"] * {
    color: #0F172A !important;
}
.block-container div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:first-child [data-testid="stVerticalBlockBorderWrapper"] {
    background: #FFFFFF !important;
    border-color: var(--orbit-border) !important;
    border-radius: 18px !important;
    box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04), 0 12px 28px -14px rgba(15, 23, 42, 0.12) !important;
}

/* â”€â”€ Settings wrap (legacy) â”€â”€ */
.orbit-settings-wrap [data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--orbit-surface) !important;
    border-color: var(--orbit-border) !important;
    border-radius: 16px !important;
}
.orbit-settings-wrap h3 { color: var(--orbit-text) !important; }
.orbit-settings-wrap .stCaption,
.orbit-settings-wrap [data-testid="stCaptionContainer"] p { color: var(--orbit-muted) !important; }
.orbit-settings-wrap strong,
.orbit-settings-wrap [data-testid="stMarkdownContainer"] p { color: var(--orbit-text) !important; }
.orbit-settings-wrap label,
.orbit-settings-wrap [data-testid="stWidgetLabel"] p {
    color: var(--orbit-label) !important;
    font-weight: 600 !important;
    font-size: 0.84rem !important;
}
.orbit-settings-wrap [data-baseweb="select"] > div {
    background-color: var(--orbit-input-bg) !important;
    border: 1.5px solid var(--orbit-border) !important;
    border-radius: 10px !important;
    color: var(--orbit-text) !important;
}
.orbit-settings-wrap [data-baseweb="select"] span,
.orbit-settings-wrap [data-baseweb="select"] div[aria-selected],
.orbit-settings-wrap [data-baseweb="select"] div[value] {
    color: var(--orbit-text) !important;
    -webkit-text-fill-color: var(--orbit-text) !important;
    opacity: 1 !important;
}
.orbit-settings-wrap textarea {
    background: var(--orbit-input-bg) !important;
    color: var(--orbit-text) !important;
    border: 1.5px solid var(--orbit-border) !important;
    border-radius: 10px !important;
}
.orbit-settings-wrap textarea::placeholder { color: #94A3B8 !important; opacity: 1 !important; }
.orbit-settings-wrap .stCheckbox label span { color: var(--orbit-text) !important; font-weight: 500 !important; }
.orbit-settings-wrap [data-testid="stFileUploader"] section {
    background: var(--orbit-input-bg) !important;
    border: 1.5px dashed var(--orbit-border) !important;
}
.orbit-settings-wrap [data-testid="stFileUploader"] span,
.orbit-settings-wrap [data-testid="stFileUploader"] small,
.orbit-settings-wrap [data-testid="stFileUploader"] p,
.orbit-settings-wrap [data-testid="stFileUploader"] button p { color: var(--orbit-text) !important; }

/* â”€â”€ Settings panel (legacy) â”€â”€ */
.orbit-settings-panel {
    background: var(--orbit-surface);
    border: 1px solid var(--orbit-border);
    border-radius: 18px;
    padding: 1.25rem 1.35rem;
    box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04), 0 12px 28px -14px rgba(15, 23, 42, 0.12);
    position: sticky;
    top: 1rem;
}
.orbit-settings-panel h3 {
    color: var(--orbit-text) !important;
    font-size: 1.1rem !important;
    font-weight: 800 !important;
    margin: 0 0 0.2rem 0 !important;
}
.orbit-settings-panel .orbit-caption { color: var(--orbit-muted); font-size: 0.85rem; margin-bottom: 1rem; }
.orbit-settings-section { margin-bottom: 1.1rem; padding-bottom: 1rem; border-bottom: 1px solid #E2E8F0; }
.orbit-settings-section:last-child { border-bottom: none; margin-bottom: 0; padding-bottom: 0; }
.orbit-settings-section-title {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.09em;
    text-transform: uppercase;
    color: var(--orbit-accent);
    margin-bottom: 0.65rem;
}

.orbit-settings-panel label,
.orbit-settings-panel [data-testid="stWidgetLabel"] p {
    color: var(--orbit-label) !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
}
.orbit-settings-panel [data-baseweb="select"] > div {
    background-color: var(--orbit-input-bg) !important;
    border: 1.5px solid var(--orbit-border) !important;
    border-radius: 10px !important;
    color: var(--orbit-text) !important;
    min-height: 42px !important;
}
.orbit-settings-panel [data-baseweb="select"] span,
.orbit-settings-panel [data-baseweb="select"] div { color: var(--orbit-text) !important; -webkit-text-fill-color: var(--orbit-text) !important; }
.orbit-settings-panel textarea {
    background: var(--orbit-input-bg) !important;
    color: var(--orbit-text) !important;
    border: 1.5px solid var(--orbit-border) !important;
    border-radius: 10px !important;
    font-size: 0.92rem !important;
}
.orbit-settings-panel textarea::placeholder { color: #94A3B8 !important; }
.orbit-settings-panel .stCheckbox label span { color: var(--orbit-text) !important; font-size: 0.92rem !important; font-weight: 500 !important; }
.orbit-settings-panel [data-testid="stFileUploader"] section {
    background: var(--orbit-input-bg) !important;
    border: 1.5px dashed var(--orbit-border) !important;
    border-radius: 12px !important;
}
.orbit-settings-panel [data-testid="stFileUploader"] span,
.orbit-settings-panel [data-testid="stFileUploader"] small,
.orbit-settings-panel [data-testid="stFileUploader"] p { color: var(--orbit-text) !important; }

/* â”€â”€ Hero â”€â”€ */
.orbit-hero {
    position: relative;
    overflow: hidden;
    background: linear-gradient(115deg, #0B1220 0%, #0F2942 32%, #0E5C6E 68%, #0891B2 100%);
    background-size: 220% 220%;
    animation: orbitDrift 16s ease-in-out infinite;
    border-radius: 22px;
    padding: 2rem 2.25rem;
    margin-bottom: 1.1rem;
    color: #fff;
    box-shadow: 0 20px 48px rgba(8, 20, 35, 0.28);
}
.orbit-hero::before {
    content: "";
    position: absolute;
    inset: 0;
    background:
        radial-gradient(420px 220px at 88% -20%, rgba(255,255,255,0.16), transparent 60%),
        radial-gradient(360px 200px at 8% 120%, rgba(6,182,212,0.25), transparent 60%);
    pointer-events: none;
}
.orbit-hero-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #A5F3FC;
    background: rgba(6, 182, 212, 0.15);
    border: 1px solid rgba(165, 243, 252, 0.35);
    padding: 0.3rem 0.7rem;
    border-radius: 999px;
    margin-bottom: 0.85rem;
    position: relative;
}
.orbit-hero h1 {
    position: relative;
    color: #fff !important;
    font-size: 2rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.01em;
    margin: 0 0 0.4rem 0 !important;
}
.orbit-hero p {
    position: relative;
    color: rgba(255,255,255,0.86) !important;
    margin: 0 0 1.1rem 0;
    font-size: 0.98rem;
    line-height: 1.55;
    max-width: 640px;
}
.orbit-hero-chips { position: relative; display: flex; flex-wrap: wrap; gap: 0.5rem; }
.orbit-hero-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    font-size: 0.78rem;
    font-weight: 600;
    color: #E6FBFF;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.16);
    padding: 0.32rem 0.75rem;
    border-radius: 999px;
    backdrop-filter: blur(4px);
}

/* â”€â”€ Stepper â”€â”€ */
.orbit-stepper {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin: 0.2rem 0 1.1rem 0;
    flex-wrap: wrap;
}
.orbit-step {
    display: flex;
    align-items: center;
    gap: 0.55rem;
    background: var(--orbit-surface);
    border: 1px solid var(--orbit-border);
    border-radius: 999px;
    padding: 0.4rem 0.9rem 0.4rem 0.5rem;
    font-size: 0.82rem;
    font-weight: 600;
    color: var(--orbit-muted);
    box-shadow: 0 1px 2px rgba(15,23,42,0.03);
    transition: all 0.2s ease;
}
.orbit-step-num {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 22px;
    height: 22px;
    border-radius: 50%;
    background: #E2E8F0;
    color: #475569;
    font-size: 0.72rem;
    font-weight: 800;
}
.orbit-step.is-active {
    color: var(--orbit-navy);
    border-color: var(--orbit-accent);
    box-shadow: 0 0 0 3px var(--orbit-accent-soft);
}
.orbit-step.is-active .orbit-step-num {
    background: linear-gradient(135deg, #0891B2, #06B6D4);
    color: #fff;
}
.orbit-step.is-done .orbit-step-num { background: #059669; color: #fff; }
.orbit-step.is-done { color: #059669; }
.orbit-step-arrow { color: #CBD5E1; font-size: 0.9rem; }

/* â”€â”€ Cards â”€â”€ */
.orbit-card {
    background: var(--orbit-surface);
    border: 1px solid var(--orbit-border);
    border-radius: 18px;
    padding: 1.3rem 1.45rem;
    margin-bottom: 0.9rem;
    box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
    animation: orbitFadeUp 0.35s ease both;
}
.orbit-card-title {
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--orbit-muted);
    margin-bottom: 0.85rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}

/* â”€â”€ Badges â”€â”€ */
.orbit-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.4rem 0.9rem;
    border-radius: 999px;
    font-size: 0.8rem;
    font-weight: 700;
    margin-bottom: 0.85rem;
}
.orbit-badge-dot { width: 8px; height: 8px; border-radius: 50%; flex: none; }
.orbit-badge-ok { background: #ECFDF5; color: #065F46; border: 1px solid #A7F3D0; }
.orbit-badge-ok .orbit-badge-dot { background: #10B981; animation: orbitPulse 2s infinite; }
.orbit-badge-warn { background: #FFFBEB; color: #92400E; border: 1px solid #FDE68A; }
.orbit-badge-warn .orbit-badge-dot { background: #D97706; animation: orbitPulseWarn 2s infinite; }

/* â”€â”€ Main upload â”€â”€ */
.orbit-main-panel [data-testid="stFileUploader"] section {
    border: 2px dashed #B9C6D6 !important;
    border-radius: 16px !important;
    background: linear-gradient(180deg, #F8FBFD 0%, #F1F6FA 100%) !important;
    transition: border-color 0.2s ease, background 0.2s ease;
}
.orbit-main-panel [data-testid="stFileUploader"] section:hover {
    border-color: var(--orbit-accent) !important;
    background: var(--orbit-accent-soft) !important;
}
.orbit-main-panel [data-testid="stFileUploader"] span,
.orbit-main-panel [data-testid="stFileUploader"] small { color: var(--orbit-muted) !important; }

/* â”€â”€ Buttons â”€â”€ */
.stButton > button[kind="primary"],
.stButton > button[kind="primary"] p,
.stButton > button[kind="primary"] span {
    background: linear-gradient(135deg, #0891B2, #0EA5C4 45%, #06B6D4) !important;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease !important;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-1px);
    box-shadow: 0 10px 22px -8px rgba(8, 145, 178, 0.55) !important;
}
.stButton > button[kind="secondary"],
.stButton > button[kind="secondary"] p {
    background: #FFFFFF !important;
    color: var(--orbit-text) !important;
    border: 1.5px solid var(--orbit-border) !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    transition: border-color 0.15s ease, background 0.15s ease !important;
}
.stButton > button[kind="secondary"]:hover { border-color: var(--orbit-accent) !important; background: var(--orbit-accent-soft) !important; }

/* â”€â”€ Slide-style preview â”€â”€ */
.orbit-preview-frame {
    background: linear-gradient(180deg, #FBFDFE 0%, #F5F9FB 100%);
    border: 1px solid var(--orbit-border);
    border-radius: 20px;
    padding: 1.1rem;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.6), 0 1px 2px rgba(15,23,42,0.04);
    margin-bottom: 0.9rem;
}
.orbit-preview-titlebar {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    gap: 0.75rem;
    padding: 0.15rem 0.4rem 0.9rem 0.4rem;
    border-bottom: 2px solid var(--orbit-navy);
    margin-bottom: 0.9rem;
    flex-wrap: wrap;
}
.orbit-preview-titlebar h3 {
    margin: 0 !important;
    font-size: 1.18rem !important;
    font-weight: 800 !important;
    color: var(--orbit-navy) !important;
}
.orbit-preview-meta { font-size: 0.83rem; color: var(--orbit-muted); font-weight: 600; }

.orbit-preview-col {
    background: var(--orbit-surface);
    border: 1px solid var(--orbit-border);
    border-radius: 14px;
    padding: 1rem 1.1rem;
    min-height: 280px;
    height: 100%;
    transition: box-shadow 0.2s ease, transform 0.2s ease;
}
.orbit-preview-col:hover { box-shadow: 0 10px 26px -16px rgba(15,23,42,0.25); }
.orbit-section-label {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.68rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--orbit-accent);
    margin: 0.9rem 0 0.4rem 0;
}
.orbit-section-label:first-child { margin-top: 0; }
.orbit-preview-col p, .orbit-preview-col li { color: var(--orbit-text) !important; font-size: 0.9rem; line-height: 1.45; }
.orbit-preview-col ul { margin: 0 0 0.2rem 0; padding-left: 1.15rem; }
.orbit-chip-row { display: flex; flex-wrap: wrap; gap: 0.35rem; margin-bottom: 0.3rem; }
.orbit-chip {
    display: inline-flex;
    font-size: 0.78rem;
    font-weight: 600;
    color: #0E5C6E;
    background: var(--orbit-accent-soft);
    border: 1px solid #B7E9F0;
    padding: 0.2rem 0.6rem;
    border-radius: 8px;
}

.orbit-warning {
    background: #FFFBEB;
    border-left: 4px solid #D97706;
    border-radius: 8px;
    padding: 0.7rem 1rem;
    color: #78350F;
    font-size: 0.88rem;
    margin-bottom: 0.5rem;
}

/* â”€â”€ Feedback log strip â”€â”€ */
.orbit-feedback-entry {
    display: flex;
    gap: 0.6rem;
    align-items: flex-start;
    padding: 0.5rem 0;
    border-bottom: 1px dashed #E2E8F0;
    font-size: 0.86rem;
}
.orbit-feedback-entry:last-child { border-bottom: none; }
.orbit-feedback-time {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: var(--orbit-muted);
    background: #F1F5F9;
    padding: 0.15rem 0.4rem;
    border-radius: 6px;
    flex: none;
}

#MainMenu { visibility: hidden; }
footer { visibility: hidden; }

/* Readable text in settings column (fix white-on-white labels) */
.orbit-settings-column,
.orbit-settings-column [data-testid="stVerticalBlockBorderWrapper"] {
    color: #0F172A !important;
}
.orbit-settings-column h1,
.orbit-settings-column h2,
.orbit-settings-column h3,
.orbit-settings-column h4,
.orbit-settings-column p,
.orbit-settings-column strong,
.orbit-settings-column label,
.orbit-settings-column span,
.orbit-settings-column [data-testid="stMarkdownContainer"] p,
.orbit-settings-column [data-testid="stMarkdownContainer"] strong,
.orbit-settings-column [data-testid="stWidgetLabel"] p,
.orbit-settings-column [data-testid="stCaptionContainer"] p {
    color: #0F172A !important;
    -webkit-text-fill-color: #0F172A !important;
    opacity: 1 !important;
}
.orbit-settings-column [data-testid="stCaptionContainer"] p {
    color: #475569 !important;
    -webkit-text-fill-color: #475569 !important;
}
.orbit-settings-column [data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    color: #0F172A !important;
    border: 1.5px solid var(--orbit-border) !important;
}
.orbit-settings-column [data-baseweb="select"] span,
.orbit-settings-column [data-baseweb="select"] div {
    color: #0F172A !important;
    -webkit-text-fill-color: #0F172A !important;
}
.orbit-settings-column [data-testid="stFileUploader"] section {
    background: #FFFFFF !important;
    border: 1.5px dashed var(--orbit-border) !important;
}
.orbit-settings-column [data-testid="stFileUploader"] span,
.orbit-settings-column [data-testid="stFileUploader"] small,
.orbit-settings-column [data-testid="stFileUploader"] p,
.orbit-settings-column [data-testid="stFileUploader"] button,
.orbit-settings-column [data-testid="stFileUploader"] button p {
    color: #0F172A !important;
    -webkit-text-fill-color: #0F172A !important;
}

/* Main panel labels and feedback */
.orbit-main-panel label,
.orbit-main-panel [data-testid="stWidgetLabel"] p,
.orbit-main-panel h4,
.orbit-main-panel [data-testid="stMarkdownContainer"] p {
    color: #0F172A !important;
    -webkit-text-fill-color: #0F172A !important;
}
.orbit-main-panel [data-testid="stCaptionContainer"] p {
    color: #475569 !important;
}
.orbit-main-panel textarea {
    color: #0F172A !important;
    background: #FFFFFF !important;
    border: 1.5px solid var(--orbit-border) !important;
}
.orbit-main-panel [data-testid="stRadio"] label span {
    color: #0F172A !important;
    font-weight: 600 !important;
}
"""


def inject_styles() -> None:
    import streamlit as st

    st.markdown(f"<style>{DESIGN_CSS}</style>", unsafe_allow_html=True)
