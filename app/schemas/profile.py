"""Pydantic schemas for Beraterprofil structured data."""

from __future__ import annotations

from pydantic import BaseModel, Field


class RelevantExperience(BaseModel):
    label: str = Field(..., description="Short topic label (bold in PPT)")
    beschreibung: str = Field(..., description="One sentence description")


class ToolKenntnisse(BaseModel):
    oss_command_management: str = ""
    statistik_analyse: str = ""
    planung_optimierung: str = ""
    drive_test_post_processing: str = ""
    mapping: str = ""


class BeraterprofilData(BaseModel):
    title_domain: str = Field(..., examples=["Funknetzplanung"])
    position: str = Field(..., examples=["Consultant"])
    schwerpunkte: str = Field(..., examples=["Netzplanung, Optimierung, 5G/LTE"])
    summary: str
    kompetenzen: list[str] = Field(..., min_length=3, max_length=7)
    relevante_erfahrungen: list[RelevantExperience] = Field(..., min_length=2, max_length=5)
    ausbildung_karriere: list[str] = Field(..., min_length=1, max_length=4)
    abschluss_zertifikate: list[str] = Field(..., min_length=1, max_length=6)
    tool_kenntnisse: ToolKenntnisse
