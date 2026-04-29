"""render → tectonic → PDF."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from cv.models import CV
from cv.render import render_tex

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
RENDER_DIR = PROJECT_ROOT / "render"


class TectonicMissingError(RuntimeError):
    pass


def _ensure_tectonic() -> str:
    path = shutil.which("tectonic")
    if not path:
        raise TectonicMissingError("tectonic not found on PATH. Install with: brew install tectonic")
    return path


def write_tex(cv: CV) -> Path:
    RENDER_DIR.mkdir(parents=True, exist_ok=True)
    tex = render_tex(cv)
    tex_path = RENDER_DIR / "cv.tex"
    tex_path.write_text(tex, encoding="utf-8")
    return tex_path


def compile_pdf(cv: CV) -> Path:
    tectonic = _ensure_tectonic()
    tex_path = write_tex(cv)
    proc = subprocess.run(
        [tectonic, "--keep-logs", "--outdir", str(RENDER_DIR), str(tex_path)],
        capture_output=True,
        text=True,
        cwd=str(PROJECT_ROOT),
    )
    if proc.returncode != 0:
        log = (
            (RENDER_DIR / "cv.log").read_text(encoding="utf-8", errors="replace")
            if (RENDER_DIR / "cv.log").exists()
            else ""
        )
        raise RuntimeError(
            "tectonic failed:\n" + proc.stderr + "\n" + proc.stdout + "\n--- cv.log tail ---\n" + log[-2000:]
        )
    pdf_path = RENDER_DIR / "cv.pdf"
    if not pdf_path.exists():
        raise RuntimeError(f"tectonic returned 0 but {pdf_path} not present")
    return pdf_path
