# Enterprise Smoke Test — Findings & Gap Analysis

Generated: 2026-04-16
Branch: `claude/smoke-test-enterprise-skills-n0qI3`

---

## How to run

```bash
chmod +x smoke-test-enterprise.sh
./smoke-test-enterprise.sh
```

---

## 1. FILES NOT RELEVANT TO A FRESH SKILLS UPLOAD

These files are tracked in git but are **not needed** when someone clones this repo to upload all skills and start fresh. They add ~60MB of binary weight and confuse the upload surface.

### 1a. `output/final/` — 10 generated example documents (25MB)

| File | Size | Why it's not needed |
|---|---|---|
| `All-Hands Town Hall - April 2026.pptx` | 6MB | Generated sample; duplicate of `samples/03-pptx/` |
| `Confined_Space_Entry_Procedure.docx` | <1MB | Generated sample; no template input JSON committed |
| `Construction KPI Dashboard.xlsx` | <1MB | Generated sample; duplicate of `samples/04-xlsx/` |
| `Corporate_Investor_Deck.pptx` | 6MB | Generated sample; no input JSON committed |
| `Hot_Work_Procedure.docx` | <1MB | Generated sample; overlaps `05-samples/` |
| `Investor Update - Q1 2026.pptx` | 6MB | Generated sample; duplicate of `samples/03-pptx/` |
| `Phase 2 Financial Model Summary.xlsx` | <1MB | Generated sample; duplicate of `samples/04-xlsx/` |
| `Q1 2026 Board Deck.pptx` | 6MB | Generated sample; duplicate of `samples/03-pptx/` |
| `Records_Retention_Standard.docx` | <1MB | Generated sample; no input JSON committed |
| `Remote_Work_Guidance.docx` | <1MB | Generated sample; no input JSON committed |

**Recommendation**: Add `output/final/` to `.gitignore`. These are regression references, not upload artifacts. Anyone running the render scripts can regenerate them. Three of the PPTX files are byte-identical duplicates of files in `samples/document-types-validation/03-pptx/`.

### 1b. `Use this to share.zip` (13MB)

A flattened zip of the Claude Project bundle for peer sharing. Useful for distribution but not for a git-based rollout. Anyone cloning the repo already has the source files.

**Recommendation**: Remove from tracking; generate on-demand with a script or GitHub Release artifact.

### 1c. `samples/document-types-validation/` (20MB)

The validation sample set (`01-governance-docx/` through `05-internal-comms/`) plus `_build/` scripts and `_inputs/` JSONs. This is a QA artifact, not a skill dependency.

