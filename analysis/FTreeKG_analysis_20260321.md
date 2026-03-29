> **Analysis Report Metadata**
> - **Generated:** 2026-03-21T02:54:21Z
> - **Version:** code-kg 0.9.2
> - **Commit:** 71e3976 (main)
> - **Platform:** macOS 26.3.1 | arm64 (arm) | Turing | Python 3.12.13
> - **Graph:** 936 nodes · 1015 edges (96 meaningful)
> - **Included directories:** all
> - **Excluded directories:** none
> - **Elapsed time:** 3s

# FTreeKG Analysis

**Generated:** 2026-03-21 02:54:21 UTC

---

## Executive Summary

This report provides a comprehensive architectural analysis of the **FTreeKG** repository using CodeKG's knowledge graph. The analysis covers complexity hotspots, module coupling, key call chains, and code quality signals to guide refactoring and architecture decisions.

| Overall Quality | Grade | Score |
|----------------|-------|-------|
| [D] **Needs Work** | **D** | 55 / 100 |

---

## Baseline Metrics

| Metric | Value |
|--------|-------|
| **Total Nodes** | 936 |
| **Total Edges** | 1015 |
| **Modules** | 21 (of 21 total) |
| **Functions** | 43 |
| **Classes** | 6 |
| **Methods** | 26 |

### Edge Distribution

| Relationship Type | Count |
|-------------------|-------|
| CALLS | 335 |
| CONTAINS | 75 |
| IMPORTS | 124 |
| ATTR_ACCESS | 242 |
| INHERITS | 4 |

---

## Fan-In Ranking

Most-called functions are potential bottlenecks or core functionality. These functions are heavily depended upon across the codebase.

| # | Function | Module | Callers |
|---|----------|--------|---------|
| 1 | `FileTreeKG()` | src/module.py | **11** |
| 2 | `stats()` | examples/query_examples.py | **9** |
| 3 | `stats()` | src/adapter.py | **9** |
| 4 | `query()` | src/adapter.py | **6** |
| 5 | `build()` | src/cli/cmd_build.py | **6** |
| 6 | `query()` | src/cli/cmd_query.py | **6** |
| 7 | `pack()` | src/adapter.py | **5** |
| 8 | `pack()` | src/cli/cmd_query.py | **5** |
| 9 | `save_snapshot()` | src/cli/cmd_snapshot.py | **5** |
| 10 | `pack()` | src/module.py | **5** |
| 11 | `capture()` | src/snapshots.py | **5** |
| 12 | `save_snapshot()` | src/snapshots.py | **5** |
| 13 | `_load()` | src/adapter.py | **4** |
| 14 | `load_snapshot()` | src/snapshots.py | **4** |
| 15 | `analyze()` | examples/query_examples.py | **4** |


**Insight:** Functions with high fan-in are either core APIs or bottlenecks. Review these for:
- Thread safety and performance
- Clear documentation and contracts
- Potential for breaking changes

---

## High Fan-Out Functions (Orchestrators)

Functions that call many others may indicate complex orchestration logic or poor separation of concerns.

No extreme high fan-out functions detected. Well-balanced architecture.

---

## Module Architecture

Top modules by dependency coupling and cohesion (showing up to 10 with activity).
Cohesion = incoming / (incoming + outgoing + 1); higher = more internally focused.

| Module | Functions | Classes | Incoming | Outgoing | Cohesion |
|--------|-----------|---------|----------|----------|----------|
| `src/snapshots.py` | 5 | 3 | 0 | 0 | 0.00 |
| `src/tests/test_query.py` | 10 | 0 | 0 | 1 | 0.50 |
| `src/adapter.py` | 0 | 1 | 0 | 1 | 0.50 |
| `src/extractor.py` | 0 | 1 | 3 | 1 | 0.20 |
| `src/tests/test_extractor.py` | 8 | 0 | 0 | 1 | 0.50 |
| `src/module.py` | 0 | 1 | 8 | 2 | 0.18 |
| `src/cli/cmd_snapshot.py` | 5 | 0 | 2 | 3 | 0.50 |
| `examples/query_examples.py` | 4 | 0 | 0 | 1 | 0.50 |
| `src/config.py` | 3 | 0 | 3 | 0 | 0.00 |
| `src/cli/cmd_query.py` | 2 | 0 | 2 | 3 | 0.50 |

