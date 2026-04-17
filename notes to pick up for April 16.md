# Notes to pick up for April 16

**For the next Claude session — read this first, then delete this file when we're done.**

---

## How to use this file

1. Read this file end-to-end before touching anything else.
2. Check the branch: `git branch --show-current` should return `claude/review-template-compliance-DUx1u`.
3. Verify current state by running the commands in the "Verification" section below.
4. Then proceed with the user's ask: **test for edge cases and harden the render pipeline.**
5. When the user says we're done with this handoff, **delete this file** (`rm "notes to pick up for April 16.md"`) as the user explicitly requested.

---

## Project context

Enterprise skill-file build for NextDecade. Multi-format document automation (DOCX, PPTX, XLSX, etc.). Three governance DOCX document types that matter here: **Procedure**, **Standard**, **Guidance**. Render pipeline lives in two mirrored copies:

- `skills/docx/scripts/render_docx.py` — Claude Code CLI path
- `NextDecade-Claude-Project/04-scripts/render_docx.py` — Claude Projects web path

Templates in `skills/docx/templates/` with mirror copies in `NextDecade-Claude-Project/02-templates/`. The two `render_docx.py` copies intentionally differ on 3 path-constant lines; smoke test section 30 filters those before comparing.

---

## What was done in this session (2 commits on this branch)

### Commit `bb22910` — Template compliance review (partially reverted by next commit)

- Documented that the "diverged render scripts" smoke-test warning was a false alarm (only 3 path-constant lines differ; added NOTE comments in both files).
- **Schema key normalization:** renamed `revision_history.number` → `rev` in Standard + Guidance schemas + sample JSONs, plus the matching `{{ rev.number }}` → `{{ rev.rev }}` edit inside the Standard + Guidance `.docx` templates. Added back-compat shim in `fill_rev` accepting both keys.
- **Brand-patched** theme1.xml and Heading 1–4 colors across all templates to Segoe UI + #002060 navy. **This was the wrong call.** User pushed back in the next turn: "I don't want the branding guidelines to ever overwrite my standard and procedure docx template."

### Commit `62d2894` — Single-source-template invariant (current state)

User's policy: **the DOCX template is the authoritative source of formatting. Brand guidelines never override templates.** Applies to Procedure + Standard. Guidance deferred to a separate decision.

Five ships delivered in this commit:

1. **Reverted** my brand-patches on Procedure + Standard `.docx` files (6 files total: both Jinja copies + both original-template copies + the originals in `03-original-templates/`). Standard's `{{ rev.rev }}` schema rename is preserved.
2. **Kept** the schema rename and render-script NOTE comments from commit 1.
3. **Architectural rewrite:** `walk_replace_procedure` and `walk_replace_standard` went from 368-line stateful XML manipulators to ~3-line wrappers around a new `render_via_docxtpl_lenient()` function that uses Jinja2 `ChainableUndefined`. Both render paths now read from the **same** Jinja template. Drift impossible by construction for Procedure + Standard.
4. **Removed** `original_template_candidates` from DOC_TYPES for Procedure + Standard. The `03-original-templates/*.docx` files for those two doc types remain on disk as archival but no code consults them.
5. **Added smoke test step 31** in `smoke-test-enterprise.sh`: renders each sample via both paths, asserts output `theme1.xml` major font + Heading 1 color match the source template. Any future programmatic formatting override fails this test.

Also: deleted `_patch_header2` and `_std_proc_table_plans` (unused after the rewrite); updated `skills/docx/SKILL.md` with the invariant note.

---

## Critical context the next agent must know