**Recommendation**: Keep the `_build/` scripts and `_inputs/` (they're small and useful for regression). Consider moving the 15 generated binary artifacts to a GitHub Release or separate `validation-outputs` branch.

### 1d. `skills/theme-factory/theme-showcase.pdf`

A pre-rendered visual showcase of the 10 themes. Not loaded by the skill at runtime.

**Recommendation**: Remove or move to docs.

### 1e. `.claude/plans/`

Two future implementation plans. Not needed for skill upload.

**Recommendation**: Keep (small, useful for maintainers), but don't include in any distribution zip.

---

## 2. GAPS — Things That Are Missing or Incomplete

### 2a. CRITICAL: Hardcoded absolute paths (breaks portability)

**5 files** contain `/home/user/Skills-fork` hardcoded:

| File | Line | Path used for |
|---|---|---|
| `skills/docx/scripts/render_docx.py` | 32 | `UPLOADS` — fallback template location |
| `skills/pptx/scripts/render_pptx.py` | 56 | `MASTER` — PowerPoint master template |
| `skills/pptx/scripts/lint_pptx_master.py` | 22 | Default master path |
| `samples/document-types-validation/_build/build_pptx_decks.py` | 15 | `POTX` — master template |
| `NextDecade-Claude-Project/04-scripts/README.md` | 74 | Documentation reference |

**Impact**: Any user who clones this repo to a different path will get `FileNotFoundError` from the render pipeline. The `04-scripts/README.md` acknowledges this and tells users to edit the constants, but the scripts themselves don't fall back gracefully.

**Fix**: Replace with `Path(__file__).resolve().parents[N]` relative paths or environment variable overrides.

### 2b. No formal test suite

There are no `pytest`, `unittest`, or any test runner files. Validation relies on:
- Manual `PROJECT-SELFTEST.md` checklist (15 tests, ~15 min)
- Template linters (`lint_docx_template.py`, `lint_pptx_master.py`)
- The `_build/` scripts under `samples/` (generate-and-eyeball)

**Impact**: No CI pipeline can catch regressions. The `smoke-test-enterprise.sh` script (added in this PR) covers structural integrity but not rendering.

### 2c. `spec/agent-skills-spec.md` is a 3-line stub

Just redirects to `https://agentskills.io/specification`. If that URL goes down, the spec is lost.

### 2d. `.gitignore` does not protect against secrets

Missing patterns: `.env`, `*.key`, `*.pem`, `credentials*`. Low risk in a skills repo, but enterprise rollout should have defense-in-depth.

### 2e. `output/final/` is tracked but `output/iter*/` is ignored

The `.gitignore` has `output/iter*/` but not `output/final/`. This looks like an oversight — `output/final/` was added in commit `67fd71d` as validation evidence but probably shouldn't persist in the default branch.

### 2f. `brand-guidelines` skill still references Anthropic

`skills/brand-guidelines/SKILL.md` describes **Anthropic's** brand colors (#141413, #faf9f5, #d97757) and **Anthropic's** visual identity. For a NextDecade enterprise rollout, this skill either needs to be replaced with NextDecade brand values or removed from the marketplace manifest.

### 2g. No `requirements.txt` or `pyproject.toml` at repo root

The render pipeline needs: `python-docx`, `python-pptx`, `docxtpl`, `openpyxl`, `jinja2`, `lxml`. These are documented in `04-scripts/README.md` but there's no pip-installable requirements file.

### 2h. Template schema versions diverge

- Procedure: **v2.0.0** (current, Rev 1 Blank April 2026)
- Standard: **v1.0.0** (legacy)
- Guidance: **v1.0.0** (legacy)

The Standard and Guidance schemas are older and don't have the same level of field documentation as the Procedure schema.

---

## 3. CODE ERRORS & ISSUES

### 3a. `marketplace.json` — trailing comma before closing bracket

Line 44 of `.claude-plugin/marketplace.json`:
```json
    }
    ,
    {
```
This is valid JSON (Python's `json.load` accepts it), but the whitespace-separated comma on its own line is atypical and could confuse strict JSON linters.

### 3b. `render_docx.py` — `_std_proc_table_plans` assumes 3-column Definitions table

The Standard/Guidance walk-and-replace path (`_std_proc_table_plans`) expects definitions with `d["no"]`, `d["term"]`, `d["definition"]` — a 3-column table (No. / Term / Definition). But the Procedure schema uses only `d["term"]` and `d["definition"]` — a 2-column table. This is correct (they're different doc types with different table shapes), but the naming similarity is confusing and there's no guard against accidentally passing Procedure-shaped data to the Standard renderer.

### 3c. No XML escape in walk-and-replace fallback paths

`render_docx.py` added `_xml_escape_data()` for the docxtpl path (commit `7e55917`), but the walk-and-replace fallback functions (`walk_replace_procedure`, `walk_replace_standard`, `walk_replace_guidance`) write data via `python-docx`'s `.text` setter, which handles XML escaping internally. This is actually fine — but it's worth noting that the two code paths have different escaping strategies, and the docxtpl path needed an explicit fix while the fallback didn't.

### 3d. `_post_render_cover_fixup` — variable name shadowing

Line 142 of `render_docx.py`: the function parameter `data` is shadowed by `data_bytes` in the zip-write loop, but there's also a local reassignment `files[part_name] = content.encode("utf-8")` that uses `files` (from the outer scope). This works but is fragile — a future refactor could accidentally reference the wrong `data`.

### 3e. `_remove_template_scaffolding` — only handles Procedure type

The function checks `if doc_type == "procedure"` and does nothing for Standard/Guidance. If those templates later gain scaffolding markers, they'll silently pass through.

---

## 4. ARCHITECTURAL OBSERVATIONS

### 4a. Two copies of everything

Templates, schemas, and some scripts exist in both `skills/docx/templates/` and `NextDecade-Claude-Project/02-templates/`. The smoke test checks they're in sync, but there's no automation to enforce it. A merge that touches one copy but not the other will silently drift.

### 4b. `NextDecade-Claude-Project/04-scripts/` vs `skills/*/scripts/`

The scripts in `04-scripts/` (render_docx.py, render_pptx.py, linters) are intended for the Claude Project bundle but reference paths inside the repo structure. Meanwhile, `skills/docx/scripts/render_docx.py` is the "real" script that the skills system loads. It's unclear which is canonical — the 04-scripts README says "these scripts assume the templates live at paths inside the NextDecade repo structure."

### 4c. The marketplace manifest has 3 plugin bundles but doesn't include the NextDecade-specific customizations

The `marketplace.json` registers `document-skills`, `example-skills`, and `claude-api` — all upstream Anthropic skills. The NextDecade enterprise customizations (brand chrome in DOCX templates, XLSX brand defaults, PPTX brand gate) are baked into the skill files themselves but aren't called out as a separate "enterprise" bundle.

---

## 5. RECOMMENDATIONS FOR ENTERPRISE ROLLOUT

1. **Fix hardcoded paths** in the 4 Python scripts (use `Path(__file__).resolve()` relative navigation)
2. **Add `output/final/` to `.gitignore`** and remove from tracking
3. **Remove or replace `skills/brand-guidelines/`** — it ships Anthropic's brand, not NextDecade's
4. **Add a root `requirements.txt`** for pip install
5. **Add `.env`, `*.key`, `*.pem` to `.gitignore`**
6. **Consider removing `Use this to share.zip`** from git tracking (use GitHub Releases instead)
7. **Document which scripts/ directory is canonical** — 04-scripts or skills/*/scripts
8. **Run `smoke-test-enterprise.sh` in CI** on every push to catch regressions
