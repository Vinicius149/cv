# CLAUDE.md

Operating manual for this repo. Read this before editing.

## What this repo is

A Pydantic-typed Python representation of Cadu's professional life that renders to a single PDF (`render/cv.pdf`) via Jinja2, LaTeX, and `tectonic`. The data is the source of truth, the templates are the look, the CLI is the entry point. There is no second copy of this CV anywhere.

The user (Cadu) drives this from inside Claude Code. He asks for changes ("add a bullet about X", "make the font bigger", "tighten the margins"), I edit one or two files and run `uv run cv build`, he opens `render/cv.pdf`. Tight loop. Don't introduce ceremony.

## Hard rules

- **No em-dashes (U+2014, the long horizontal dash, sometimes auto-substituted from `--`). Anywhere.** Not in CV prose, not in code comments, not in commit messages, not in this file. Cadu reads them as AI slop. Use commas, colons, parentheses, or two sentences. En-dashes (U+2013) inside numeric ranges are fine.
- **Verb-led prose** in CV descriptions. "Built", "Led", "Migrated", "Owned", "Refactored", "Mentored". Not "Was responsible for", not "Worked on".
- **Impact first.** When writing a role description, lead with what shipped and what changed because of it. Implementation details follow, they don't lead.
- **Don't invent technologies.** Only list stacks the data supports. If a description claims he used X, X must actually be evidenced (in his repos, in PR history, in his LinkedIn, or by him telling me directly).
- **Don't leak internal product / project / tool names** for current or active employers (most strictly: Cogram). Generalize: describe a service by what it is, not what it's called internally. Outside readers can't decode "Fluester" or "Byzantium". Past employers' product names already in his LinkedIn export are fine to keep (he disclosed them). His own public OSS names (`cadurso`, `sqlalchemy-easy-softdelete`, etc.) are credentials, not leaks: keep.
- **Don't create remote artifacts without being asked.** No `git push`, no `gh release create`, no `gh repo create` unless the user asks for it explicitly in this turn.
- **Don't add commentary or attribution to commits** ("Generated with Claude", "Co-Authored-By: Claude"). Cadu's global rule.
- **CI gates main on `ruff check`, `ruff format --check`, and `mypy` strict.** Run all three locally before any commit you stage. Same versions in CI (pinned via `uv.lock`). Don't hand-patch what the toolchain can fix or flag; let it do its job.
- **Prefer structured fields and automated rules over hand-arrangement.** When the user asks to reorder, hide, deduplicate, retitle, or force a layout, the right first instinct is "is there a field, validator, or template rule for this?" before "let me edit prose / shuffle the tuple by hand." This codebase grew around that habit: `OpenSourceProject.order` (sort key), `Position.keywords` and `OpenSourceProject.keywords` (replace inline Stack lines), `Company.hidden` (drop without deleting), `Personal.epigraph` (closing colophon), `\needspace` in templates (smart pagination instead of `\newpage`). If you find yourself manually arranging content, that's a signal to add a field or rule instead.
- **The user edits files alongside you.** System reminders surface his in-flight changes (`Note: ... was modified ... change was intentional, ... don't revert unless asked`). Treat those edits as intentional, do not undo them, and adapt your follow-up work to fit. If his edit conflicts with what you were about to do, ask before overriding.

## Daily loop

When the user asks for a change:

1. Identify which file owns it. Most CV-content changes touch exactly one file under `src/cv/data/`. Most look changes touch `templates/preamble.tex.j2`.
2. Make the edit.
3. The watcher (`uv run cv build --watch`, usually running in a `tu` session named `cvwatch`) rebuilds automatically on save. If unsure whether it's running, the user will tell you; otherwise assume it is and do not ask him to re-run `cv build`.
4. If the change is visual, read pages of `render/cv.pdf` with the Read tool to verify it looks right. Don't claim a visual change is done without seeing the rendered PDF.
5. Tell Cadu in one sentence what you changed and where.

Don't push, tag, or release unless asked. He iterates locally; he tells you when he wants a release.

## Project layout