---

## Key Call Chains

Deepest call chains in the codebase.

**Chain 1** (depth: 2)

```
basic_queries → FileTreeKG
```

**Chain 2** (depth: 3)

```
stats → stats → build
```

**Chain 3** (depth: 4)

```
stats → stats → _load → FileTreeKG
```

**Chain 4** (depth: 4)

```
basic_queries → query → _load → FileTreeKG
```

**Chain 5** (depth: 4)

```
basic_queries → build → stats → FileTreeKG
```

---

## Public API Surface

Identified public APIs (module-level functions with high usage).

| Function | Module | Fan-In | Type |
|----------|--------|--------|------|
| `FileTreeKG()` | src/module.py | 11 | class |
| `stats()` | examples/query_examples.py | 9 | function |
| `build()` | src/cli/cmd_build.py | 6 | function |
| `query()` | src/cli/cmd_query.py | 6 | function |
| `pack()` | src/cli/cmd_query.py | 5 | function |
| `save_snapshot()` | src/cli/cmd_snapshot.py | 5 | function |
| `analyze()` | examples/query_examples.py | 4 | function |
| `FileTreeKGExtractor()` | src/extractor.py | 2 | class |
| `SnapshotDelta()` | src/snapshots.py | 1 | class |
| `SnapshotMetrics()` | src/snapshots.py | 1 | class |
---

## Docstring Coverage

Docstring coverage directly determines semantic retrieval quality. Nodes without
docstrings embed only structured identifiers (`KIND/NAME/QUALNAME/MODULE`), where
keyword search is as effective as vector embeddings. The semantic model earns its
value only when a docstring is present.

| Kind | Documented | Total | Coverage |
|------|-----------|-------|----------|
| `function` | 25 | 43 | [WARN] 58.1% |
| `method` | 21 | 26 | [OK] 80.8% |
| `class` | 6 | 6 | [OK] 100.0% |
| `module` | 20 | 21 | [OK] 95.2% |
| **total** | **72** | **96** | **[WARN] 75.0%** |

> **Recommendation:** 24 nodes lack docstrings. Prioritize documenting high-fan-in functions and public API surface first — these have the highest impact on query accuracy.

---

## Structural Importance Ranking (SIR)

Weighted PageRank aggregated by module — reveals architectural spine. Cross-module edges boosted 1.5×; private symbols penalized 0.85×. Node-level detail: `codekg centrality --top 25`

| Rank | Score | Members | Module |
|------|-------|---------|--------|
| 1 | 0.166081 | 2 | `src/cli/group.py` |
| 2 | 0.157023 | 7 | `src/module.py` |
| 3 | 0.141755 | 16 | `src/snapshots.py` |
| 4 | 0.118407 | 9 | `src/adapter.py` |
| 5 | 0.097486 | 9 | `src/extractor.py` |
| 6 | 0.051751 | 4 | `src/config.py` |
| 7 | 0.049642 | 5 | `examples/query_examples.py` |
| 8 | 0.048105 | 3 | `src/cli/cmd_query.py` |
| 9 | 0.045077 | 6 | `src/cli/cmd_snapshot.py` |
| 10 | 0.032874 | 11 | `src/tests/test_query.py` |
| 11 | 0.027079 | 9 | `src/tests/test_extractor.py` |
| 12 | 0.020250 | 2 | `src/cli/cmd_build.py` |
| 13 | 0.013211 | 2 | `src/cli/main.py` |
| 14 | 0.011455 | 2 | `src/cli/cmd_analyze.py` |
| 15 | 0.008086 | 2 | `conftest.py` |



---

## Code Quality Issues

