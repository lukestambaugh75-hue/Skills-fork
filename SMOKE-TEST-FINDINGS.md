# Enterprise Smoke Test Findings (v2)

**Generated**: 2026-04-16
**Branch**: `claude/smoke-test-enterprise-WgTKd`
**Script**: `smoke-test-enterprise.sh` (v2, 30 sections, 197 checks)

---

## Summary

| Metric | Count |
|--------|-------|
| PASS   | 186   |
| FAIL   | 0     |
| WARN   | 11    |
| Total  | 197   |

---

## 1. Branding-vs-Formatting Override Validation

**Verdict: NextDecade branding does NOT override Procedure/Standard/Guidance formatting.**

The smoke test (sections 21-23) confirms clean separation at every layer:

| Layer | Branding (colors/fonts/voice) | Document structure (sections/tables/ordering) | Conflict? |
|-------|-------------------------------|-----------------------------------------------|-----------|
| `brand-guidelines/SKILL.md` | Defines colors, fonts, voice, boilerplate | Zero structural rules (no section numbers, no heading order, no schema refs) | **None** |
| `docx/SKILL.md` | References brand colors from brand-guidelines | Defines full Procedure/Standard/Guidance structure, render pipeline, schema refs | **None** |
| `CLAUDE-INSTRUCTIONS.md` | Brand identity section (lines 9-35) | Governance documents section (lines 37-71) with per-type structure | **None** (different sections, both defer to templates) |
| `render_docx.py` | Brand chrome preserved byte-identically from .docx template | Structure locked by Jinja template + schema markers | **None** (template IS the structure) |
| Walk-and-replace fallback | Copies original template (preserves all brand chrome) | Fills markers by style-name matching, not brand rules | **None** |

### Why no override is possible

1. **Template-driven rendering**: `render_docx.py` takes a `.docx` template file and fills Jinja markers. The section order, heading styles, table layouts, and page structure all come from the Word template binary -- not from any SKILL.md or CLAUDE-INSTRUCTIONS.md. Branding rules cannot alter template structure.

2. **Brand-guidelines has no structural vocabulary**: The skill defines `#002060`, `Segoe UI`, voice registers, and boilerplate text. It has no concept of "1.0 Purpose", "Revision History table", or "INTRODUCTION -> SCOPE -> GOVERNANCE". These live exclusively in the docx skill and its schemas.

3. **CLAUDE-INSTRUCTIONS.md separates concerns explicitly**: Line 36 says "use the templates in `02-templates/`" -- it defers to templates rather than re-defining structure inline. The section descriptions are documentation aids, not override rules.

4. **Walk-and-replace fallback uses style-name matching**: It targets styles like `"RGLNG 1 (Hdg1)"`, `"Body Text"`, `"Title Cover Page (Proc Title)"` which are baked into the template. Brand color changes don't affect style names.

### Edge cases to monitor

- If someone edits `brand-guidelines/SKILL.md` to add section-ordering rules (e.g., "Procedures must start with Purpose"), it would create an implicit override. The smoke test section 21 guards against this with pattern matching.
- `CLAUDE-INSTRUCTIONS.md` line 7 says "Follow the rules below unless the user explicitly overrides" -- a user could theoretically say "use NCS green for all headers" and override navy headers in a Procedure. This is by design, not a bug.

---

## 2. Code Errors Found

### 2a. Pipe-subshell counter bug (FIXED in v2)

**File**: `smoke-test-enterprise.sh` (original v1)
**Issue**: `python3 -c ... | while read ...` runs the while-loop in a subshell. PASS/FAIL/WARN counter increments were lost when the subshell exited, causing the summary to undercount.
**Fix**: Added `_COUNTER_FILE` temp file approach. Each `pass()`/`fail()`/`warn()` writes a marker to a shared file. `_reconcile_counters()` reads the file before printing the summary.

### 2b. `_std_proc_table_plans` definitions table column assumption

