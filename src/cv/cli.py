"""`cv` CLI."""

from __future__ import annotations

import subprocess
import sys
import time
from datetime import date
from itertools import pairwise
from pathlib import Path

import click

from cv.build import PROJECT_ROOT, compile_pdf, write_tex
from cv.models import CV


def _load_cv_with_metrics(force_refresh: bool = False) -> CV:
    # Imported lazily so `cv refresh-metrics` doesn't pay the data-load cost twice.
    from cv.data import build_cv
    from cv.enrich import enrich_projects

    cv = build_cv()
    enriched = enrich_projects(cv.open_source, force_refresh=force_refresh)
    return cv.model_copy(update={"open_source": enriched})


@click.group()
def main() -> None:
    """Render Cadu's CV from Pydantic life data."""


@main.command()
@click.option("--watch", "-w", is_flag=True, help="Rebuild on every save (Ctrl+C to stop).")
def build(watch: bool) -> None:
    """Render the CV PDF (uses cached OSS metrics if fresh)."""
    if not watch:
        cv = _load_cv_with_metrics(force_refresh=False)
        pdf = compile_pdf(cv)
        click.echo(f"wrote {pdf}")
        return
    _watch_loop()


def _watch_loop() -> None:
    """Re-run `cv build` in a subprocess on every relevant file change."""
    from watchfiles import watch as fs_watch

    watch_dirs = [
        PROJECT_ROOT / "templates",
        PROJECT_ROOT / "src" / "cv",  # covers both code and src/cv/data/
    ]
    relevant_suffixes = {".py", ".j2"}

    def _build_once(reason: str) -> None:
        from datetime import datetime

        ts = datetime.now().strftime("%H:%M:%S")
        t0 = time.monotonic()
        click.secho(f"[{ts}] → {reason}", fg="cyan")
        proc = subprocess.run(
            [sys.executable, "-m", "cv.cli", "build"],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
        )
        elapsed = time.monotonic() - t0
        done_ts = datetime.now().strftime("%H:%M:%S")
        if proc.returncode == 0:
            msg = (proc.stdout.strip() or "wrote render/cv.pdf") + f"  ({elapsed:.1f}s)"
            click.secho(f"[{done_ts}] {msg}", fg="green")
        else:
            click.secho(f"[{done_ts}] " + (proc.stderr or proc.stdout).rstrip(), fg="red")

    _build_once("initial build")
    click.secho(f"watching {', '.join(p.name for p in watch_dirs)} (Ctrl+C to stop)", fg="yellow")

    try:
        for changes in fs_watch(*[str(p) for p in watch_dirs], debounce=300, step=50):
            files = sorted({Path(p).name for _, p in changes if Path(p).suffix in relevant_suffixes})
            if not files:
                continue
            _build_once(", ".join(files))
    except KeyboardInterrupt:
        click.secho("\nstopped", fg="yellow")


@main.command()
def tex() -> None:
    """Emit the generated LaTeX (no compile). Useful for debugging."""
    cv = _load_cv_with_metrics(force_refresh=False)
    path = write_tex(cv)
    click.echo(f"wrote {path}")


@main.command(name="refresh-metrics")
def refresh_metrics() -> None:
    """Force-refresh OSS star/language/pushed metrics from GitHub."""
    from cv.data import build_cv
    from cv.enrich import refresh as _refresh

    cv = build_cv()
    repos = [p.repo for p in cv.open_source]
    if not repos:
        click.echo("no open-source projects to refresh", err=True)
        return
    _refresh(repos)
    click.echo(f"refreshed metrics for {len(repos)} repos")


@main.command()
def lint() -> None:
    """Validate the data: chronology and overlap warnings."""
    from cv.data import build_cv

    cv = build_cv()
    problems: list[str] = []
    warnings: list[str] = []
    today = date.today()

    for company in cv.companies:
        for pos in company.positions:
            if pos.start > today:
                warnings.append(f"{company.label} / {pos.title}: start {pos.start} is in the future")
            if pos.end and pos.end > today:
                warnings.append(f"{company.label} / {pos.title}: end {pos.end} is in the future")
        # Chronology of promotions inside a single company.
        sorted_pos = sorted(company.positions, key=lambda p: p.start)
        for prev, curr in pairwise(sorted_pos):
            if prev.end and curr.start < prev.end:
                warnings.append(
                    f"{company.label}: {curr.title!r} starts {curr.start} before {prev.title!r} ended {prev.end}"
                )

    for w in warnings:
        click.echo(f"warning: {w}", err=True)
    for p in problems:
        click.echo(f"error: {p}", err=True)
    if problems:
        sys.exit(1)
    click.echo(f"ok ({len(cv.companies)} companies, {len(cv.open_source)} OSS projects)")


if __name__ == "__main__":
    main()
