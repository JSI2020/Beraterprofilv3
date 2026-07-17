"""Enforce one-page limits and correct section semantics."""

from __future__ import annotations

import re

from app.schemas.profile import BeraterprofilData, RelevantExperience, ToolKenntnisse

LIMITS = {
    "title_domain": 28,
    "position": 22,
    "schwerpunkte": 50,
    "summary": 400,
    "kompetenzen_count": 7,
    "kompetenzen_item": 48,
    "relevante_count": 5,
    "relevante_label": 40,
    "relevante_desc": 58,
    "ausbildung_count": 4,
    "ausbildung_item": 72,
    "abschluss_count": 6,
    "abschluss_item": 78,
    "tool_category": 52,
}

_DEGREE_RE = re.compile(
    r"(^|\b)(19|20)\d{2}(\b|,)|"
    r"\b(Bachelor|Master|B\.?\s*E\.?|B\.?\s*S\.?|M\.?\s*Sc|M\.?\s*S\.?|"
    r"Diplom|Ph\.?D|MBA|SSC|F\.?\s*Sc|D\.?\s*T\.?\s*T|Abschluss|Zertifikat|"
    r"University|Universität|College|FUUAST|NED University|Karachi)\b",
    re.IGNORECASE,
)

_CAREER_HINTS = re.compile(
    r"\b(Projekt|Einsatz|Kunde|international|Regional|Lead|Consultant|"
    r"Erfahrung|Zusammenarbeit|Vendor|Operator|Netzbetreiber|Länder|"
    r"Pakistan|Deutschland|Telekom|Huawei|Ericsson|ORBIT)\b",
    re.IGNORECASE,
)


def _trunc(text: str, max_len: int, end: str = "") -> str:
    text = re.sub(r"\s+", " ", (text or "").strip())
    if len(text) <= max_len:
        return _sanitize_tail(text)
    cut = text[: max_len - len(end)]
    if " " in cut:
        cut = cut.rsplit(" ", 1)[0]
    cut = cut.rstrip(".,;:")
    cut = _sanitize_tail(cut)
    return cut + end


def _sanitize_tail(text: str) -> str:
    """Remove dangling connectors left by truncation (e.g. 'Funknetzplanung &')."""
    text = text.strip()
    text = re.sub(r"[\s&,+/\-–—]+$", "", text)
    text = re.sub(r"\s+(und|oder)$", "", text, flags=re.IGNORECASE)
    return text.strip()


def _trim_list(items: list[str], max_count: int, max_item: int) -> list[str]:
    out: list[str] = []
    for item in items:
        if len(out) >= max_count:
            break
        t = _trunc(item, max_item)
        if t:
            out.append(t)
    return out


_CAREER_JOB_RE = re.compile(
    r"\b(bei|Engineer|Manager|Lead|Consultant|seit|heute|Project|NPO|Rollout|Swap)\b",
    re.IGNORECASE,
)


def _looks_like_degree(text: str) -> bool:
    return bool(_DEGREE_RE.search(text))


def _looks_like_career(text: str) -> bool:
    return bool(_CAREER_HINTS.search(text))


def _looks_like_job_entry(text: str) -> bool:
    return bool(_CAREER_JOB_RE.search(text))


def _looks_like_abschluss(text: str) -> bool:
    t = text.strip()
    if re.match(r"^(19|20)\d{2}\b", t):
        return True
    return _looks_like_degree(t) and not _looks_like_job_entry(t)


def _derive_ausbildung_from_relevante(data: BeraterprofilData) -> list[str]:
    lines: list[str] = []
    for item in data.relevante_erfahrungen:
        line = f"{item.label}: {item.beschreibung}".strip(": ").strip()
        if line:
            lines.append(line)
        if len(lines) >= LIMITS["ausbildung_count"]:
            break
    return lines


def _recover_ausbildung(
    ausbildung: list[str],
    abschluss: list[str],
    data: BeraterprofilData,
) -> list[str]:
    if ausbildung:
        return ausbildung

    career_from_abschluss = [
        x
        for x in abschluss
        if (_looks_like_career(x) or _looks_like_job_entry(x)) and not _looks_like_abschluss(x)
    ]
    if career_from_abschluss:
        return _trim_list(career_from_abschluss, LIMITS["ausbildung_count"], LIMITS["ausbildung_item"])

    derived = _derive_ausbildung_from_relevante(data)
    if derived:
        return _trim_list(derived, LIMITS["ausbildung_count"], LIMITS["ausbildung_item"])

    return []


