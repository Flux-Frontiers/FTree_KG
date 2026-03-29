# FTreeKG Packaging Fix — Agent Brief

## Problem Summary

FTreeKG cannot be reliably installed as a path dependency from kgrag (or any other repo)
due to two structural issues in its `pyproject.toml`.

---

## Issue 1: Broken `packages` Declaration

**File:** `pyproject.toml` line 13
**Current:**
```toml
packages = [{include = "src"}]
```
**Problem:** This tells Poetry to install a top-level package named `src`. The code lives
directly inside `src/` with no `ftree_kg/` subdirectory, so the installed import path is
`import src` — which collides with any other package using the same flat layout, and is
not importable by a meaningful name.

**All CLI entry points are also broken as a result:**
```toml
ftreekg        = "src.cli:cli"
ftreekg-build  = "src.cli.cmd_build:build"
ftreekg-query  = "src.cli.cmd_query:query"
ftreekg-pack   = "src.cli.cmd_query:pack"
ftreekg-analyze = "src.cli.cmd_analyze:analyze"
ftreekg-snapshot = "src.cli.cmd_snapshot:snapshot"
```

---

## Issue 2: Circular Dependency

**File:** `pyproject.toml` line 35
**Current:**
```toml
kg-rag = { git = "https://github.com/Flux-Frontiers/KGRAG.git"}
```
**Problem:** kgrag depends on ftree-kg, and ftree-kg depends on kg-rag → circular.
Poetry/pip resolvers will either fail or silently install mismatched versions.

FTreeKG should depend on `code-kg` and `doc-kg` directly (as it already does on lines 36–37),
not on the kgrag orchestrator.

---

## Fix Plan

### Step 1 — Restructure source layout

```
# Before
src/
  __init__.py
  adapter.py
  cli/
  config.py
  extractor.py
  module.py
  snapshots.py
  tests/

# After
src/
  ftree_kg/
    __init__.py
    adapter.py
    cli/
    config.py
    extractor.py
    module.py
    snapshots.py
  tests/   ← move tests out of src
```

### Step 2 — Fix `pyproject.toml`

```toml
# packages
packages = [{include = "ftree_kg", from = "src"}]

# scripts
[tool.poetry.scripts]
ftreekg          = "ftree_kg.cli:cli"
ftreekg-build    = "ftree_kg.cli.cmd_build:build"
ftreekg-query    = "ftree_kg.cli.cmd_query:query"
ftreekg-pack     = "ftree_kg.cli.cmd_query:pack"
ftreekg-analyze  = "ftree_kg.cli.cmd_analyze:analyze"
ftreekg-snapshot = "ftree_kg.cli.cmd_snapshot:snapshot"

# dependencies — remove kg-rag, keep code-kg and doc-kg
[tool.poetry.dependencies]
python   = ">=3.12,<3.14"
click    = "^8.1.0"
code-kg  = { git = "https://github.com/Flux-Frontiers/code_kg.git" }
doc-kg   = { git = "https://github.com/Flux-Frontiers/doc_kg.git" }
```

### Step 3 — Update all internal imports

All files that currently do `from src.xxx import ...` or `import src.xxx` must be updated
to `from ftree_kg.xxx import ...` / `import ftree_kg.xxx`.

### Step 4 — Fix mypy overrides in `pyproject.toml`

```toml
[[tool.mypy.overrides]]
module = ["code_kg.*", "kg_rag.*", "ftree_kg.*"]
ignore_missing_imports = true
```

### Step 5 — Rebuild and verify

```bash
cd /Users/egs/repos/FTreeKG
poetry install
ftreekg --help   # verify CLI resolves
cd /Users/egs/repos/kgrag
poetry update ftree-kg
python -c "import ftree_kg; print(ftree_kg.__version__)"
```

---

## Convention Reference

All other packages in this ecosystem follow the same layout:

| Repo     | packages declaration                          | Import root |
|----------|-----------------------------------------------|-------------|
| code_kg  | `{include = "code_kg", from = "src"}`         | `code_kg`   |
| doc_kg   | `{include = "doc_kg", from = "src"}`          | `doc_kg`    |
| kgrag    | `{include = "kg_rag", from = "src"}`          | `kg_rag`    |
| FTreeKG  | `{include = "src"}` ← **broken, fix this**   | `src` ← bad |

---

## Context

- kgrag `pyproject.toml` currently has: `ftree-kg = {path = "../FTreeKG", develop = true}`
- This path dep is correct; the problem is entirely inside FTreeKG itself
- Fix was deferred because source files were staged at time of discovery (2026-03-25)
