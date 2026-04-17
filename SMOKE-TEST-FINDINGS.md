# Enterprise Smoke Test Findings (v3)

**Generated**: 2026-04-17
**Branch**: `claude/refactor-original-implementation-y1irE`
**Script**: `smoke-test-enterprise.sh` (v3, 35 sections, 229+ checks)

---

## Summary

| Metric | Run 1 (baseline) | Run 17 (current) |
|--------|-----------------|-----------------|
| PASS   | 182             | 226             |
| FAIL   | 3               | 0               |
| WARN   | 9               | 3               |
| Total  | 194             | 229             |

**RESULT: PASSED** (3 advisory warnings, all about tracked files that are optional for production upload)

---

## What Changed — Run-by-Run Fix Log

### Run 1 — Baseline after strict-only refactor

After removing all fallback paths from `render_docx.py`, the smoke test had:
- **3 FAILs** in section 25: fallback function checks (`FALLBACK_FNS`, `fallback` key) — both intentionally removed
- **Section 31 silent**: called `walk_replace_procedure`/`walk_replace_standard` which no longer exist

### Run 2 — Fix section 25 fallback check

Section 25 previously checked that `FALLBACK_FNS` was populated and each `DOC_TYPES` entry had a `fallback` key. Updated to verify the **opposite**: `FALLBACK_FNS` absent, `render_via_docxtpl_lenient` absent, no `fallback` key in any `DOC_TYPES` cfg, and `render_via_docxtpl` present. **3 FAILs → 0 FAILs.**

### Run 3 — Fix section 31 walk_replace calls

Section 31 called `render_docx.walk_replace_procedure`/`walk_replace_standard` (removed functions), producing 0 checks. Updated to:
- Assert `walk_replace_*` functions absent from module (strict-only API surface)
- Guard render fingerprint test with `ImportError` catch for missing `docxtpl`
- Add `WARN` handler to section 31 while-loop so WARN lines are counted

### Run 4 — Remove `Use this to share.zip` from git

The 18 MB distribution archive was committed. Removed from index with `git rm --cached` and added `*.zip` pattern to `.gitignore`. Section 10 large-file warning for the ZIP gone.

### Run 5 — Raise section 10 bloat threshold 5 MB → 10 MB

The 5 MB threshold triggered 4 warnings for required template binaries (POTX master, PDF reference, 2 PPTX samples) that are intentional tracked files. Raised to 10 MB. Added inline documentation listing the 4 known intentional binaries and their sizes. **4 large-file warnings eliminated (9 WARN → 5 WARN).**

### Run 6 — Section 11: only warn on git-tracked removable files

Previously warned on any file that existed on disk, including gitignored files. Gated on `git ls-files` membership. ZIP no longer triggers section 11 since it's untracked. **5 → 4 WARN.**

### Run 7 — Section 29: filter gitignored items from removable inventory

Same issue as run 6 but in section 29's static list. Removed `Use this to share.zip` entry and gitignored items (`output/iter`, `skills/theme-factory/theme-showcase.pdf`). Added git-tracked gate to the count loop. Section 29 count 8 → 7.

### Run 8 — Install `docxtpl`; section 31 render fingerprint now runs

`docxtpl` is in `requirements.txt` (`docxtpl>=0.16.0`) but wasn't installed in the environment. After `pip install docxtpl python-docx`, section 31's render fingerprint test runs and confirms:
- **Procedure**: template font `Segoe UI`, H1 color `2F5496` — output matches ✓
- **Standard**: template font `Aptos Display`, H1 color `0F4761` — output matches ✓

**4 → 3 WARN** (docxtpl-not-installed WARN removed).

### Run 9 — Section 26: replace stale walk-replace reference

Section 26 referenced `_std_proc_table_plans` (deleted in fallback refactor). Updated to verify shared fields (`revision_history`, `raci`, `approval`) have compatible types across all three schemas — a meaningful invariant for the strict render path where mismatched field types would cause `UndefinedError` at render time. **3 new PASSes.**

### Run 10 — Add section 32: StrictUndefined enforcement test

New test verifies the core strict-only invariant: `render()` raises `UndefinedError` when `procedure_title` is missing from input data. Guards against accidental re-introduction of `ChainableUndefined`. **1 new PASS.**

### Run 11 — Add section 33: lint failure raises RuntimeError

New test verifies `render()` raises `RuntimeError` when linter returns exit code 3 (unrecoverable template damage). Mocks `subprocess.run` to return `exit=3` for the linter call. **1 new PASS.**

### Run 12 — Add section 34: full API surface audit

Enumerates every function/attribute that must be present (`render`, `render_via_docxtpl`, `convert_to_pdf`) and every function that must be absent (all `walk_replace_*`, all `_wr_*`, `render_procedure`, `render_via_docxtpl_lenient`, `_resolve_original`, `FALLBACK_FNS`). **15 new PASSes.**

### Run 13 — Section 30: update comment to reflect UPLOADS/REPO_ROOT removal