def _recover_abschluss(abschluss: list[str], ausbildung: list[str]) -> list[str]:
    if abschluss:
        return abschluss

    degree_from_ausbildung = [x for x in ausbildung if _looks_like_abschluss(x)]
    if degree_from_ausbildung:
        return _trim_list(degree_from_ausbildung, LIMITS["abschluss_count"], LIMITS["abschluss_item"])

    return []


def _non_empty_strings(items: list | None) -> list[str]:
    return [str(x).strip() for x in (items or []) if str(x).strip()]


def profile_validation_issues(data: dict) -> list[str]:
    """Return missing/invalid fields that must come from the CV extraction."""
    issues: list[str] = []
    if not str(data.get("title_domain") or "").strip():
        issues.append("title_domain")
    if not str(data.get("position") or "").strip():
        issues.append("position")
    if not str(data.get("schwerpunkte") or "").strip():
        issues.append("schwerpunkte")
    if not str(data.get("summary") or "").strip():
        issues.append("summary")
    if len(_non_empty_strings(data.get("kompetenzen"))) < 3:
        issues.append("kompetenzen (mindestens 3 aus dem CV)")

    relevante = data.get("relevante_erfahrungen") or []
    valid_relevante = 0
    for item in relevante:
        if not isinstance(item, dict):
            continue
        if str(item.get("label") or "").strip() and str(item.get("beschreibung") or "").strip():
            valid_relevante += 1
    if valid_relevante < 2:
        issues.append("relevante_erfahrungen (mindestens 2 aus dem CV)")

    ausbildung = _non_empty_strings(data.get("ausbildung_karriere"))
    abschluss = _non_empty_strings(data.get("abschluss_zertifikate"))
    if not ausbildung:
        career_from_abschluss = [
            x
            for x in abschluss
            if (_looks_like_career(x) or _looks_like_job_entry(x)) and not _looks_like_abschluss(x)
        ]
        ausbildung = career_from_abschluss
    if not ausbildung:
        for item in relevante[:2]:
            if isinstance(item, dict):
                label = str(item.get("label") or "").strip()
                desc = str(item.get("beschreibung") or "").strip()
                if label and desc:
                    ausbildung.append(f"{label}: {desc}")
    if not ausbildung:
        issues.append("ausbildung_karriere (aus dem CV)")

    if not abschluss:
        issues.append("abschluss_zertifikate (aus dem CV)")

    return issues


def sanitize_profile_dict(data: dict) -> dict:
    """Structural cleanup only — never inject generic placeholder content."""
    tools = data.get("tool_kenntnisse")
    if not isinstance(tools, dict):
        data["tool_kenntnisse"] = {}

    data["kompetenzen"] = _non_empty_strings(data.get("kompetenzen"))[: LIMITS["kompetenzen_count"]]
    data["ausbildung_karriere"] = _non_empty_strings(data.get("ausbildung_karriere"))[
        : LIMITS["ausbildung_count"]
    ]
    data["abschluss_zertifikate"] = _non_empty_strings(data.get("abschluss_zertifikate"))[
        : LIMITS["abschluss_count"]
    ]

    relevante = []
    for item in data.get("relevante_erfahrungen") or []:
        if not isinstance(item, dict):
            continue
        label = str(item.get("label") or "").strip()
        desc = str(item.get("beschreibung") or "").strip()
        if label and desc:
            relevante.append({"label": label, "beschreibung": desc})
    data["relevante_erfahrungen"] = relevante[: LIMITS["relevante_count"]]

    if not data["ausbildung_karriere"]:
        career_from_abschluss = [
            x
            for x in data["abschluss_zertifikate"]
            if (_looks_like_career(x) or _looks_like_job_entry(x)) and not _looks_like_abschluss(x)
        ]
        if career_from_abschluss:
            data["ausbildung_karriere"] = career_from_abschluss[: LIMITS["ausbildung_count"]]
            data["abschluss_zertifikate"] = [
                x for x in data["abschluss_zertifikate"] if x not in career_from_abschluss
            ]

    if not data["ausbildung_karriere"]:
        derived: list[str] = []
        for item in data["relevante_erfahrungen"][:2]:
            line = f"{item['label']}: {item['beschreibung']}".strip(": ").strip()
            if line:
                derived.append(line)
        data["ausbildung_karriere"] = derived[: LIMITS["ausbildung_count"]]

    return data


# Backwards-compatible alias used by imports
fill_required_profile_dict = sanitize_profile_dict


