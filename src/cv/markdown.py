"""Tiny markdown subset → LaTeX.

Supports paragraphs, `- bullets`, `**bold**`, `*italic*`, `[text](url)`.
No nesting, no headings, no tables. Hand-rolled to keep output predictable.
"""

from __future__ import annotations

import re

# Order matters: backslash first, otherwise we'd escape the backslashes we add.
_TEX_REPLACEMENTS = (
    ("\\", r"\textbackslash{}"),
    ("&", r"\&"),
    ("%", r"\%"),
    ("$", r"\$"),
    ("#", r"\#"),
    ("_", r"\_"),
    ("{", r"\{"),
    ("}", r"\}"),
    ("~", r"\textasciitilde{}"),
    ("^", r"\textasciicircum{}"),
)

# Sentinels for inline markup so escape doesn't mangle them.
_BOLD_OPEN = "\x00BOLDOPEN\x00"
_BOLD_CLOSE = "\x00BOLDCLOSE\x00"
_ITALIC_OPEN = "\x00ITOPEN\x00"
_ITALIC_CLOSE = "\x00ITCLOSE\x00"
_CODE_OPEN = "\x00CODEOPEN\x00"
_CODE_CLOSE = "\x00CODECLOSE\x00"
_LINK_OPEN = "\x00LINKOPEN\x00"
_LINK_MID = "\x00LINKMID\x00"
_LINK_CLOSE = "\x00LINKCLOSE\x00"


def tex_escape(text: str) -> str:
    """Escape LaTeX special characters in plain text. Use on inline content only."""
    out = text
    for a, b in _TEX_REPLACEMENTS:
        out = out.replace(a, b)
    return out


def _replace_inline(text: str) -> str:
    """Replace **bold**, *italic*, [text](url) with sentinels, escape, then materialize."""

    # [text](url) handled first so the inner text gets escaped too.
    def link_sub(m: re.Match[str]) -> str:
        return f"{_LINK_OPEN}{m.group(2)}{_LINK_MID}{m.group(1)}{_LINK_CLOSE}"

    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link_sub, text)
    # `code` first so the inner text doesn't get touched by italic/bold.
    text = re.sub(r"`([^`]+)`", lambda m: f"{_CODE_OPEN}{m.group(1)}{_CODE_CLOSE}", text)
    # Bold (lazy) before italic, so nested *italic* inside **bold** still renders.
    text = re.sub(r"\*\*(.+?)\*\*", lambda m: f"{_BOLD_OPEN}{m.group(1)}{_BOLD_CLOSE}", text)
    text = re.sub(r"\*([^*]+)\*", lambda m: f"{_ITALIC_OPEN}{m.group(1)}{_ITALIC_CLOSE}", text)
    text = tex_escape(text)
    text = (
        text.replace(_BOLD_OPEN, r"\textbf{")
        .replace(_BOLD_CLOSE, "}")
        .replace(_ITALIC_OPEN, r"\textit{")
        .replace(_ITALIC_CLOSE, "}")
        .replace(_CODE_OPEN, r"\texttt{")
        .replace(_CODE_CLOSE, "}")
        .replace(_LINK_OPEN, r"\href{")
        .replace(_LINK_MID, "}{")
        .replace(_LINK_CLOSE, "}")
    )
    # Make `/` a soft break opportunity in body text so compound phrases like
    # "infrastructure/platform-engineering" can wrap. URLs inside \href{...} are
    # left untouched.
    text = re.sub(
        r"(\\href\{[^}]*\})|/",
        lambda m: m.group(1) if m.group(1) else r"/\allowbreak{}",
        text,
    )
    return text


def md_to_tex(text: str) -> str:
    """Convert markdown subset to LaTeX. Returns LaTeX source ready to embed.

    CommonMark-flavoured wrapping: a single newline inside a paragraph or
    bullet collapses to a space, so source lines can be hard-wrapped freely.
    Blank lines separate blocks. Bullet continuations are any non-blank line
    after a `- ` line that doesn't itself start a new bullet. Fenced code
    blocks (```...```) render as a verbatim environment.
    """
    if not text or not text.strip():
        return ""

    text = text.replace("\r\n", "\n")

    # Pre-pass: extract fenced code blocks before paragraph processing,
    # so their content survives untouched (no escape, no inline parsing).
    code_blocks: list[str] = []

    def _extract_fence(m: re.Match[str]) -> str:
        code_blocks.append(m.group(1))
        return f"\x00CODEBLK{len(code_blocks) - 1}\x00"

    text = re.sub(
        r"^[ \t]*```[^\n]*\n(.*?)\n[ \t]*```[ \t]*$",
        _extract_fence,
        text,
        flags=re.DOTALL | re.MULTILINE,
    )

    lines = text.split("\n")
    out: list[str] = []
    para: list[str] = []
    bullets: list[list[str]] = []  # one inner list per bullet, holding line fragments
    mode = "none"  # "para" | "bullets" | "none"

    def flush_para() -> None:
        nonlocal mode
        if para:
            joined = " ".join(s for s in para if s)
            if joined:
                out.append(_replace_inline(joined))
                out.append("")
            para.clear()
        if mode == "para":
            mode = "none"

    def flush_bullets() -> None:
        nonlocal mode
        if bullets:
            out.append(r"\begin{itemize}")
            for b_lines in bullets:
                joined = " ".join(s for s in b_lines if s)
                out.append(r"  \item " + _replace_inline(joined))
            out.append(r"\end{itemize}")
            out.append("")
            bullets.clear()
        if mode == "bullets":
            mode = "none"

    for raw in lines:
        stripped = raw.strip()
        if not stripped:
            flush_para()
            flush_bullets()
        elif stripped.startswith("- "):
            flush_para()
            bullets.append([stripped[2:].strip()])
            mode = "bullets"
        elif mode == "bullets":
            # Continuation line for the last bullet (any non-blank, non-`- ` line
            # while we're inside a bullet block).
            bullets[-1].append(stripped)
        else:
            para.append(stripped)
            mode = "para"

    flush_para()
    flush_bullets()

    while out and out[-1] == "":
        out.pop()
    rendered = "\n".join(out)

    # Replace code-block placeholders with verbatim environments. Each placeholder
    # was emitted as a single "paragraph" so the verbatim block lands at block level.
    for i, code in enumerate(code_blocks):
        verbatim = "\\begin{verbatim}\n" + code + "\n\\end{verbatim}"
        rendered = rendered.replace(f"\x00CODEBLK{i}\x00", verbatim)
    return rendered
