"""CLI test script for Beraterprofil generation."""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.pipeline import generate_beraterprofil


async def main(cv_path: str, provider: str = "deepseek") -> None:
    path = Path(cv_path)
    out, profile = await generate_beraterprofil(path, provider=provider)
    print(f"Generated: {out}")
    print(profile.model_dump_json(indent=2, ensure_ascii=False))


if __name__ == "__main__":
    cv = sys.argv[1] if len(sys.argv) > 1 else str(ROOT / "samples" / "farhan_cv.pdf")
    prov = sys.argv[2] if len(sys.argv) > 2 else "deepseek"
    asyncio.run(main(cv, prov))
