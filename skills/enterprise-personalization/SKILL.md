---
name: enterprise-personalization
description: Orchestrates the intake-to-template personalization workflow. Use this skill when the user says "personalize the repo," "extract from uploads," "run the gap analysis," "turn this into our template," or references the /uploads/ folder. This is the master workflow that reads every artifact in /uploads/, produces a structured specification, and rewrites every other skill in the repo to enforce NextDecade LNG standards. Also use for follow-on refreshes when new brand assets are added.
---

# Enterprise Personalization Workflow

## Purpose

Transform this generic skills repo into **the NextDecade LNG enterprise template library** by extracting specifications from `/uploads/` and propagating them into every skill.

This skill does not produce user-facing content. It produces **other skills** — it's a meta-skill that personalizes the repo.

## When to use

- User says "personalize the repo" / "run extraction" / "build our template from uploads"
- User signals that they've uploaded the first batch of assets
- User asks "what's missing" or "run the gap analysis"
- Periodic refresh: when new brand assets or style updates are added
- When onboarding a new acquisition or business unit whose materials need to be added

## When NOT to use

- When the user asks to produce a single artifact (a memo, a deck, an email) — use the individual skills for that
- When uploads folder is empty — ask the user to populate uploads first
- For one-off personalization of a single skill — just edit that skill directly

## Workflow — 7 phases

### Phase 1: Intake audit

1. Walk `/uploads/` recursively. For each numbered subfolder, inventory what's present vs. what the subfolder's README asked for.
2. Produce `/uploads/_inventory.md` with a table:

   | Folder | Priority | Files present | Priority items missing | Status |
   |--------|----------|---------------|------------------------|--------|
   | 01-brand | Required | brand-guide-2025.pdf, logos/ | Spanish tagline | Partial |

3. Flag "Required" folders that are empty — these block personalization of depending skills.

### Phase 2: Gap report

Before extracting anything, produce `/uploads/_gap-report.md` covering:

1. **Blocking gaps** — Required uploads that are missing. List which skills can't be personalized without them.
2. **Partial gaps** — Required folders with some material but missing key elements.
3. **Optional gaps** — Recommended folders that are empty and which skills will remain generic as a result.
4. **Proposed next-batch upload list** — prioritized, so the user knows exactly what to gather next.

Present the gap report to the user. Ask whether to:
- Proceed with extraction of what's available (and mark skills that depend on missing inputs)
- Wait for more uploads
- Accept specific gaps and use placeholders

### Phase 3: Extraction

For each upload, extract systematically. Store results in `/uploads/_extracted/` as structured markdown. One file per topic. Examples:

```
uploads/_extracted/
  colors.md                    # Every color with hex / RGB / CMYK / Pantone / usage
  typography.md                # Font families, weights, type scale, pairing rules
  voice.md                     # Voice attributes, tone guide, terminology
  terminology.md               # Approved / forbidden / preferred terms
  legal-blocks/                # Verbatim legal boilerplate
    forward-looking.md
    safe-harbor-slide.md
    reg-fd.md
    about-nextdecade.md
    copyright.md
    email-footer.md
  document-specs/              # Per-template specs
    letterhead.md
    memo.md
    report.md
    board-memo.md
  presentation-specs/
    investor-deck.md
    board-deck.md
    earnings-deck.md
  classification.md            # Taxonomy + visual treatment
  file-naming.md               # Convention
  imagery-inventory.md         # Catalog of approved images with usage rules
  chart-palette.md             # Data viz standards
  boilerplate-paragraphs.md    # "About NDLNG," etc.
```

**Extraction rules:**
- **Verbatim for legal**: Never paraphrase. Quote exactly.
- **Specific for visual**: Extract concrete numbers (hex, pt, DXA, EMU) not descriptions ("bluish" ❌ → `#005A8B` ✅).
- **Provenance-tagged**: Every spec line cites the source file (e.g., "Source: `uploads/01-brand/brand-guide-2025.pdf` p. 14").
- **Version-aware**: When multiple versions exist (e.g., several FLS paragraphs over time), keep the most recent as default and archive prior versions with dates.

### Phase 4: Specification review

Before rewriting any skill, present `/uploads/_extracted/` to the user for review. The user confirms:
- Colors are exact
- Fonts are correct
- Voice characterization matches their intent
- Legal language is the current approved version
- Classification defaults are appropriate

**Do not skip this step.** Errors in extracted specs propagate to 20+ skills. Confirming specs once is cheaper than diffing 20 skills.