```
src/cv/                  the package (renderer + CLI + models + life data)
  models.py                Pydantic models: CV, Personal, Company, Position,
                           OpenSourceProject, Education, Language; the
                           MarkdownText annotation that auto-dedents triple-
                           quoted description strings
  render.py                Jinja2 environment, helper filters, render_tex(cv)
  markdown.py              MD-to-LaTeX converter (paragraphs, bullets,
                           **bold**, *italic*, `code`, [links](url),
                           ```fenced code```, slash break opportunities)
  enrich.py                gh API + JSON cache for OSS star/lang/pushed_at
  build.py                 tectonic invocation, render/cv.pdf path management
  cli.py                   `cv build / build --watch / lint / tex / refresh-metrics`
  data/                    source-of-truth life data (Pydantic instantiations)
    personal.py              name, contact, profile summary, epigraph
    experience.py            tuple of every Company (renderer sorts)
    companies/<name>.py      one Company per file
    education.py
    languages.py
    open_source.py
    _oss_metrics.json        committed cache of GitHub stars

templates/
  preamble.tex.j2          ALL typography lives here; the "make my name
                           bigger" file. Defines \cvheader, \cvposition,
                           \cvcompanyhead, \cveducation, \cvossheader,
                           \cvkeywords, \cvepigraph; loads needspace,
                           newunicodechar, geometry, etc.
  cv.tex.j2                top-level layout: section order, sort keys,
                           where \needspace and section breaks happen

render/                  build output (gitignored)
.github/workflows/
  ci.yml                   ruff + mypy --strict on push/PR to main
  release.yml              tag-triggered PDF build attached to GH release
```

## Where to make what kind of change

| Request | File |
|---|---|
| Add or edit a job description | `src/cv/data/companies/<name>.py` |
| Add or rename a company | `src/cv/data/companies/<name>.py` + add to `COMPANIES` tuple in `src/cv/data/experience.py` |
| Hide a company from the render (without deleting) | set `hidden=True` on the `Company` |
| Edit profile summary, contact info, headline, epigraph | `src/cv/data/personal.py` |
| Edit education / languages | `src/cv/data/education.py`, `src/cv/data/languages.py` |
| Add or edit an OSS project | `src/cv/data/open_source.py` |
| Reorder OSS projects | set `order=N` on the `OpenSourceProject` (lower = earlier; default 100) |
| Refresh OSS star counts | `uv run cv refresh-metrics` (writes `src/cv/data/_oss_metrics.json`) |
| Margins, fonts, colors, section heading style, line spacing, list spacing | `templates/preamble.tex.j2` |
| Layout macros (`\cvheader / \cvposition / \cvcompanyhead / \cveducation / \cvossheader / \cvkeywords / \cvepigraph`) | `templates/preamble.tex.j2` |
| Section ordering, block-level layout, `\needspace` placement | `templates/cv.tex.j2` |
| New markdown syntax (e.g. underline, smallcaps) | `src/cv/markdown.py` |
| Date format, sort order, contact-strip layout | `src/cv/render.py` (helpers) |

## Authoring data

`src/cv/data/companies/*.py` files instantiate Pydantic models directly. Triple-quoted descriptions are dedented at validation time (see `MarkdownText` in `models.py`), so author them naturally indented inside the call:

```python
from datetime import date
from cv.models import Company, Position

NEXTCORP = Company(
    name="NextCorp",
    one_liner="What they do, and where",
    url="https://nextcorp.io",
    hidden=False,                    # set True to drop without deleting
    positions=(
        Position(
            title="Staff Software Engineer",
            start=date(2027, 1, 1),
            end=None,                # None = Present
            location="Berlin, Germany",
            remote=True,
            description="""
                Lead with impact. One short framing sentence, then bullets:

                - **Built X.** Concrete artifacts, named systems, measurable outcomes.
                - **Owned Y.** ...
            """,
            keywords=("Python", "FastAPI", "K3s"),
        ),
    ),
)
```

Then add to `COMPANIES` in `src/cv/data/experience.py`. Order in that tuple does not matter; the renderer sorts companies by latest end date descending.

`Position.keywords` and `OpenSourceProject.keywords` render as a small-grey "Keywords:" line after the description. They replace inline `**Stack:**` paragraphs in prose; do not write `**Stack:**` lines in descriptions any more.

`OpenSourceProject.order` controls render order in the Open Source section (ascending; default 100). Lower numbers come first; ties keep definition order.

`Personal.epigraph` plus `Personal.epigraph_attribution` render a small italic muted closing line at the very bottom (left-aligned). Set both or leave both `None`.

## Markdown subset (used inside `description` and `summary`)

What's supported:

- Blank-line-separated paragraphs.
- Single newlines inside a paragraph or bullet collapse to a space (CommonMark wrapping). Hard-wrap source lines freely; the output flows.
- `- bullet` lines (group into an `itemize`). Bullet continuation lines (any non-blank, non-`- ` line after a `- ` line) join into the previous bullet with a space.
- `**bold**`, `*italic*`, `` `code` ``, `[text](url)`. Bold can wrap italic and code (`**Owned the *foo* layer**` works).
- Fenced code blocks: ```` ``` ```` on their own lines bracket a verbatim block. Content survives untouched (no escape, no inline parsing).
- `/` in body text becomes a soft break opportunity (`/\allowbreak{}`), so long compounds like `infrastructure/platform-engineering` wrap at the slash. URLs inside `\href{...}` are exempted.

What's not:

- Nested lists, headings inside descriptions, tables.
- HTML.
- Inline math.

If you need something the parser doesn't support, extend `src/cv/markdown.py` rather than dropping raw LaTeX into a description.

## Templates (smart pagination)

`templates/preamble.tex.j2` loads `needspace`. Every `\cvcompanyhead` is wrapped with `\needspace{7\baselineskip}`, so a company that would otherwise be orphaned at the bottom of a page (heading visible, body bumped to next page) gets pushed to the next page automatically. The Education and Languages sections in `cv.tex.j2` use the same trick (`\needspace{10}` and `\needspace{6}` respectively).

If pagination needs adjustment (companies still splitting awkwardly), tune the `\needspace{N\baselineskip}` value in the relevant macro/section. Don't add hard `\newpage`s unless explicitly asked.

## Building & watching

```bash
uv run cv build               # render/cv.pdf
uv run cv build --watch       # rebuild on every save (cadu's editing loop)
uv run cv tex                 # render/cv.tex only (debug)
uv run cv lint                # date / overlap warnings
uv run cv refresh-metrics     # GitHub stars
```

The watch loop runs `cv build` in a subprocess on every relevant save (300 ms debounce), printing a `[HH:MM:SS] → file.py` line and the elapsed build time. It usually lives in a `tu` virtual-terminal session named `cvwatch`. If you need to restart it: `tu kill --name cvwatch && tu run --name cvwatch --cwd /Users/cadu/w/cadu/cv --shell "uv run cv build --watch"`.

If `tectonic` is missing, `brew install tectonic`. Never paper over a build failure by adding `try/except` around the renderer; root-cause it.

## Lint / format / typecheck

CI gates `main` on three checks. Same toolchain locally and in CI (versions pinned via `uv.lock`):

```bash
uv sync --group dev
uv run ruff check             # lint
uv run ruff format --check    # `ruff format` to auto-fix
uv run mypy                   # --strict, configured in pyproject.toml
```

If all three pass locally, CI will pass. Don't push without running them.

Pyright is configured under `[tool.pyright]` in `pyproject.toml`; if your editor still surfaces import-resolution errors, that's an editor-config issue, not the codebase. Mypy is the source of truth.

## Visual verification

After any change to a template, any visible-by-default macro, or any non-trivial copy edit, you must look at the result, not just the build exit code. Use the Read tool on `render/cv.pdf` (it accepts a `pages` range) and confirm the change rendered as intended. A green build with the wrong output is worse than a red one.

## Style for descriptions

Looking at the existing entries (Asimov, Puzzl Software House, MEDGRUPO) for tone reference, the voice is:

- Concise, confident, technical.
- Specific about systems and stacks. Names projects when they matter.
- Mostly past-tense for finished work, present-tense for ongoing.
- Bullets when listing distinct shipped items. Paragraphs when the work was a continuous arc.
- Tech stack belongs in the structured `keywords` field, not in inline `**Stack:**` prose.

Don't soften with adverbs ("successfully", "effectively"). The verb does the work.

## Releases

**Canonical command (one shot, creates the tag remotely + the release in a single call):**

```bash
gh release create vX.Y.Z --generate-notes
```

That's it. `gh release create` pushes the tag and creates the release. The push triggers `.github/workflows/release.yml`, which builds the PDF in CI, names it `cadu-cv-<UTC-YYYYMMDD>-<HHMM>-vX.Y.Z.pdf`, and attaches it to the release. **Do NOT** run `git tag vX.Y.Z && git push origin vX.Y.Z` first; that's a two-step workaround for a one-step problem, and `gh release create` already does both.

Do not pass `render/cv.pdf` as a file argument to `gh release create` either: that would attach a second asset (named `cv.pdf`) alongside the timestamped one the workflow uploads. Let the workflow be the single source of the artifact.

Bump versions semver-style. Patch bumps are fine for content tweaks. Cadu cuts releases when he wants to send the PDF to someone, not on a schedule.

After triggering, watch the build with:
```bash
gh run watch $(gh run list --workflow=release.yml --limit=1 --json databaseId --jq '.[0].databaseId') --exit-status
```

## Things to ignore

- `render/` is gitignored. Don't `git add` PDFs.
- `*.pyc`, `__pycache__/`, `.venv/` are gitignored.
- The diff between Pyright (editor-side) and mypy (CI gate) can produce noisy import warnings on the editor side that don't actually fail CI. Trust mypy.

## When in doubt

Ask. The user prefers a quick "want me to also do X?" over a surprise change. He is the source of truth for his own life data.