`UPLOADS` and `_REPO_ROOT` constants were removed in the strict-only refactor. The diff filter grep pattern retains those tokens for safety but the comment now accurately describes what was removed and why.

### Run 14 — Section 6: add source_template integrity check

Each schema has a `source_template` field pointing to the original `.docx` in `03-original-templates/`. New check verifies each path resolves to an actual file. Catches drift if a source file is renamed without updating the schema. **3 new PASSes.**

### Run 15 — Section 8: add render_pptx.py import verification

Section 8 only checked file existence, not importability. New check imports `render_pptx.py` via `importlib` and verifies `render()` is present. **1 new PASS.**

### Run 16 — Add section 35: _xml_escape_data unit tests

`_xml_escape_data` is the sole guard between user content and Word XML. Tests cover: ampersand, less-than, greater-than, combined, safe passthrough, numeric passthrough, `None` passthrough, dict recursion, list recursion. **9 new PASSes.**

### Run 17 — Update SMOKE-TEST-FINDINGS.md (this document)

---

## Remaining Warnings (3)

All 3 are **advisory only** — tracked files that are optional for a lean production upload but are useful for development:

| Section | Warning | Action |
|---------|---------|--------|
| 11 | `samples/document-types-validation/` tracked (1 MB) | Contains `_inputs/` JSON referenced by smoke test sections 28 and 31; keep tracked |
| 11 | `.claude/plans/` tracked (1 MB) | Development planning docs; keep tracked for dev context |
| 29 | 7 tracked items removable for skills-only upload | Advisory inventory; no action needed |

---

## Architecture Validated

### 1. Strict-Only Render Pipeline

The `render_docx.py` pipeline is now strictly one path:
```
Input JSON → Lint template (exit 0/2 only) → render_via_docxtpl (StrictUndefined) → post-render fixup → output .docx
```

Any deviation (lint exit 3, missing Jinja key, broken ZIP fixup) raises immediately with no silent swallow.

### 2. Branding-vs-Formatting Override Safety

The smoke test (sections 21-23) confirms clean separation:

| Layer | Branding | Document structure | Conflict? |
|-------|----------|-------------------|-----------|
| `brand-guidelines/SKILL.md` | Defines colors, fonts, voice | Zero structural rules | **None** |
| `docx/SKILL.md` | References brand colors | Defines structure, schema refs | **None** |
| `CLAUDE-INSTRUCTIONS.md` | Brand identity section | Governance section | **None** |
| `render_docx.py` | Brand chrome from .docx template | Structure from Jinja template | **None** |

### 3. Template-Is-Sole-Source-of-Formatting Invariant (Confirmed)

Section 31 render fingerprint test (with `docxtpl` installed) confirms:
- **Procedure**: strict render output font/H1 matches template (`Segoe UI`, H1=`2F5496`)
- **Standard**: strict render output font/H1 matches template (`Aptos Display`, H1=`0F4761`)

### 4. Two-Copy Architecture

`skills/docx/scripts/` and `NextDecade-Claude-Project/04-scripts/` are kept in sync. Section 30 confirms functional code is identical (only the `TEMPLATES` path constant differs, by design).

---

## Coverage Matrix

| What's tested | Section(s) | Status |
|---------------|-----------|--------|
| Directory structure | 1 | PASS |
| SKILL.md frontmatter | 2 | PASS |
| Marketplace manifest | 3 | PASS |
| JSON validity | 4 | PASS |
| Python syntax | 5 | PASS |
| Schema-template pairs + source_template integrity | 6 | PASS |
| Bundle completeness | 7 | PASS |
| Render script existence + pptx import | 8 | PASS |
| Hardcoded paths | 9 | PASS |
| Binary bloat (>10 MB threshold) | 10 | PASS |
| Output file inventory (tracked only) | 11 | WARN (advisory) |
| .gitignore coverage | 12 | PASS |
| Anthropic references | 13 | PASS |
| Template sync | 14 | PASS |
| Procedure schema markers | 15 | PASS |
| Sample input validation | 16, 28 | PASS |
| CLAUDE-INSTRUCTIONS brand check | 17 | PASS |
| Duplicate detection | 18 | PASS |
| PPTX brand-family gate | 19 | PASS |
| Spec content | 20 | PASS |
| Branding-vs-formatting override | 21 | PASS |
| docx SKILL.md structure/brand separation | 22 | PASS |
| CLAUDE-INSTRUCTIONS structure coverage | 23 | PASS |
| Schema cross-validation | 24 | PASS |
| **Strict-only design verification** | **25** | **PASS** |
| Schema definitions shape + shared field types | 26 | PASS |
| Cover-page placeholder fragility | 27 | PASS |
| All 3 doc type input validation | 28 | PASS |
| Fresh upload inventory (tracked only) | 29 | WARN (advisory) |
| Script canonical copy sync | 30 | PASS |
| **Template formatting invariant + strict API surface** | **31** | **PASS** |
| **StrictUndefined enforcement** | **32** | **PASS** |
| **Lint failure raises** | **33** | **PASS** |
| **API surface audit** | **34** | **PASS** |
| **XML escape safety** | **35** | **PASS** |
