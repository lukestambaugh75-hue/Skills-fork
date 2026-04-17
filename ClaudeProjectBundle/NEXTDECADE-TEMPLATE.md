# NextDecade LNG Enterprise Skills Template

This repository is a fork of Anthropic's public skills repo, customized for NextDecade LNG use. Its purpose is to teach Claude how to produce on-brand, on-voice, correctly-classified, legally-compliant NextDecade content by default for Word documents, PowerPoint decks, Excel reports, internal and external communications, regulatory filings, investor material, HSE content, and ESG disclosures.

## How the repo is organized

| Path | What's there | Who uses it |
|---|---|---|
| `NextDecade-Claude-Project/` | Self-contained bundle for Claude Projects — brand PDFs, Jinja-tagged templates, original templates, render scripts, Hot Work sample set, and `START-HERE.md` / `CLAUDE-INSTRUCTIONS.md` / `PROJECT-SELFTEST.md`. | Upload these files into a Claude Project on claude.ai to draft NextDecade documents via chat. |
| `extracted-specs.md` | Claude-readable distillation of NextDecade brand specs (colors, fonts, voice, classification, boilerplate). | Upload alongside the bundle; referenced by the validation samples. |
| `gap-report.md` | What's still missing from the brand / governance extract. | Upload alongside the bundle. |
| `skills/` | The skill set Claude Code loads — `docx`, `pptx`, `xlsx`, `pdf`, plus supporting skills. The `docx` and `pptx` skills are wired to the bundle's templates and master. | Claude Code users and the Claude API. |
| `samples/document-types-validation/` | One sample per major NextDecade artifact type, with `_build/` scripts and `_inputs/` JSONs — breadth sweep for validating the skill set. | Reference output for regression / QA. |

## Two ways to use this repo

### A. Claude Projects (web, no code)

Upload the contents of `NextDecade-Claude-Project/` plus the two root-level spec files into a Claude Project. Follow `NextDecade-Claude-Project/START-HERE.md`. Claude drafts procedures, standards, guidance, decks, emails, and trackers in chat; you download the output.

### B. Claude Code / Claude API (automated generation)

Use the skills in `skills/` directly. The `docx` and `pptx` skills render governance documents and branded decks from structured JSON input via docxtpl and python-pptx. Templates live in `NextDecade-Claude-Project/02-templates/` (Jinja-tagged) and `03-original-templates/` (untagged source); the render scripts under `skills/docx/scripts/` and `skills/pptx/scripts/` point at those paths.

## Brand standards baked in

- Primary navy `#002060`, primary orange `#FC7134`, primary green `#00B050` (NCS)
- Segoe UI throughout
- Classification footer defaults to Confidential/Proprietary
- Forward-Looking Statements boilerplate available from the PPTX master's Public Disclaimer layout
- Three-brand family: NextDecade / Rio Grande LNG / NEXT Carbon Solutions

## Updating the bundle

When brand standards change (new logo, new color, new tagline), update the authoritative files in place:
- Templates in `NextDecade-Claude-Project/02-templates/` and `03-original-templates/`
- Brand PDFs in `NextDecade-Claude-Project/01-brand-references/`
- Specs in `extracted-specs.md` and `gap-report.md`

Re-run `skills/docx/scripts/build_procedure_jinja.py` if the source Procedure template changes, and `skills/pptx/scripts/lint_pptx_master.py` after any edit to the .potx master.

## Upstream origin

Fork of `anthropics/skills`. Mechanical skills (`docx`, `pptx`, `xlsx`, `pdf`) are kept with NDLNG defaults baked in. Generic creative skills from upstream may be pruned as the library matures.
