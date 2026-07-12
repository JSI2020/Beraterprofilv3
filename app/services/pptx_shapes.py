"""Locate ORBIT template shapes — anchors from beraterprofil_reference_example (example2)."""

from __future__ import annotations

from dataclasses import dataclass

# User-corrected layout: Textfeld boxes (not old Inhaltsplatzhalter positions)
TEMPLATE_ANCHORS: dict[str, tuple[int, int]] = {
    "title": (503148, 27489),
    "position": (3727239, 1034736),
    "schwerpunkte": (3727239, 1330749),
    "summary": (3727239, 1590943),
    "kompetenzen": (244765, 3020190),
    "relevante_erfahrungen": (3882189, 2956946),
    "ausbildung_karriere": (7766652, 2964793),
    "tool_kenntnisse": (244765, 4869126),
    "abschluss_zertifikate": (7766651, 4718786),
    "tools_dup": (438105, 4788720),
    "photo": (503148, 874880),
}

_TOLERANCE = 300000


@dataclass(frozen=True)
class ShapeRect:
    left: int
    top: int
    width: int
    height: int


def find_shape_at(slide, left: int, top: int, tolerance: int = _TOLERANCE):
    best = None
    best_dist = float("inf")
    for shape in slide.shapes:
        if not shape.has_text_frame:
            continue
        dist = abs(shape.left - left) + abs(shape.top - top)
        if dist < best_dist and dist <= tolerance:
            best_dist = dist
            best = shape
    if best is None:
        raise KeyError(f"No text shape near ({left}, {top})")
    return best


def find_all_content_shapes(slide) -> dict:
    shapes: dict = {}
    for key, (left, top) in TEMPLATE_ANCHORS.items():
        if key == "photo":
            for shape in slide.shapes:
                if abs(shape.left - left) + abs(shape.top - top) <= _TOLERANCE:
                    shapes[key] = shape
                    break
            else:
                raise KeyError("Photo shape not found")
        else:
            shapes[key] = find_shape_at(slide, left, top)
    return shapes


def clear_shape_text(shape) -> None:
    if not shape.has_text_frame:
        return
    for paragraph in shape.text_frame.paragraphs:
        paragraph.text = ""
