"""data → LaTeX via Jinja2."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from cv.markdown import md_to_tex, tex_escape
from cv.models import CV, Company, Personal, Position

TEMPLATES_DIR = Path(__file__).resolve().parent.parent.parent / "templates"

_MONTHS = (
    "Jan",
    "Fev",
    "Mar",
    "Abr",
    "Mai",
    "Jun",
    "Jul",
    "Ago",
    "Set",
    "Out",
    "Nov",
    "Dez",
)


def fmt_month_year(d: date) -> str:
    return f"{_MONTHS[d.month - 1]} {d.year}"


def fmt_daterange(start: date, end: date | None) -> str:
    end_str = fmt_month_year(end) if end else "Presente"
    return f"{fmt_month_year(start)} -- {end_str}"


def fmt_year_range(start: date | None, end: date | None) -> str:
    """For education: just the years."""
    s = str(start.year) if start else ""
    e = str(end.year) if end else "Presente"
    if s and e:
        return f"{s} -- {e}"
    return s or e


def fmt_position_locale(pos: Position) -> str:
    bits: list[str] = []
    if pos.location:
        bits.append(pos.location)
    if pos.remote:
        bits.append("Remoto")
    return " · ".join(bits)


def sort_companies(cs: tuple[Company, ...]) -> list[Company]:
    """Newest end-date first; tie-break on latest start. Hidden companies are dropped."""
    return sorted(
        (c for c in cs if not c.hidden),
        key=lambda c: (c.latest_end, c.earliest_start),
        reverse=True,
    )


def contact_strip(p: Personal) -> str:
    """Render the contact line as escaped LaTeX with hyperlinks."""
    parts: list[str] = [tex_escape(p.location)]
    if p.phone:
        parts.append(tex_escape(p.phone))
    parts.append(rf"\href{{mailto:{p.email}}}{{{tex_escape(p.email)}}}")
    parts.append(rf"\href{{{p.github}}}{{{tex_escape(_strip_proto(str(p.github)))}}}")
    parts.append(rf"\href{{{p.linkedin}}}{{{tex_escape(_strip_proto(str(p.linkedin)))}}}")
    if p.portfolio:
        parts.append(rf"\href{{{p.portfolio}}}{{{tex_escape(_strip_proto(str(p.portfolio)))}}}")
    return r" \quad\textperiodcentered\quad ".join(parts)


def _strip_proto(url: str) -> str:
    for prefix in ("https://", "http://"):
        if url.startswith(prefix):
            url = url[len(prefix) :]
            break
    if url.startswith("www."):
        url = url[4:]
    return url.rstrip("/")


def _build_env() -> Environment:
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        block_start_string="((*",
        block_end_string="*))",
        variable_start_string="(((",
        variable_end_string=")))",
        comment_start_string="((#",
        comment_end_string="#))",
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
        autoescape=False,
        undefined=StrictUndefined,
    )
    env.filters["esc"] = tex_escape
    env.filters["md"] = md_to_tex
    env.filters["daterange"] = lambda p: fmt_daterange(p.start, p.end)
    env.filters["year_range"] = lambda e: fmt_year_range(e.start, e.end)
    env.filters["locale"] = fmt_position_locale
    env.filters["sort_companies"] = sort_companies
    env.filters["contact_strip"] = contact_strip
    env.filters["strip_proto"] = _strip_proto
    return env


def render_tex(cv: CV) -> str:
    env = _build_env()
    template = env.get_template("cv.tex.j2")
    return template.render(cv=cv)