def _separate_sections(data: BeraterprofilData) -> BeraterprofilData:
    """
    Ausbildung/Karriere = career highlights (NOT degrees).
    Abschluss/Zertifikate = degrees, certs, training.
    """
    ausbildung: list[str] = []
    abschluss: list[str] = []

    for item in data.ausbildung_karriere:
        if _looks_like_abschluss(item) and not _looks_like_career(item):
            abschluss.append(item)
        else:
            ausbildung.append(item)

    for item in data.abschluss_zertifikate:
        if _looks_like_abschluss(item) and not _looks_like_job_entry(item):
            abschluss.append(item)
        elif _looks_like_career(item) or _looks_like_job_entry(item):
            ausbildung.append(item)
        elif _looks_like_degree(item):
            abschluss.append(item)

    ausbildung = [x for x in ausbildung if not (_looks_like_abschluss(x) and not _looks_like_career(x))]

    # Deduplicate abschluss while preserving order
    seen: set[str] = set()
    deduped_abschluss: list[str] = []
    for entry in abschluss:
        key = entry.strip().lower()
        if key not in seen:
            seen.add(key)
            deduped_abschluss.append(entry)

    return data.model_copy(
        update={"ausbildung_karriere": ausbildung, "abschluss_zertifikate": deduped_abschluss}
    )


def fit_profile(data: BeraterprofilData, *, preserve_sections: bool = False) -> BeraterprofilData:
    if not preserve_sections:
        data = _separate_sections(data)

    kompetenzen = _trim_list(
        data.kompetenzen, LIMITS["kompetenzen_count"], LIMITS["kompetenzen_item"]
    )

    relevante: list[RelevantExperience] = []
    for item in data.relevante_erfahrungen[: LIMITS["relevante_count"]]:
        label = _trunc(item.label, LIMITS["relevante_label"])
        desc = _trunc(item.beschreibung, LIMITS["relevante_desc"])
        if label and desc:
            relevante.append(RelevantExperience(label=label, beschreibung=desc))

    ausbildung = _trim_list(
        data.ausbildung_karriere, LIMITS["ausbildung_count"], LIMITS["ausbildung_item"]
    )
    abschluss = _trim_list(
        data.abschluss_zertifikate, LIMITS["abschluss_count"], LIMITS["abschluss_item"]
    )
    if not abschluss and data.abschluss_zertifikate:
        abschluss = _trim_list(
            [x for x in data.abschluss_zertifikate if x.strip()],
            LIMITS["abschluss_count"],
            LIMITS["abschluss_item"],
        )

    tools = data.tool_kenntnisse
    fitted_tools = ToolKenntnisse(
        oss_command_management=_trunc(tools.oss_command_management, LIMITS["tool_category"]),
        statistik_analyse=_trunc(tools.statistik_analyse, LIMITS["tool_category"]),
        planung_optimierung=_trunc(tools.planung_optimierung, LIMITS["tool_category"]),
        drive_test_post_processing=_trunc(
            tools.drive_test_post_processing, LIMITS["tool_category"]
        ),
        mapping=_trunc(tools.mapping, LIMITS["tool_category"]),
    )

    schwerpunkte_parts = [p.strip() for p in data.schwerpunkte.split(",") if p.strip()][:3]
    schwerpunkte = _trunc(", ".join(schwerpunkte_parts), LIMITS["schwerpunkte"])

    ausbildung = _recover_ausbildung(ausbildung, abschluss, data)
    abschluss = _recover_abschluss(abschluss, ausbildung)

    issues = profile_validation_issues(
        {
            "title_domain": data.title_domain,
            "position": data.position,
            "schwerpunkte": schwerpunkte,
            "summary": data.summary,
            "kompetenzen": kompetenzen,
            "relevante_erfahrungen": [
                {"label": item.label, "beschreibung": item.beschreibung} for item in relevante
            ],
            "ausbildung_karriere": ausbildung,
            "abschluss_zertifikate": abschluss,
        }
    )
    if issues:
        raise ValueError(
            "Profil unvollständig — folgende Inhalte fehlen im CV-Extract: "
            + ", ".join(issues)
        )

    return BeraterprofilData(
        title_domain=_trunc(data.title_domain, LIMITS["title_domain"]),
        position=_trunc(data.position, LIMITS["position"]),
        schwerpunkte=schwerpunkte,
        summary=_trunc(data.summary, LIMITS["summary"], end="."),
        kompetenzen=kompetenzen[: LIMITS["kompetenzen_count"]],
        relevante_erfahrungen=relevante[: LIMITS["relevante_count"]],
        ausbildung_karriere=ausbildung,
        abschluss_zertifikate=abschluss,
        tool_kenntnisse=fitted_tools,
    )
