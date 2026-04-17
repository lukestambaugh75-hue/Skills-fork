# Enterprise Overview

Read this before using, editing, or rolling out this repository.

---

## TL;DR

- **What this repo is:** a fork of Anthropic's public [`anthropics/skills`](https://github.com/anthropics/skills) marketplace, extended with a **NextDecade Corporation document-rendering pipeline** (Jinja-tagged DOCX / PPTX templates, a render pipeline, validation samples, and a drop-in Claude Project bundle). It is our company's canonical source for agent skills, the `SKILL.md` authoring standard, and the brand-compliant document generation workflow.
- **Who it is for:** anyone inside the company who drafts a NextDecade governance document, presentation, internal email, or branded spreadsheet; writes or edits a skill; or sets the Markdown standard that all of the above share.
- **Before rollout:** review [Gaps before rollout](#gaps-before-rollout). The repo is content-ready; ownership, sync policy, and marketplace metadata still need company-specific decisions.

---

## 1. What this repo is

This is a **fork**, not a new project. The skills in `skills/` are Anthropic's published examples plus the four document-processing skills (`docx`, `pdf`, `pptx`, `xlsx`) that power Claude's native document capabilities.

We are keeping the fork because it gives us three things at once:

1. **A working marketplace** — `.claude-plugin/marketplace.json` is a real plugin bundle a Claude Code user can install with `/plugin marketplace add ...`. We can ship it to the enterprise deployment with zero additional scaffolding.
2. **A library of reference skills** — 17 skills covering document generation, design, testing, communications, API development, and skill-authoring itself. These are our working examples of "what a good skill looks like."
3. **A style anchor for company Markdown** — every skill's `SKILL.md` is itself a piece of structured documentation. The patterns these files use (YAML frontmatter, trigger descriptions, `When to use` / `How it works` / `Examples` / `Guardrails` sections, relative links into `scripts/` and `references/`) become our house style for company docs.

---

## 2. History & intent

The full commit log is short (28 commits) and tells a clear story:

| Phase | Commits | What happened |
|---|---|---|
| Bootstrap | `37292f3 init repo` → `83291af` | Anthropic published the repo with skill examples organized into folders. |
| Spec introduced | `10e0fbe` | First public draft of the Agent Skills spec. |
| Spec split out | `f232228`, `be229a5`, `69c0b1a` | Spec content moved to [agentskills.io/specification](https://agentskills.io/specification); `spec/agent-skills-spec.md` became a 3-line redirect. |
| Example skills added | `0f77e50`, `e5c6015`, `0075614`, etc. | `frontend-design`, `doc-coauthoring`, and friends. |
| Document skills added | `4e6907a`, `a5bcdd7` | `docx`, `pdf`, `pptx`, `xlsx` — the production document capabilities. |
| `claude-api` skill | `7029232`, `98669c1`, `887114f`, `ca1e7dc` | Long-running skill for SDK-based apps. |
| YAML rendering fix | `0f7c287` | Most recent upstream commit. |
| **This audit** | local commits on `claude/audit-and-document-NqUn5` | See [Appendix: Audit + fix record](#appendix-audit--fix-record). |

**On "everything merged":** the branch `claude/audit-and-document-NqUn5` was at parity with `main` before this audit. Any prior work you may have thought was merged into this branch was **not** here — it was either upstream content or lives elsewhere. Confirm that separately if it matters.

**Meeting the intent:** yes, this repo can serve the stated purpose (enterprise skills + documentation standard), provided the eight rollout gaps below are closed. It is not ready to deploy as-is, but none of the gaps require reshaping the repo — they are ownership, metadata, and policy decisions only.

---

## 3. Repo map

| Path | What it is |
|---|---|
| `README.md` | Top-level readme. Starts with our Enterprise section, then preserves upstream content verbatim below. |
| `ENTERPRISE_OVERVIEW.md` | This file. |
| `.claude-plugin/marketplace.json` | Claude Code plugin manifest. Declares three plugin bundles: `document-skills`, `example-skills`, `claude-api`. 17 skills total, 1:1 with `skills/` on disk. |
| `skills/` | 17 skill directories — see [§4 Catalog](#4-catalog-of-skills). |
| `spec/agent-skills-spec.md` | 3-line redirect to agentskills.io. Intentional. |
| `template/SKILL.md` | Starter template for new skills. Re-authored during this audit to model the enterprise standard. |
| `THIRD_PARTY_NOTICES.md` | License notices for bundled third-party assets (fonts, FFmpeg, Pillow, imageio). Required for the document skills. |
| `.gitignore` | Standard OS/IDE ignores. |
| `NextDecade-Claude-Project/` | Drop-in bundle for Claude.ai Projects — brand references, Jinja templates, original Word sources, Python render scripts, and a full sample set. See [§5 NextDecade pipeline](#5-nextdecade-document-pipeline). |
| `NEXTDECADE-TEMPLATE.md` | Short guide describing the procedure/standard/guidance template system. |
| `samples/` | Sample inputs + rendered outputs used to validate the render pipeline across every document type. See `samples/document-types-validation/`. |
| `test-inputs/` | JSON input files you can drop in and render with the `render_docx.py` / `render_pptx.py` scripts. `test-inputs/README.md` shows exact commands. |
| `smoke-test-enterprise.sh` | Executable, ~74 KB. End-to-end smoke test that exercises the render pipeline and skills integration. Read before running. |
| `requirements.txt` | Python dependencies for the render pipeline (`docxtpl`, `python-docx`, `python-pptx`, Pillow, etc.). Install with `pip install -r requirements.txt`. |
| `extracted-specs.md` | Machine-readable distillation of the NextDecade Brand & Style Guidelines and Writing Style Guide PDFs. Claude reads this directly. |
| `gap-report.md` | Known gaps between current templates and the extracted spec. Maintain it as gaps are closed. |
| `SMOKE-TEST-FINDINGS.md` | Cumulative log of smoke-test runs (29 runs captured). Treat as append-only test history. |
| `notes to pick up for April 16.md` | Work-in-progress notes. Roll into `gap-report.md` and delete once resolved. |
| `.claude/` | Claude Code workspace settings for this repo. |

---

## 4. Catalog of skills

All 17 skills live under `skills/`, are declared in `marketplace.json`, and all `name:` fields match the directory name.

### Apache-2.0 example skills (13)

| Skill | One-line purpose | Ships |
|---|---|---|
| `algorithmic-art` | Generative art using p5.js with seeded randomness. | templates/ |
| `brand-guidelines` | Applies Anthropic's brand colors and typography to artifacts. | SKILL.md only |
| `canvas-design` | Produces .png / .pdf static designs, posters, art. | canvas-fonts/ |
| `claude-api` | Building / debugging / optimizing Claude API + SDK apps. | per-language docs (python, typescript, java, go, ruby, csharp, php, curl, shared) |
| `doc-coauthoring` | Structured workflow for co-authoring docs, proposals, specs. | SKILL.md only |
| `frontend-design` | Production-grade frontend UI (React, Tailwind, shadcn/ui). | SKILL.md only |
| `internal-comms` | Company-style internal communications (updates, newsletters, FAQs, incident reports). | examples/ |
| `mcp-builder` | Authoring high-quality MCP servers (Python FastMCP or Node SDK). | reference/, scripts/ |
| `skill-creator` | Meta-skill — creating, editing, and evaluating other skills. | agents/, assets/, eval-viewer/, references/, scripts/ |
| `slack-gif-creator` | Animated GIFs sized and tuned for Slack. | core/, requirements.txt |
| `theme-factory` | Applies one of 10 preset themes to slides/docs/HTML. | theme-showcase.pdf, themes/ |
| `web-artifacts-builder` | Complex multi-component claude.ai HTML artifacts. | scripts/ |
| `webapp-testing` | Playwright-driven testing of local web apps. | scripts/, examples/ |

### Source-available document skills (4)

These power Claude's production document capabilities. They are **proprietary / source-available** — not Apache-2.0 — and must not be redistributed as open source.

| Skill | One-line purpose | Ships |
|---|---|---|
| `docx` | Creating, reading, editing, manipulating Word documents. | scripts/ |
| `pdf` | Reading, extracting, merging, splitting, filling, OCR'ing PDFs. | scripts/ |
| `pptx` | Creating and editing PowerPoint decks. | scripts/, editing.md, pptxgenjs.md |
| `xlsx` | Creating and editing Excel/CSV/TSV spreadsheets. | scripts/ |

---

## 5. NextDecade document pipeline

This is the company-specific layer built on top of the skills. It turns a JSON input into a fully brand-compliant Word / PowerPoint / Excel file. Two deployment modes:

- **Claude.ai Projects (web, no-code)** — upload the `NextDecade-Claude-Project/` bundle into a Claude Project and chat. Claude drafts content on-brand but does not run scripts. Good for "I need a procedure on X" ad hoc drafting.
- **Claude Code (CLI/desktop, fully automated)** — run `render_docx.py` / `render_pptx.py` on a JSON input and get a `.docx` / `.pptx` out. Good for repeatable, CI-friendly document generation.

### 5.1 `NextDecade-Claude-Project/` (the drop-in bundle)

Follow `NextDecade-Claude-Project/START-HERE.md` step-by-step. Summary:

| Subfolder | Contents | Role |
|---|---|---|
| `01-brand-references/` | Brand & Style Guidelines 2024 PDF, Writing Style Guide & Resources 2024 PDF. | Canonical colors, fonts, voice. Pair with `extracted-specs.md` + `gap-report.md`. |
| `02-templates/` | Jinja-tagged DOCX templates (Procedure Rev 1, Standard, Guidance), the PowerPoint master (Oct 2025, brand-corrected), the HSSE Flash template, JSON schemas, a `README.md`. | Production templates Claude uses when drafting. |
| `03-original-templates/` | Un-tagged source Word/PowerPoint files. | Editable in Word if structure needs to change. Re-lint after edits. |
| `04-scripts/` | `render_docx.py`, `render_pptx.py`, `extract_docx.py`, `lint_docx_template.py`, `lint_pptx_master.py`, `README.md`. | Only used in Claude Code mode. |
| `05-samples/` | Complete Hot Work example set: Procedure + Standard + Guidance (docx + pdf), Safety Moment deck (pptx + pdf), All-Hands Email, Permit Tracker, `input-example.json`. | Few-shot examples for Claude. |
| `CLAUDE-INSTRUCTIONS.md` | Custom-instructions text you paste into the Claude Project settings. | Encodes brand identity, voice registers, document structures. |
| `START-HERE.md` | The 3-step setup guide for a new user. | Read first. |
| `PROJECT-SELFTEST.md` | Checks that confirm the bundle is wired correctly. | Run after upload. |

### 5.2 Render pipeline (Claude Code mode)

Entry points under `NextDecade-Claude-Project/04-scripts/` (duplicated under `skills/docx/scripts/` and `skills/pptx/scripts/` for skill-marketplace use):

| Script | Input | Output | Notes |
|---|---|---|---|
| `render_docx.py procedure\|standard\|guidance input.json output.docx [--pdf]` | JSON matching the matching `*_schema.json` | `.docx` (and optional `.pdf`) | Pipeline: lint → `docxtpl` fast path → walk-and-replace fallback. |
| `render_pptx.py input.json output.pptx` | JSON | `.pptx` | Uses the Oct 2025 PowerPoint master. |
| `extract_docx.py source.docx` | `.docx` (existing NextDecade doc) | JSON dict | Converts an existing doc back into the render-pipeline input shape. |
| `lint_docx_template.py template.docx schema.json` | Jinja-tagged template | Exit 0 / 2 / 3 | 0 = clean, 2 = warnings (still renders), 3 = errors (falls back). Run after every Word edit to a Jinja template. |
| `lint_pptx_master.py master.potx` | PowerPoint master | Exit 0 / 1 | Check slide-layout integrity. |
| `build_procedure_jinja.py` | `.docx` | Jinja-tagged `.docx` | One-time: converts an un-tagged procedure into a render-ready template. |

Install deps: `pip install -r requirements.txt`. Then drop JSON into `test-inputs/` and run the commands in `test-inputs/README.md`.

### 5.3 Validation sets

- `samples/document-types-validation/` — breadth sweep. **One of every document type** (governance DOCX × 3, business DOCX × 5, PPTX × 3, XLSX × 2, internal-comms × 2) so every render path is exercised head-to-head against the extracted specs. See `samples/document-types-validation/README.md` for the full index.
- `NextDecade-Claude-Project/05-samples/` — depth sweep on one subject (Hot Work). Complete example set that teaches Claude "what good looks like" for one topic.

### 5.4 Specs & gap tracking

- `extracted-specs.md` — machine-readable NDLNG brand + governance specifications distilled from the two brand PDFs. Claude reads this directly; humans use it to reason about which rule a given render must satisfy.
- `gap-report.md` — known gaps between templates and spec. Update as each gap is closed. Track the Aptos-vs-Segoe-UI theme inconsistency, the three unreached governance templates, and anything else flagged during smoke runs.
- `SMOKE-TEST-FINDINGS.md` — append-only log, currently 29 smoke-test runs deep. Any new finding goes here first; resolved findings roll into `gap-report.md`.

### 5.5 Running the smoke test

```bash
./smoke-test-enterprise.sh
```

Large (~74 KB) executable that exercises the render pipeline end-to-end against the fixture set. Read the top of the script before running in a shared environment — it touches real files under `samples/` and `test-inputs/`.

---

## 6. Guardrails

### Repo-wide

- **Upstream disclaimer (inherited):** from `README.md` — "These skills are provided for demonstration and educational purposes only… Always test skills thoroughly in your own environment before relying on them for critical tasks." Treat this as our floor, not our ceiling.
- **License split is not cosmetic.** The four document skills are source-available. Do not bundle them into an externally distributed marketplace without legal sign-off. All others are Apache-2.0.
- **Third-party obligations** in `THIRD_PARTY_NOTICES.md` travel with the document skills. Preserve the notices if you ship them.

### Per-skill guardrails

The skill bodies already encode their own rules. A few patterns to know:

- **`algorithmic-art` / `canvas-design`** — both explicitly instruct Claude to create original work and not copy existing artists to avoid copyright issues.
- **`claude-api`** — the only skill that fully models the `TRIGGER when: … DO NOT TRIGGER when: …` description pattern. Use it as the reference example for new skills.
- **`skill-creator`** — has its own evaluation loop (`eval-viewer/`, `scripts/run_eval.py`). Run new skills through it before merging.
- **`webapp-testing`** — runs Playwright. Keep it pointed at local / staging endpoints.
- **`slack-gif-creator`** — evaluate whether this belongs in the enterprise cut at all (see rollout checklist).

### SKILL.md authoring rules

Every skill we ship must:

1. Have a `SKILL.md` whose YAML `name:` matches its directory name.
2. Declare `description:` with enough context for Claude to fire the skill accurately. New skills should use explicit `TRIGGER when: …` / `DO NOT TRIGGER when: …` clauses (see `skills/claude-api/SKILL.md:3`).
3. Declare `license:` — `Complete terms in LICENSE.txt` for Apache-2.0 skills, `Proprietary. LICENSE.txt has complete terms` for source-available skills.
4. Ship a `LICENSE.txt` beside the SKILL.md.
5. Appear in `.claude-plugin/marketplace.json` under the right plugin block.

### Upstream sync guardrail

Do **not** edit the bodies of upstream skills. When you need different behaviour, fork the skill into a new directory (e.g. `skills/internal-comms-acme/`) and register the fork in `marketplace.json`. This keeps future Anthropic pulls clean.

---

## 7. Gaps before rollout

Eight items require a company-specific decision before enterprise deployment. None require code changes — they are policy or metadata.

1. **Ownership.** Add `CODEOWNERS` at the repo root. Decide who reviews new skills vs. upstream syncs.
2. **PR template.** Add `.github/pull_request_template.md` with checkboxes for the authoring rules in §5.
3. **Marketplace metadata.** `.claude-plugin/marketplace.json` still declares `name: anthropic-agent-skills` and `owner: Keith Lazuka <klazuka@anthropic.com>`. Rename to the company's bundle name and owner before publishing internally.
4. **Upstream sync policy.** Pick a cadence (monthly? on-demand?) and an owner for running `git fetch upstream && git merge upstream/main`. Document the exclusions: our Enterprise section of `README.md`, this file, and any company-forked skills.
5. **Marketplace publishing.** Decide whether Claude users run `/plugin marketplace add <our-internal-URL>` or whether we ship skills via a different channel. Configure auth accordingly.
6. **License posture.** Confirm with legal that mixing Apache-2.0 and source-available skills in one marketplace is acceptable for our distribution model (internal only? partner-facing?).
7. **Skill cut.** Audit the 17 skills for enterprise fit. `slack-gif-creator` is the obvious candidate for removal; `brand-guidelines` currently encodes Anthropic brand and should either be replaced with our own or retitled.
8. **Documentation standard adoption.** If this repo is going to set the Markdown standard for the whole company, announce it. The rules in §5 + the template in `template/SKILL.md` become the canon. Point teams at them.

---

## 8. What "good" looks like for a company SKILL.md

Use this as a one-page style guide.

- **Frontmatter:** `name`, `description`, `license` required. `allowed-tools` optional. Nothing else.
- **Description style for new skills:**
  `Short summary sentence. TRIGGER when: <explicit phrases/files/imports>. DO NOT TRIGGER when: <adjacent cases to skip>.`
  Keep it a single YAML string. Quote it if it contains a colon.
- **Length budget:** aim under 400 lines. If you need more, push long reference material into a sibling `references/` folder and link to it. `skill-creator` at 486 lines is at the upper bound.
- **Section order:** When to use → How it works → Examples → Guardrails → Supporting files. The upgraded `template/SKILL.md` models this exactly. Upstream Anthropic skills sometimes use different headings (e.g. `brand-guidelines` uses `Overview / Features`). That's fine for inherited content; **new** skills should follow the template.
- **Supporting files:** keep `scripts/`, `references/`, `assets/`, `examples/`, `templates/` — the names the existing skills already use. Reference them by relative path from SKILL.md.
- **Tone:** imperative ("Read the file", "Ask the user"). No hedging. The skill is instructions to Claude, not prose for humans.

---

## Appendix: Audit + fix record

Conducted on branch `claude/audit-and-document-NqUn5`. All findings from two audit passes (initial + re-audit).

| # | Issue | Severity | Fix | Commit |
|---|---|---|---|---|
| 1 | `skills/doc-coauthoring/` missing `LICENSE.txt` and `license:` frontmatter | Medium | Copied Apache-2.0 LICENSE.txt from skill-creator; added `license:` field | `88ad9ed` |
| 2 | `skills/skill-creator/SKILL.md` missing `license:` frontmatter | Low | Added `license: Complete terms in LICENSE.txt` | `88ad9ed` |
| 3 | License phrasing inconsistent across skills | Low | Kept both forms — the difference is semantic (Apache-2.0 vs source-available). Documented the rule in §5. | — |
| 4 | `.claude-plugin/marketplace.json:44` had orphan comma on its own line | Cosmetic | Reformatted | `a4e10b7` |
| 5 | `README.md` referenced non-existent `template-skill` | Cosmetic | Pointed to `./template` | `1f76335` |
| 6 | `template/SKILL.md` was a 6-line stub | Gap | Replaced with full enterprise template | `1f76335` |
| 7 | `README.md` had no enterprise framing | Gap | Prepended Enterprise Use section; preserved upstream content below | `1f76335` |
| 8 | Branch had zero divergence from main | Information | Audit fixes now provide the divergence | — |
| 9 | README contradicted itself on required frontmatter field count (2 vs 3) | P0 | Reconciled: 2 is the upstream minimum; 3 is the enterprise standard | `1df51f0` |
| 10 | TRIGGER/DO NOT TRIGGER mandate was too strict (only claude-api follows it) | P0 | Softened to "new skills should"; upstream skills exempted | `1df51f0` |
| 11 | `ENTERPRISE_OVERVIEW.md` referenced by README but did not exist | P0 | This file | pending commit |
| 12 | `CODEOWNERS`, PR template, sync cadence, marketplace metadata, license posture, skill cut, adoption announcement | P0–P1 | **Not code changes** — tracked in [Gaps before rollout](#gaps-before-rollout) for your decision | — |

### Non-issues (verified clean)

- No merge conflict markers, no `.orig` / `.rej` / `.bak` files, no TODO / FIXME / XXX / HACK anywhere.
- All 17 skills have valid YAML frontmatter with matching directory names.
- All referenced supporting files (scripts/, references/, assets/, examples/, templates/, core/, themes/) exist.
- `marketplace.json` parses as valid JSON and remains 1:1 with disk.
