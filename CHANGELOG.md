# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `src/ftree_kg/` — proper Python package namespace replacing the flat `src/` layout; Poetry now builds and installs the `ftree_kg` distribution correctly
- `[[tool.mypy.overrides]]` for `ftree_kg.*` so mypy gracefully handles self-referential imports in isolated environments
- `poetry.toml` — in-project virtualenv configuration (`in-project = true`)

### Changed
- Renamed package root from `src/` (flat, uninstallable) to `src/ftree_kg/` and updated `pyproject.toml` `packages` declaration to `{include = "ftree_kg", from = "src"}`
- All internal imports rewritten from `src.*` → `ftree_kg.*` across every module, CLI command, and test file
- CLI entry points updated from `src.cli.*` → `ftree_kg.cli.*`
- Removed `kg-rag` as a required dependency; `code-kg` and `doc-kg` remain as direct git-sourced dependencies
- Removed `[tool.poetry.extras]` stanza (extras replaced by direct dependencies)
- Bumped version to 0.3.0

### Fixed
- Package was previously uninstallable via `pip install` / `poetry install` because `packages = [{include = "src"}]` included the entire `src/` directory rather than a named importable package

### Added
- Initial FileTreeKG scaffold with KGModule infrastructure
- FileTreeKGExtractor for filesystem traversal
- FileTreeKG module with build, query, pack, analyze operations
- FileTreeKGAdapter for KGRAG federation (meta kind)
- Comprehensive test suite for extractor and query operations
- Full CLI (`ftreekg`) with `build`, `query`, `pack`, `analyze`, and `snapshot` subcommands
- `src/snapshots.py` — `SnapshotManager` with `capture`, `save_snapshot`, `load_snapshot` (including `"latest"` key), `list_snapshots`, and `diff_snapshots`; filesystem-specific metrics (`total_files`, `total_dirs`, `dir_node_counts` per top-level directory); delta tracking vs. previous and baseline snapshots; degenerate-snapshot guard; git tree hash / branch auto-detection
- `src/config.py` — reads `[tool.filetreekg]` from `pyproject.toml` for `include`/`exclude` dir lists; ships `DEFAULT_SKIP_DIRS` applied at every walk depth
- `.claude/` tooling: agents, commands, plugins, and skills for Claude Code integration
- `examples/query_examples.py` — runnable usage examples
- `analysis/filetreekg_analysis.md` — architectural analysis report
- `.pre-commit-config.yaml` and `.secrets.baseline` for pre-commit quality gates
- `src/cli/cmd_hooks.py` — new `ftreekg install-hooks` CLI command that writes a pre-commit hook into `.git/hooks/`; the hook rebuilds the FTreeKG index, captures a metrics snapshot, stages `.filetreekg/snapshots/`, then delegates to the pre-commit framework
- `FTreeKG.code-workspace` — VSCode workspace file for the project
- `codekg_pyproject.toml` — reference pyproject.toml snippet showing CodeKG integration setup
- `poetry.toml` — Poetry local virtualenv configuration (`in-project = true`)
- `analysis/FTreeKG_analysis_20260321.md` — CodeKG architectural analysis report (2026-03-21, 936 nodes, grade D/55)

### Fixed
- Removed stale `# type: ignore[import-untyped]` comments from `src/adapter.py`, `src/extractor.py`, `src/module.py`, and `src/tests/test_extractor.py` — optional deps are now installed during type-checking so suppression is no longer needed
- CI type-check job now installs all extras (`--all-extras`) so mypy can resolve `code_kg` and `kg_rag` imports instead of treating them as `Any`
- Added `[[tool.mypy.overrides]]` fallback for `code_kg.*` / `kg_rag.*` to gracefully handle environments where optional deps are absent
- Resolved cyclic import between `src/cli/main.py` and all `cmd_*.py` modules by extracting the `cli` Click group into `src/cli/group.py`; command modules now import from `group` and `main.py` re-exports `cli` after registering all subcommands
- Restored `kg-rag` as a required git dependency (was accidentally dropped when extras were removed, breaking `kg_rag` and `src/snapshots.py` at runtime)
- Guarded `from kg_rag.snapshots import ...` in `src/snapshots.py` with `try/except ImportError` so the module loads cleanly when `kg_rag` is absent; snapshot tests skip via `pytest.importorskip("kg_rag.snapshots")` rather than error

### Changed
- `ftreekg snapshot` promoted from stub to a proper subcommand group (`save`, `list`, `show`, `diff`) backed by `SnapshotManager`; pre-commit hook now captures and stages `.filetreekg/snapshots/` alongside `.codekg/snapshots/`
- `test_snapshot_round_trip` replaced with three real snapshot tests: round-trip load, list, and diff
- Restructured source tree: `filetreekg/` → `src/` and renamed package from `filetreekg` to `ftree-kg`
- `code-kg`, `doc-kg`, and `kg-rag` are required git-sourced dependencies (not extras)
- Tests relocated from `filetreekg/tests/` to `src/tests/`
- Added `[tool.filetreekg]` config section and pylint settings to `pyproject.toml`
- Updated `poetry.lock` to Poetry 2.3.2 format with revised optional-marker semantics
- `src/snapshots.py` refactored as a thin layer over `kg_rag.snapshots`; `FtreeSnapshotManager` subclass re-exports `Snapshot` and `SnapshotManifest` from the shared base and adds filesystem-specific `SnapshotMetrics`/`SnapshotDelta` hydration and `files_delta`/`dirs_delta` in deltas
- `src/cli/main.py` now registers all subcommand modules (`cmd_analyze`, `cmd_build`, `cmd_hooks`, `cmd_query`, `cmd_snapshot`) via explicit imports so CLI entry points resolve correctly at install time
- `doc-kg` optional dependency commented out; `code-kg` bumped to 0.9.1 and `poetry.lock` markers updated to remove `doc-kg` from all package constraint sets

## [0.1.0] - 2026-03-15

### Added
- Initial release of FileTreeKG
