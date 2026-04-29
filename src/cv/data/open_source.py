from cv.models import OpenSourceProject

# Author-time fields only. Stars / language / pushed date come from
# `cv refresh-metrics` (cached at data/_oss_metrics.json).
#
# Definition order below is irrelevant; the renderer sorts by `order` ascending.
# Lower `order` = appears first. Default is 100 ("no preference").
# Use small numbers (10, 20, 30, ...) to promote, larger to demote.

OPEN_SOURCE_PROJECTS = (
    OpenSourceProject(
        name="sqlalchemy-easy-softdelete",
        repo="flipbit03/sqlalchemy-easy-softdelete",
        tagline="Drop-in soft-deletion for SQLAlchemy models.",
        description="""
            Mixin that adds soft-delete semantics to SQLAlchemy 1.4/2.x models without touching application code: filtered queries, cascade rules, and admin escape hatches all work transparently. Used in production across multiple Python services.
        """,
        keywords=("Python", "SQLAlchemy", "soft-delete", "ORM"),
    ),
    OpenSourceProject(
        name="cadurso",
        repo="flipbit03/cadurso",
        tagline="Authorization framework for Python applications (RBAC / ABAC).",
        description="""
            Library for declaring and evaluating authorization rules in Python. Supports both role-based and attribute-based access control with a small, type-friendly API designed to live next to your domain models.
        """,
        keywords=("Python", "RBAC", "ABAC", "authorization", "type-safe"),
    ),
    OpenSourceProject(
        name="lineark",
        repo="flipbit03/lineark",
        tagline="Unofficial Linear CLI for humans and coding agents.",
        description="""
            Rust CLI for the Linear issue tracker, designed equally for terminal use and for scripting/agent integration. Exposes a structured SDK surface that LLM-based coding agents can drive directly.
        """,
        keywords=("Rust", "CLI", "Linear API", "SDK", "agent-friendly", "agentic-tooling"),
        order=15,
    ),
    OpenSourceProject(
        name="terminal-use",
        repo="flipbit03/terminal-use",
        tagline="tu: tmux for your coding agent.",
        description="""
            Rust virtual-terminal harness that lets coding agents (Claude Code and friends) drive interactive TUIs (htop, vim, ncurses installers) via screenshot and keystroke primitives. Wraps a vt100 emulator under an alacritty-style backend.
        """,
        keywords=("Rust", "vt100", "alacritty", "agent-friendly", "agentic-tooling", "TUI automation"),
        order=10,
    ),
    OpenSourceProject(
        name="forestui",
        repo="flipbit03/forestui",
        tagline="TUI git-worktree + Claude Code session manager.",
        description="""
            Python TUI that manages parallel git worktrees and the Claude Code sessions running inside them, so multiple agent sessions can work on isolated branches without stepping on each other.
        """,
        keywords=("Python", "TUI", "git worktree", "Claude Code"),
        order=20,
    ),
)