- [WARN] Moderate docstring coverage (75.0%) — semantic retrieval quality is degraded for undocumented nodes; BM25 is as effective as embeddings without docstrings
- [WARN] 7 orphaned functions found (`extractor`, `test_snapshot_diff`, `test_node_id_format`, `test_snapshot_round_trip`, `test_extract_yields_specs`, `test_node_ids_are_stable`, `test_pack_snippets_have_content`) -- consider archiving or documenting

---

## Architectural Strengths

- Well-structured with 15 core functions identified
- No god objects or god functions detected

---

## Recommendations

### Immediate Actions
1. **Improve docstring coverage** — 24 nodes lack docstrings; prioritize high-fan-in functions and public APIs first for maximum semantic retrieval gain
2. **Remove or archive orphaned functions** — `extractor`, `test_snapshot_diff`, `test_node_id_format`, `test_snapshot_round_trip`, `test_extract_yields_specs` (and 2 more) have zero callers and add maintenance burden

### Medium-term Refactoring
1. **Harden high fan-in functions** — `FileTreeKG`, `stats`, `stats` are widely depended upon; review for thread safety, clear contracts, and stable interfaces
2. **Reduce module coupling** — consider splitting tightly coupled modules or introducing interface boundaries
3. **Add tests for key call chains** — the identified call chains represent well-traveled execution paths that benefit most from regression coverage

### Long-term Architecture
1. **Version and stabilize the public API** — document breaking-change policies for `FileTreeKG`, `stats`, `build`
2. **Enforce layer boundaries** — add linting or CI checks to prevent unexpected cross-module dependencies as the codebase grows
3. **Monitor hot paths** — instrument the high fan-in functions identified here to catch performance regressions early

---

## Inheritance Hierarchy

**4** INHERITS edges across **4** classes. Max depth: **0**.

| Class | Module | Depth | Parents | Children |
|-------|--------|-------|---------|----------|
| `FileTreeKGAdapter` | src/adapter.py | 0 | 1 | 0 |
| `FileTreeKGExtractor` | src/extractor.py | 0 | 1 | 0 |
| `FileTreeKG` | src/module.py | 0 | 1 | 0 |
| `FtreeSnapshotManager` | src/snapshots.py | 0 | 1 | 0 |


---

## Snapshot History

Recent snapshots in reverse chronological order. Δ columns show change vs. the immediately preceding snapshot.

| # | Timestamp | Branch | Version | Nodes | Edges | Coverage | Δ Nodes | Δ Edges | Δ Coverage |
|---|-----------|--------|---------|-------|-------|----------|---------|---------|------------|
| 1 | 2026-03-15 04:45:52 | main | v0.1.0 | 294 | 312 | 53.3% | — | — | — |


---

## Appendix: Orphaned Code

Functions with zero callers (potential dead code):

| Function | Module | Lines |
|----------|--------|-------|
| `test_snapshot_round_trip()` | src/tests/test_query.py | 26 |
| `test_snapshot_diff()` | src/tests/test_query.py | 15 |
| `extractor()` | src/tests/test_extractor.py | 6 |
| `test_extract_yields_specs()` | src/tests/test_extractor.py | 6 |
| `test_node_id_format()` | src/tests/test_extractor.py | 5 |
| `test_pack_snippets_have_content()` | src/tests/test_query.py | 4 |
| `test_node_ids_are_stable()` | src/tests/test_extractor.py | 3 |
---

## CodeRank -- Global Structural Importance

Weighted PageRank over CALLS + IMPORTS + INHERITS edges (test paths excluded). Scores are normalized to sum to 1.0. This ranking seeds Phase 2 fan-in discovery and Phase 15 concern queries.