1. **Do not re-add `document_name` or `doc_number` to Standard's `required_markers`.** The schema has a `_required_markers_note` explaining why — those fields are consumed by the post-render cover-fixup (text-box substitution), not by docxtpl. Listing them as required caused every Standard render to fail lint and fall through to the fallback path, which was the root cause of the original "output doesn't match template" bug.
2. **Both `render_docx.py` copies must stay in sync** (except for 3 path-constant lines). Smoke test section 30 enforces this. When editing one, mirror to the other.
3. **Guidance is out of scope.** Don't modify it. Guidance still has:
   - Its brand-patched theme (Segoe UI + #002060 from my commit 1, not reverted)
   - The same `document_name` / `doc_number` bug in `required_markers` (every render goes through fallback)
   - Dependency on `03-original-templates/Guidance Template.docx` via the legacy `walk_replace_guidance` code
   Flag Guidance for follow-up when the user is ready.
4. **The lenient-fallback path is newly written.** I tested against three sample JSONs and confirmed both paths produce matching fingerprints. **I did NOT exhaustively test edge cases.** That's the user's ask for this next session.

---

## User's ask for this next session

> "I want you to test for edge cases and harden."

Scope: the new `render_via_docxtpl_lenient()` + the two thin-wrapper `walk_replace_*` functions + their interaction with the router in `render()`.

## Edge-case checklist (priority-ordered)

### High-priority (most likely to bite real users)

1. **Missing required data keys** — strict path raises `UndefinedError` with field name. Lenient path renders empty strings. Pass a partial input JSON missing (say) `scope_text`. Verify strict raises cleanly and lenient produces a valid `.docx` with an empty scope section (not a crashed/corrupted file).
2. **Missing nested attrs** — `{{ rev.rev }}` inside `{%tr for rev in revision_history %}`. If `revision_history = []`, does the table render correctly (empty body, preserved header) in both paths?
3. **Empty list fields** — `roles: []`, `definitions: []`, `references: []`, `appendices: []`. docxtpl's `{%tr for %}` typically handles empty iterables but verify template rows don't leak.
4. **XML-special characters in data** — `&`, `<`, `>`, `"`, `'`, em-dashes, smart quotes. `_xml_escape_data()` exists but was only tested against three sample JSONs. Try a role name with `&`, a purpose_text with `<foo>`, a reference title with smart quotes.
5. **Unicode:** non-ASCII, emoji, RTL text, combining characters.
6. **Very long strings** — a `purpose_text` that's 10,000 characters. Does it wrap correctly, overflow the page, trigger a Word pagination edge case?
7. **Very large lists** — 100+ revision history rows, 50+ references, 20+ appendices. Perf + correctness.
8. **Invalid input types** — `revision_history: "not a list"`, `roles: null`. What errors surface and are they actionable?
9. **Back-compat shim in `fill_rev`** — accepts `rev.get("rev", rev.get("number", ""))`. Test mixed input where some rows use `rev` and others `number`.
10. **Duplicate keys in input JSON** — parser picks one; verify it's the last one (or document the behavior).

### Cover-fixup edge cases

11. **`document_name` contains XML-special chars** — cover fixup is raw text replacement; does it escape correctly? Test a standard with `"AT&T Services Standard"`.
12. **`doc_number` format variations** — unusual formatting, different column count than `xxx-xxx-xxx-xxx-xxx-#####`.
13. **`document_name` or `doc_number` missing entirely** — cover-fixup currently returns `[]` if both empty; test one-but-not-the-other.

### Render-path routing edge cases

14. **Lint exit code 2 (warnings only)** — strict docxtpl should still be tried. Test a template with lint warnings.
15. **docxtpl syntax error inside a template** (e.g., malformed `{% %}`) — does the lenient fallback also fail? Does it degrade gracefully?
16. **Template file missing or corrupted** — what error does the user see? Actionable?
17. **`allow_fallback=False`** — verify strict-only mode raises instead of falling through.

### Structural

18. **PDF conversion pipeline** — `convert_to_pdf` invoked with `--pdf` flag. Test with the new lenient path.
19. **Concurrent renders** — two `render()` calls against the same template file simultaneously. Shared-state issues?
20. **Sample JSON validator** — no test verifies sample JSONs are valid input for their schemas. Worth adding.
21. **Schema sync check** — no test verifies `02-templates/*.json` are byte-identical to `skills/docx/templates/*.json`. They should be.

### Template integrity

22. **Accidental template damage** — if someone edits a `.docx` template in Word and damages a Jinja marker, does the lint catch it? Worth running `lint_docx_template.py` in CI.
23. **Step 31 fingerprint is narrow** — only checks major font + Heading 1 color. A template could drift in other ways (minor font, Heading 2–4 colors, body font, margins, footer text) and step 31 wouldn't catch it. Consider broadening.

### Deferred (out of scope unless user reopens)

24. Guidance's legacy fallback path + drift risk.
25. Guidance's `required_markers` bug (same as Standard had).
26. Guidance's leftover brand-patched theme from commit 1 (not reverted).

---

## Verification commands (run these first to confirm state)

```bash
cd /home/user/Skills-fork
git log --oneline -3
# Should show 62d2894 "Single-source-template invariant for Procedure + Standard" at top

bash smoke-test-enterprise.sh
# Expect: PASS 189, FAIL 0, WARN 9 (all pre-existing advisory)
# Step 31 should show 4 PASS lines:
#   procedure-happy, procedure-fallback, standard-happy, standard-fallback

python3 skills/docx/scripts/lint_docx_template.py \
    "skills/docx/templates/Procedure Template (Jinja).docx" \
    "skills/docx/templates/procedure_schema.json"
# Expect: exit 0, issues=[], warnings=[]

python3 skills/docx/scripts/lint_docx_template.py \
    "skills/docx/templates/Standard Template (Jinja).docx" \
    "skills/docx/templates/standard_schema.json"
# Expect: exit 0, issues=[], warnings=[]

# Guidance still has its legacy state — exit 3 with 2 issues. Expected.
python3 skills/docx/scripts/lint_docx_template.py \
    "skills/docx/templates/Guidance Template (Jinja).docx" \
    "skills/docx/templates/guidance_schema.json"
```

Current fingerprints to confirm output still matches templates:
- Procedure: Segoe UI / Heading 1 = `#2F5496`
- Standard: Aptos Display / Heading 1 = `#0F4761`
- Guidance: Segoe UI / Heading 1 = `#002060` (brand-patched, not reverted)

---

## Working style the user prefers

- Concise updates. Brief is fine; silent is not.
- Ask before making risky architectural changes.
- Be honest about what's tested vs. not.
- Commit + push to this same branch (`claude/review-template-compliance-DUx1u`).
- **Do not create PRs** unless the user explicitly asks.
- Don't create documentation files unless asked (this one is asked — delete when done).

---

## Dependencies installed during last session

- `python-docx` (1.2.0)
- `docxtpl` (0.20.2)
- `lxml` (6.0.4)
- `typing_extensions` (4.15.0)

If a fresh container loses these, reinstall: `pip install python-docx docxtpl`.

---

## When we're done

Delete this file:

```bash
rm "/home/user/Skills-fork/notes to pick up for April 16.md"
```

Commit the deletion with a clear message so the audit trail shows this was a handoff doc by design.
