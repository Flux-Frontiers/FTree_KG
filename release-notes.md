# Release Notes — v0.8.0

> Released: 2026-04-29

## Highlights

**v0.8.0** adds a live status dashboard, cleans up how dotdirs are handled, and fixes the MCP server configuration.

### `ftreekg status`

A new `status` command gives you an instant snapshot of the indexed graph — node and edge counts by kind, total indexed size, whether the LanceDB vector index is present, and a bar chart of size by top-level directory, all rendered with Rich. Useful for a quick health check before querying or before a rebuild.

### Smarter dotdir exclusion

Previously, directories like `.git`, `.venv`, `.codekg`, and `.pytest_cache` had to be listed individually in `DEFAULT_SKIP_DIRS` to be excluded. Now the extractor automatically skips any directory whose name starts with `.` — unless you explicitly opt it back in via `include_dirs`. This produces much cleaner index counts (the repo itself indexes at 51 nodes instead of 1,400+) and means you never have to maintain that list again.

### MCP configuration fixed

The `.mcp.json` and the `/setup-mcp` command were still wired to the old `codekg-mcp` binary (which doesn't exist in this venv) and pointed at the wrong-case repo path. Both are now corrected to use `pycodekg mcp` and `dockg-mcp` via `poetry run`.

---

_Full changelog: [CHANGELOG.md](CHANGELOG.md)_
