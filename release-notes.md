# Release Notes — v0.6.0

> Released: 2026-04-24

## Highlights

**FTreeKG v0.6.0** brings snapshot housekeeping, a cleaner install story, richer
analysis output, and formal software citation support via Zenodo/CITATION.cff.

---

## New Features

### `ftreekg snapshot prune`
A new CLI command that removes vestigial snapshots to keep the `.filetreekg/snapshots/`
directory lean. It handles three categories automatically:

- **Metric-duplicates** — interior snapshots whose metrics are unchanged from the
  previous entry (noise with no signal)
- **Broken entries** — manifest entries whose JSON file is missing from disk
- **Orphaned files** — JSON files on disk not referenced by the manifest

The oldest (baseline) and newest (latest) snapshots are always preserved.

```bash
ftreekg snapshot prune --dry-run   # preview what would be removed
ftreekg snapshot prune             # remove for real
```

### `PruneResult` re-exported
`ftree_kg.snapshots.PruneResult` is now publicly re-exported for callers that
inspect prune results programmatically.

### ASCII directory tree in `analyze()`
`FileTreeKG.analyze()` now renders a depth-limited, child-truncated ASCII directory
tree (depth ≤ 3) at the end of the Markdown report, giving an at-a-glance picture
of the indexed hierarchy.

### Software citation (`CITATION.cff`)
A `CITATION.cff` file has been added to the repo root. GitHub and Zenodo both
recognise this format, so the preferred citation metadata is always available
alongside the DOI.

---

## Improvements

### Simpler installation
`pyproject.toml` has been restructured around PEP 621 `[project.optional-dependencies]`
instead of Poetry-specific groups. All install paths now work the same way:

| Goal | Command |
|---|---|
| Core runtime only | `pip install -e "."` |
| Core + dev tools | `pip install -e ".[dev]"` |
| Core + KG integrations | `pip install -e ".[kgdeps]"` |
| Everything | `pip install -e ".[all]"` |
| Everything (Poetry) | `poetry install --all-extras` |

### Cleaner analysis terminology
`analyze()` now uses **paths** and **links** instead of "nodes" and "edges" throughout
the summary table, section headings, and bar chart — language that better matches the
filesystem domain.

### VS Code test discovery fixed
`.vscode/settings.json` now correctly points pytest at `tests/` (was `filetreekg/tests/`,
a stale path from an earlier repo rename that prevented the VS Code test runner from
discovering any tests).

---

## Bug Fixes

- `_ascii_tree()` type annotations tightened: bare `dict` → `dict[str, dict[str, Any]]`
  (resolved mypy `type-arg` errors)
- `_bar` local variable renamed to `size_bar` to satisfy pylint `disallowed-name`

---

## Installation

```bash
pip install -e ".[all]"
# or
poetry install --all-extras
```

Requires Python 3.12 or 3.13.

---

_Full changelog: [CHANGELOG.md](CHANGELOG.md)_