**File**: `render_docx.py:717-732`
**Issue**: The Standard walk-and-replace fallback assumes a 3-column Definitions table (`No.`, `Term`, `Definition`) with fields `d["no"]`, `d["term"]`, `d["definition"]`. The Procedure schema uses 2-column (`Term`, `Definition`). This is correct behavior (they're different document types with different template layouts), but the function name `_std_proc_table_plans` is misleading -- it's only used for Standard, not Procedure.
**Severity**: Low (functional, naming is confusing)

### 2c. `_post_render_cover_fixup` fragile string matching

**File**: `render_docx.py:94-146`
**Issue**: Uses exact string matches (`"NAME"`, `"xxx-xxx-xxx-xxx-xxx-#####"`) to find and replace cover-page text boxes in Standard/Guidance. If someone edits the template and changes these placeholder strings, the fixup silently becomes a no-op.
**Mitigation**: Smoke test section 27 now validates that these placeholders still exist in the templates. Currently PASS (2/2 for both Standard and Guidance).

### 2d. `_remove_template_scaffolding` incomplete for Standard/Guidance

**File**: `render_docx.py:149-194`
**Issue**: Procedure type gets thorough cleanup (removes "Use the following for notes, cautions, and warnings" paragraph + demo table). Standard/Guidance only remove `[CONTENT TITLE]`, `Enter text here`, `Click here to enter text`. If the Standard/Guidance templates gain additional scaffolding, it'll survive into rendered output.
**Severity**: Low (current templates work; future template changes need matching code updates)

---

## 3. Files NOT Relevant to Fresh Skill Upload

These files/directories can be excluded when uploading skills for a fresh start. They are examples, dev artifacts, or build outputs:

| Item | Size | Reason | Action |
|------|------|--------|--------|
| `Use this to share.zip` | 12MB | Flattened shareable bundle | Remove from git, use GitHub Releases |
| `.claude/plans/` | 1MB | Development planning docs (future implementation ideas) | Exclude from upload |
| `samples/document-types-validation/` | 1MB | Validation sample set (rebuild via `_build/` scripts) | Exclude from upload (already gitignored for binary outputs) |
| `SMOKE-TEST-FINDINGS.md` | <1MB | Previous/current smoke test findings | Exclude from upload (dev artifact) |
| `extracted-specs.md` | <1MB | Claude-readable brand distillation | Useful for Claude Projects, NOT needed for skill upload |
| `gap-report.md` | <1MB | Gap analysis report | Useful for Claude Projects, NOT needed for skill upload |
| `NextDecade-Claude-Project/05-samples/` | 9MB | Hot Work example set (6 documents) | Reference only -- exclude from skill upload |
| `NextDecade-Claude-Project/03-original-templates/` | 1MB | Source templates before Jinja tagging | Used by `build_procedure_jinja.py`, not runtime |

### What IS needed for a clean skills-only upload

```
skills/                           # All 17 skills with SKILL.md files
  docx/                           # Templates, schemas, render scripts
  pptx/                           # Render scripts, brand-family gate
  xlsx/                           # Render scripts, recalc
  pdf/                            # PDF processing scripts
  brand-guidelines/               # Brand constants
  internal-comms/                 # Comms guidelines
  [other skills]/                 # algorithmic-art, canvas-design, etc.
.claude-plugin/marketplace.json   # Skill manifest
template/SKILL.md                 # Skill template
spec/agent-skills-spec.md         # Agent Skills spec
requirements.txt                  # Python dependencies
```

### What IS needed for Claude Projects (web) upload

```
NextDecade-Claude-Project/
  01-brand-references/            # 2 PDFs
  02-templates/                   # 3 Jinja DOCX + 3 JSON schemas + 2 PPTX/PDF
  04-scripts/                     # 4 Python scripts
  START-HERE.md
  CLAUDE-INSTRUCTIONS.md          # Paste into Project custom instructions
  PROJECT-SELFTEST.md
extracted-specs.md                # Brand distillation (upload as knowledge)
gap-report.md                     # Gap analysis (upload as knowledge)
```

---

## 4. Warnings (11 total)

| # | Section | Warning | Severity | Recommendation |
|---|---------|---------|----------|----------------|
| 1-5 | 10 | 5 tracked files > 5MB (PPTX, POTX, PDF, ZIP) | Low | Move `Use this to share.zip` to Releases; others are templates that must be tracked |
| 6-8 | 11 | 3 removable items for fresh upload | Advisory | See section 3 above |
| 9 | 29 | 8 items identified as removable | Advisory | Overlaps with section 11 |
| 10-11 | 30 | `render_docx.py` and `render_pptx.py` DIVERGED between `skills/` and `04-scripts/` | Medium | Decide which is canonical and sync. `skills/` should be canonical since it's the skill runtime path; `04-scripts/` is the Claude Projects copy |

---

## 5. Architectural Observations

### 5a. Two copies of everything

Templates, schemas, and scripts exist in both `skills/docx/` and `NextDecade-Claude-Project/`. Schemas are in sync (section 6 PASS), templates are in sync (section 14 PASS), but scripts have DIVERGED (section 30 WARN). This creates maintenance burden -- edits to render_docx.py must be mirrored.

**Recommendation**: Make `skills/` canonical. Add a `sync-to-project.sh` script or symlinks.

### 5b. Schema version inconsistency

All three schemas have `schema_version: "2.0.0"` at the top level, but the `description` field in Standard and Guidance says "v1.0.0 (legacy layout)". This suggests Standard and Guidance haven't been updated to match the April 2026 Procedure revision.

### 5c. marketplace.json doesn't register NextDecade customizations

The manifest registers 3 upstream bundles (`document-skills`, `example-skills`, `claude-api`) but doesn't call out NextDecade-specific skills or customizations as a separate enterprise bundle.

### 5d. No formal test suite

The repo has: manual `PROJECT-SELFTEST.md` checklist, template linters, `_build/` eyeball scripts, and now this smoke test. But there's no `pytest`/`unittest` suite for the render pipeline. A test that renders each doc type from a fixture JSON and asserts the output XML structure would catch regressions.

---

## 6. Smoke Test Coverage Matrix

| What's tested | Section(s) | Status |
|---------------|-----------|--------|
| Directory structure | 1 | PASS |
| SKILL.md frontmatter | 2 | PASS |
| Marketplace manifest | 3 | PASS |
| JSON validity | 4 | PASS |
| Python syntax | 5 | PASS |
| Schema-template pairs | 6 | PASS |
| Bundle completeness | 7 | PASS |
| Script existence | 8 | PASS |
| Hardcoded paths | 9 | PASS |
| Binary bloat | 10 | WARN |
| Output file inventory | 11, 29 | WARN |
| .gitignore coverage | 12 | PASS |
| Anthropic references | 13 | PASS |
| Template sync | 14 | PASS |
| Procedure schema markers | 15 | PASS |
| Sample input validation | 16, 28 | PASS |
| CLAUDE-INSTRUCTIONS brand check | 17 | PASS |
| Duplicate detection | 18 | PASS |
| PPTX brand-family gate | 19 | PASS |
| Spec content | 20 | PASS |
| **Branding-vs-formatting override** | **21** | **PASS** |
| **docx SKILL.md structure/brand separation** | **22** | **PASS** |
| **CLAUDE-INSTRUCTIONS structure coverage** | **23** | **PASS** |
| **Schema cross-validation** | **24** | **PASS** |
| **Render pipeline dry-run** | **25** | **PASS** |
| **Definitions table column check** | **26** | **PASS** |
| **Cover-page placeholder fragility** | **27** | **PASS** |
| **All 3 doc type input validation** | **28** | **PASS** |
| **Fresh upload inventory** | **29** | **WARN** |
| **Script canonical copy sync** | **30** | **WARN** |
