"""Fetch open-source repo metrics via `gh api`, with a committed JSON cache."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from datetime import UTC, date, datetime
from pathlib import Path
from typing import TypedDict, cast

from cv.models import OpenSourceProject

CACHE_PATH = Path(__file__).resolve().parent / "data" / "_oss_metrics.json"
CACHE_TTL_SECONDS = 24 * 60 * 60  # 24h


class _Metric(TypedDict):
    stars: int
    language: str | None
    last_commit: str  # ISO date


class _CacheFile(TypedDict):
    fetched_at: str  # ISO datetime
    repos: dict[str, _Metric]


def _now() -> datetime:
    return datetime.now(UTC)


def _load_cache() -> _CacheFile | None:
    if not CACHE_PATH.exists():
        return None
    try:
        return cast(_CacheFile, json.loads(CACHE_PATH.read_text(encoding="utf-8")))
    except OSError, json.JSONDecodeError:
        return None


def _cache_is_fresh(cache: _CacheFile) -> bool:
    try:
        fetched_at = datetime.fromisoformat(cache["fetched_at"])
    except KeyError, ValueError:
        return False
    age = (_now() - fetched_at).total_seconds()
    return age < CACHE_TTL_SECONDS


def _fetch_one(repo: str) -> _Metric:
    if not shutil.which("gh"):
        raise RuntimeError("gh CLI not found. Install with: brew install gh")
    proc = subprocess.run(
        [
            "gh",
            "api",
            f"repos/{repo}",
            "--jq",
            "{stars: .stargazers_count, language: .language, pushed_at: .pushed_at}",
        ],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"gh api failed for {repo}: {proc.stderr.strip()}")
    payload = json.loads(proc.stdout)
    pushed_at = payload.get("pushed_at") or ""
    last_commit = pushed_at[:10] if pushed_at else _now().date().isoformat()
    return {
        "stars": int(payload.get("stars") or 0),
        "language": payload.get("language"),
        "last_commit": last_commit,
    }


def refresh(repos: list[str]) -> _CacheFile:
    """Force-refresh the cache for `repos`. Writes the JSON file."""
    metrics: dict[str, _Metric] = {}
    for r in repos:
        metrics[r] = _fetch_one(r)
        print(
            f"  {r}: ★ {metrics[r]['stars']}  ·  {metrics[r]['language'] or 'n/a'}  ·  pushed {metrics[r]['last_commit']}",
            file=sys.stderr,
        )
    cache: _CacheFile = {"fetched_at": _now().isoformat(), "repos": metrics}
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(json.dumps(cache, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return cache


def load_or_refresh(repos: list[str], force: bool = False) -> _CacheFile:
    """Return cached metrics, refreshing only if stale or missing. Falls back to stale on failure."""
    cache = _load_cache()
    if cache and not force and _cache_is_fresh(cache):
        return cache
    if force or cache is None:
        return refresh(repos)
    # Stale: try refresh, fall back to stale on error.
    try:
        return refresh(repos)
    except Exception as exc:
        print(f"warning: refresh failed ({exc}); using stale cache", file=sys.stderr)
        return cache


def enrich_projects(
    projects: tuple[OpenSourceProject, ...],
    *,
    force_refresh: bool = False,
) -> tuple[OpenSourceProject, ...]:
    """Return the projects with stars/language/last_commit populated from cache."""
    if not projects:
        return projects
    repos = [p.repo for p in projects]
    cache = load_or_refresh(repos, force=force_refresh)
    out: list[OpenSourceProject] = []
    for p in projects:
        m = cache["repos"].get(p.repo)
        if m:
            out.append(
                p.model_copy(
                    update={
                        "stars": m["stars"],
                        "language": p.language or m["language"],
                        "last_commit": date.fromisoformat(m["last_commit"]),
                    }
                )
            )
        else:
            out.append(p)
    return tuple(out)