### Phase 5: Skill personalization

Rewrite existing skills and create new ones according to this mapping:

#### Rewrite (replace Anthropic / generic content with NDLNG specifics)
| Skill | Source of truth |
|-------|-----------------|
| `brand-guidelines/` | 01-brand, 02-typography, 03-imagery |
| `docx/` | 04-document-templates + 07-sample-documents + 11-legal-boilerplate + 18-classification-rules |
| `pptx/` | 05-presentation-templates + 08-sample-presentations + 18-classification-rules |
| `xlsx/` | 06-spreadsheet-templates + 17-data-viz-charts |
| `internal-comms/` | 09-sample-communications + 10-style-voice-guide |
| `doc-coauthoring/` | 10-style-voice-guide + 04-document-templates |
| `pdf/` | 18-classification-rules (classification stamping) |

#### Create new (skills that don't exist yet)
| New skill | Source of truth |
|-----------|-----------------|
| `classification/` | 18-classification-rules |
| `legal-boilerplate/` | 11-legal-boilerplate |
| `file-naming/` | 19-file-naming |
| `regulatory-comms/` | 12-regulatory-samples |
| `investor-relations/` | 13-investor-relations + 11-legal-boilerplate |
| `safety-hse/` | 14-safety-hse |
| `community-stakeholder/` | 15-community-stakeholder |
| `esg-reporting/` | 16-esg-sustainability |
| `data-visualization/` | 17-data-viz-charts |
| `email-signatures/` | 20-org-signatures |
| `exec-bios/` | 20-org-signatures |
| `crisis-communications/` | 14-safety-hse (incident subset) + 11-legal-boilerplate |

#### Each skill rewrite follows this structure:
1. YAML frontmatter (`name`, `description` — keywords for discoverability)
2. "When to use" / "When NOT to use" at top
3. NDLNG specifications baked in — not placeholders
4. Pre-approved templates embedded or referenced from `/skills/<skill>/templates/`
5. Legal / classification defaults hard-coded
6. Links to source specs in `/uploads/_extracted/` so the audit trail is clear
7. Example output demonstrating correct usage

### Phase 6: Diff review

Produce `/uploads/_diff-report.md` listing:
- Every skill changed (before / after summary)
- Every new skill created
- Any placeholders that remain (because uploads didn't cover them)
- Any contradictions encountered (e.g., two sample docs use different heading fonts) — flagged for user decision

User reviews and approves before anything is committed.

### Phase 7: Smoke test

Before declaring personalization complete, generate one artifact of each major type and verify it's on-brand:

1. A 1-page board memo (tests `docx/` + classification + letterhead)
2. A 5-slide investor update (tests `pptx/` + safe harbor + IR voice)
3. A press release draft (tests `internal-comms/` + legal boilerplate)
4. A safety moment (tests `safety-hse/`)
5. A community announcement (tests `community-stakeholder/` + bilingual)
6. A financial report spreadsheet (tests `xlsx/` + data viz)

Compare each against the `/uploads/08-sample-*` reference artifacts. Flag visual or voice divergence for tuning.

## Outputs

This skill produces:
- `/uploads/_inventory.md` — what's uploaded
- `/uploads/_gap-report.md` — what's missing
- `/uploads/_extracted/` — structured specs pulled from uploads
- `/uploads/_diff-report.md` — what was changed in the repo
- Updated skills across `/skills/`
- New skills in `/skills/`
- `/PERSONALIZATION-LOG.md` at repo root — dated log of each personalization run

## Guardrails

- **Never commit without user approval** of the diff report. This repo will be distributed — changes need explicit sign-off.
- **Never invent brand specs.** If a color, font, or phrase isn't in uploads, flag it as a gap — don't guess from what's publicly visible (e.g., website scraping).
- **Never paraphrase legal language.** Always verbatim. If rewording seems necessary, escalate to user + legal.
- **Never overwrite uploads/** content — treat it as read-only source of truth.
- **Log every change.** The `PERSONALIZATION-LOG.md` is the audit trail for when a spec came from which upload on which date.

## Refresh workflow

When user adds new uploads or updates existing ones:

1. Re-run Phase 1 (inventory)
2. Diff against prior inventory — identify new or updated files
3. Re-extract only affected areas (e.g., new brand guide → re-run colors/typography/imagery extraction, skip voice if style guide unchanged)
4. Propose targeted skill updates only for affected skills
5. Seek user approval before committing
6. Log the refresh in `PERSONALIZATION-LOG.md`