| Rank | Score | Kind | Name | Module |
|------|-------|------|------|--------|
| 1 | 0.003408 | method | `FileTreeKGAdapter._load` | src/adapter.py |
| 2 | 0.003175 | function | `_load_dir_list` | src/config.py |
| 3 | 0.002515 | method | `FileTreeKGExtractor.node_kinds` | src/extractor.py |
| 4 | 0.002238 | class | `SnapshotDelta` | src/snapshots.py |
| 5 | 0.002213 | function | `_hydrate_snapshot` | src/snapshots.py |
| 6 | 0.001928 | function | `metrics_from_dict` | src/snapshots.py |
| 7 | 0.001928 | function | `delta_from_dict` | src/snapshots.py |
| 8 | 0.001692 | class | `SnapshotMetrics` | src/snapshots.py |
| 9 | 0.001576 | method | `FileTreeKGExtractor.meaningful_node_kinds` | src/extractor.py |
| 10 | 0.001552 | function | `metrics_to_dict` | src/snapshots.py |
| 11 | 0.001426 | method | `FtreeSnapshotManager._collect_dir_node_counts` | src/snapshots.py |
| 12 | 0.001398 | function | `delta_to_dict` | src/snapshots.py |
| 13 | 0.001357 | method | `FileTreeKGExtractor._get_metadata` | src/extractor.py |
| 14 | 0.001330 | method | `FtreeSnapshotManager.load_snapshot` | src/snapshots.py |
| 15 | 0.001330 | method | `FtreeSnapshotManager._compute_delta_from_metrics` | src/snapshots.py |
| 16 | 0.001176 | module | `conftest` | conftest.py |
| 17 | 0.001176 | function | `sample_filesystem` | conftest.py |
| 18 | 0.001176 | module | `query_examples` | examples/query_examples.py |
| 19 | 0.001176 | function | `basic_queries` | examples/query_examples.py |
| 20 | 0.001176 | function | `pack_snippets` | examples/query_examples.py |

---

## Concern-Based Hybrid Ranking

Top structurally-dominant nodes per architectural concern (0.60 × semantic + 0.25 × CodeRank + 0.15 × graph proximity).

### Configuration Loading Initialization Setup

| Rank | Score | Kind | Name | Module |
|------|-------|------|------|--------|
| 1 | 0.8508 | method | `FileTreeKGAdapter._load` | src/adapter.py |
| 2 | 0.7461 | method | `FileTreeKGAdapter.__init__` | src/adapter.py |
| 3 | 0.7425 | method | `FileTreeKG.__init__` | src/module.py |
| 4 | 0.7333 | method | `FileTreeKGExtractor.__init__` | src/extractor.py |

### Data Persistence Storage Database

| Rank | Score | Kind | Name | Module |
|------|-------|------|------|--------|
| 1 | 0.7793 | function | `_hydrate_snapshot` | src/snapshots.py |
| 2 | 0.75 | function | `save_snapshot` | src/cli/cmd_snapshot.py |
| 3 | 0.7342 | function | `pack` | src/cli/cmd_query.py |
| 4 | 0.7315 | method | `FileTreeKGAdapter.is_available` | src/adapter.py |
| 5 | 0.7287 | method | `FtreeSnapshotManager.save_snapshot` | src/snapshots.py |

### Query Search Retrieval Semantic

| Rank | Score | Kind | Name | Module |
|------|-------|------|------|--------|
| 1 | 0.75 | function | `query` | src/cli/cmd_query.py |
| 2 | 0.7022 | function | `pack` | src/cli/cmd_query.py |
| 3 | 0.6947 | function | `basic_queries` | examples/query_examples.py |
| 4 | 0.686 | function | `stats` | examples/query_examples.py |
| 5 | 0.685 | function | `analyze` | examples/query_examples.py |

### Graph Traversal Node Edge

| Rank | Score | Kind | Name | Module |
|------|-------|------|------|--------|
| 1 | 0.7607 | method | `FileTreeKGExtractor.meaningful_node_kinds` | src/extractor.py |
| 2 | 0.75 | method | `FileTreeKGExtractor.extract` | src/extractor.py |
| 3 | 0.7466 | method | `FtreeSnapshotManager._collect_dir_node_counts` | src/snapshots.py |
| 4 | 0.7426 | method | `FileTreeKGExtractor.edge_kinds` | src/extractor.py |
| 5 | 0.7371 | method | `FileTreeKGExtractor.coverage_metric` | src/extractor.py |



---

*Report generated by CodeKG Thorough Analysis Tool — analysis completed in 3.5s*
