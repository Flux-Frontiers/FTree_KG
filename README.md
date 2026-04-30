[![Python](https://img.shields.io/badge/python-3.12%20%7C%203.13-blue.svg)](https://www.python.org/)
[![License: Elastic-2.0](https://img.shields.io/badge/License-Elastic%202.0-blue.svg)](https://www.elastic.co/licensing/elastic-license)
[![Version](https://img.shields.io/badge/version-0.8.0-blue.svg)](https://github.com/Flux-Frontiers/FTreeKG/releases)
[![CI](https://github.com/Flux-Frontiers/FTreeKG/actions/workflows/ci.yml/badge.svg)](https://github.com/Flux-Frontiers/FTreeKG/actions/workflows/ci.yml)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![DOI](https://zenodo.org/badge/1182124358.svg)](https://zenodo.org/badge/latestdoi/1182124358)

**FTreeKG** — A Knowledge Graph for Filesystem Hierarchies

*Author: Eric G. Suchanek, PhD*
*Flux-Frontiers, Liberty TWP, OH*

---

## Overview

FTreeKG builds a **searchable, queryable knowledge graph** of any filesystem tree. It walks a directory, extracts every file, folder, and symlink as a typed node with metadata (size, path, kind), connects them with structural edges, and stores everything in SQLite with a vector index layered on top via LanceDB.

The result is a filesystem you can **ask questions of** — find config files by description, analyze size distribution across a project, or feed the whole structure to an AI agent as grounded context. FTreeKG is a [KGModule](https://github.com/Flux-Frontiers/kg_utils) and integrates with the [KGRAG](https://github.com/Flux-Frontiers/kgrag) federated retrieval system alongside [CodeKG](https://github.com/Flux-Frontiers/code_kg) and [DocKG](https://github.com/Flux-Frontiers/doc_kg).

---

## Features

- **Semantic search** — find files and directories by natural-language description
- **Structural graph** — every node typed (`file`, `directory`, `symlink`) with `CONTAINS` edges preserving the hierarchy
- **File metadata** — `size_bytes`, kind, and full relative path stored per node
- **Rich analysis** — summary table, ASCII size bar chart, directory tree (depth ≤ 3), full path/link breakdown
- **Live status** — `ftreekg status` gives an instant dashboard of the indexed graph
- **Temporal snapshots** — save and diff graph metrics as the filesystem evolves
- **Dotdir exclusion** — `.git`, `.venv`, `.codekg`, and all dotdirs are skipped automatically
- **Configurable scope** — `[tool.filetreekg]` in `pyproject.toml` to include/exclude directories
- **KGRAG integration** — federates with CodeKG and DocKG as a `kind="meta"` adapter

---

## Quick Start

```bash
# Index a directory
ftreekg build --repo /path/to/project

# Search by description
ftreekg query "Python test files"
ftreekg query "configuration and environment files"

# Live status dashboard
ftreekg status

# Full analysis report (written to analysis/filetreekg_analysis.md)
ftreekg analyze
```

---

## Installation

**Requirements:** Python ≥ 3.12, < 3.14

```bash
# pip (core runtime)
pip install ftree-kg

# pip (with KG integrations — CodeKG, DocKG, AgentKG)
pip install 'ftree-kg[kgdeps]'

# Poetry
poetry add ftree-kg
```

---

## Usage

### Build and query

```bash
ftreekg build                        # index current directory (wipes by default)
ftreekg build --repo /path/to/dir    # index a specific directory
ftreekg build --no-wipe              # keep existing index, add new paths only

ftreekg query "large source files"   # semantic search
ftreekg pack  "configuration files"  # metadata snippets for LLM context
```

### Live status

```bash
ftreekg status
```

Shows node/edge counts, total indexed size, LanceDB presence, active include/exclude config, and a size-by-top-directory bar chart.

### Analyze

```bash
ftreekg analyze                      # full Markdown report
ftreekg analyze -o reports/my.md     # custom output path
```

Produces a report with summary table, size chart, directory tree, and path/link breakdowns.

### Snapshots

```bash
ftreekg snapshot save 0.8.0          # capture current metrics
ftreekg snapshot list                # show all saved snapshots
ftreekg snapshot diff 0.7.0 0.8.0    # compare two versions
ftreekg snapshot prune               # remove duplicate/broken entries
ftreekg snapshot prune --dry-run     # preview what would be removed
```

---

## Python API

```python
from ftree_kg import FileTreeKG

kg = FileTreeKG(repo_root="/path/to/project")
kg.build()                           # wipe=True by default

# Semantic search
result = kg.query("configuration files", k=5)
for node in result.nodes:
    print(f"{node['kind']:12} {node['qualname']}")

# Stats and analysis
stats = kg.stats()
print(f"{stats['total_nodes']} paths, {stats['total_size_bytes']} bytes")

report = kg.analyze()                # returns Markdown string
```

---

## Knowledge Graph Schema

### Node kinds

| Kind        | Description                         |
|-------------|-------------------------------------|
| `file`      | A regular file                      |
| `directory` | A directory                         |
| `symlink`   | A symbolic link                     |

### Edge types

| Type       | Description                              |
|------------|------------------------------------------|
| `CONTAINS` | Directory → its immediate children       |

### Node ID format

`<kind>:<relative_path>:<name>`

Example: `file:src/ftree_kg/module.py:module.py`

---

## Configuration

Add to your `pyproject.toml` to control which directories are indexed:

```toml
[tool.filetreekg]
include = ["src", "docs"]   # restrict to these directories (empty = all)
exclude = ["archives"]      # skip in addition to the built-in skip list
```

Dotdirs (`.git`, `.venv`, `.codekg`, etc.) are always excluded unless explicitly listed in `include`.

---

## Storage Layout

```
.filetreekg/
  graph.sqlite      # SQLite knowledge graph (nodes + edges)
  lancedb/          # LanceDB vector index
  snapshots/        # Temporal metric snapshots (JSON)
    manifest.json
    <timestamp>.json
```

---

## Citation

If you use FTreeKG in research or a project, please cite it:

[![DOI](https://zenodo.org/badge/1182124358.svg)](https://zenodo.org/badge/latestdoi/1182124358)

**APA**

> Suchanek, E. G. (2026). *FTreeKG: Knowledge Graph for Filesystem Hierarchies* (Version 0.8.0) [Software]. Flux-Frontiers. https://doi.org/10.5281/zenodo.1182124358

**BibTeX**

```bibtex
@software{suchanek_ftree_kg,
  author    = {Suchanek, Eric G.},
  title     = {{FTreeKG}: Knowledge Graph for Filesystem Hierarchies},
  version   = {0.8.0},
  year      = {2026},
  publisher = {Flux-Frontiers},
  url       = {https://github.com/Flux-Frontiers/FTreeKG},
  doi       = {10.5281/zenodo.1182124358},
}
```

---

## License

[Elastic License 2.0](LICENSE) — free for non-commercial and internal use; commercial redistribution requires a license from Flux-Frontiers.
