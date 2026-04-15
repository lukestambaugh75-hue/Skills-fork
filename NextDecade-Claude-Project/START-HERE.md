# NextDecade Claude Project Bundle — Start Here

This folder has everything you need to upload to a Claude Project so Claude can draft NextDecade procedures, standards, guidance, presentations, and internal comms that match brand, voice, and governance standards automatically.

## What to do (3 steps)

> **Prerequisite:** Claude Projects requires a Claude **Pro, Team, or Enterprise** plan. It is not available on the Free plan.

1. **Download the ZIP and unzip locally** — Claude web uploads individual files, not folders or ZIPs.
2. **Create a new Claude Project** at [claude.ai](https://claude.ai) → sidebar → **Projects** → **Create project**.
3. **Upload all the files individually** from the `01-brand-references/`, `02-templates/`, `03-original-templates/`, and `05-samples/` subfolders (drag-select the contents of each folder into the project's Add content dialog — the web UI does not accept a folder or ZIP as a unit). In the Project's *Custom instructions* box, paste the contents of `CLAUDE-INSTRUCTIONS.md`.

That's it. Claude now knows how to draft on-brand NextDecade content.

## What Claude can now do for you

- Draft a **Procedure, Standard, or Guidance document** that matches the governance structure and uses NextDecade fonts, colors, and tables correctly. The Procedure template is the current Rev 1 Blank (April 2026) format with Roles table, PPE section, Steps table, Definitions, Abbreviations, References, and Appendices.
- Produce a **PowerPoint safety moment or investor-style deck** using the Oct 2025 master, with the NextDecade tagline, Public Disclaimer forward-looking statements, and the right brand family (NextDecade / Rio Grande LNG / NEXT Carbon Solutions).
- Write an **internal all-hands email** in the casual NEXT-digest voice, or an **external press release** in the formal voice.
- Build a **branded spreadsheet tracker** with Segoe UI, navy headers, color-coded status cells, and the classification footer.
- Rewrite a draft you already have into NextDecade voice + format.

## Try these prompts after you upload

- *"Draft a Lockout/Tagout Procedure in the same Rev 1 Blank format as the Hot Work Procedure sample."*
- *"I need a safety moment deck about confined space entry — 4 slides, using the ND layouts."*
- *"Here's a rough email about benefits enrollment. Rewrite it in NEXT digest voice for all-hands."* (paste your draft)
- *"Create a Standard for MOC — model it on the Hot Work sample, keep the same section order, and fill the RACI and Approval tables."*
- *"Build me a weekly HSSE KPI tracker spreadsheet using the NextDecade brand chrome."*

## What's in each folder

| Folder | What's in it | Why it's there |
|---|---|---|
| `01-brand-references/` | Brand & Style Guidelines PDF, Writing Style Guide PDF, `extracted-specs.md` (Claude-readable distillation of brand specs), `gap-report.md` | So Claude knows the canonical colors, fonts, voice rules, and what's still missing |
| `02-templates/` | Jinja-tagged DOCX templates (Procedure — Rev 1; Standard and Guidance — legacy), the PowerPoint master (brand-corrected), HSSE Flash template, JSON schemas (procedure is v2.0.0), template `README.md` | These are the production templates Claude references when drafting |
| `03-original-templates/` | Un-tagged source versions | For editing in Word if you need to update structure, and for Claude to reference if asked |
| `04-scripts/` | Python scripts (`render_docx.py`, `render_pptx.py`, linters) | Only used if you're running **Claude Code** (the CLI/desktop app), not the web Project — for fully automated generation. See `04-scripts/README.md`. |
| `05-samples/` | Complete Hot Work example set: Procedure (.docx + .pdf), Standard (.docx + .pdf), Guidance (.docx + .pdf), Safety Moment deck (.pptx + .pdf), All-Hands Email (.docx), Permit Tracker (.xlsx), and a working `input-example.json` for the Procedure pipeline | Show Claude what "good" output looks like; use as few-shot examples |

## Key things to know if you're new to Claude

- **Claude Projects (claude.ai web)** = you upload files, Claude reads them, you chat. Claude can **reference** the uploaded templates and samples but doesn't **run scripts**. For "I need a procedure on X," Claude will produce a draft in chat that matches the template format. You copy into Word or download as DOCX from Claude's output.
- **Claude Code (desktop/CLI app)** = you can also run the Python scripts under `04-scripts/` to generate DOCX/PDF files directly from a JSON input. More automation, steeper learning curve. Start with the web Project first.
- **Templates in Word** — the Jinja templates (files named `*(Jinja).docx`) have markers like `{{ purpose_text }}` visible in them. Don't edit those markers in Word unless you're willing to re-lint. Edit the **original** templates in `03-original-templates/` if you want to change structure.
- **Redact sensitive content before uploading.** Claude Projects persist across chats. If your Hot Work sample had real names or real site details, strip them first.
- **Brand colors Claude will use**:
  - Primary navy `#002060` / RGB 0, 32, 96
  - Primary orange `#FC7134` / RGB 252, 113, 52
  - Primary green `#00B050` / RGB 0, 176, 80 (NCS)
  - Font: Segoe UI everywhere
- **Classification footer** — Claude includes "Confidential and Proprietary – This document is intended solely for internal use…" on every document by default. Tell Claude if a specific piece is Public.
- **Forward-Looking Statements** — if you're making an external investor deck, tell Claude explicitly "include the FLS disclaimer slide" and it will use the verbatim boilerplate from the master template.

## Template status at a glance

| Template | Source | Schema version | Status |
|---|---|---|---|
| Procedure | NextDecade Blank Procedure Template (Rev 1, April 2026) | v2.0.0 | **Current** — use this format for all new procedures |
| Standard | Legacy Standard Template | v1.0.0 | Current (legacy structure still in use) |
| Guidance | Legacy Guidance Template | v1.0.0 | Current (legacy structure still in use) |
| PowerPoint Master | Final_Oct 2025 (brand-corrected orange) | n/a | Current |
| HSSE Flash | Template R5 | n/a | Current |

## Troubleshooting

- **Claude produces text that doesn't match the template format?** — Remind it: *"Use the exact section order and table structure from the Procedure Template (Rev 1) in the templates folder. Refer to the Hot Work sample as the format."*
- **Wrong voice / tone?** — Tell Claude which register: *"Formal external voice — no contractions, spell out 'Rio Grande LNG', use 'NextDecade employees'."*
- **Missing a document type (press release, fact sheet, etc.)?** — Check `gap-report.md` — we only tagged the three governance templates (Procedure, Standard, Guidance) so far. For other doc types, Claude will draft from scratch following the Writing Style Guide.
- **Stuck?** — Ask Claude: *"Based on the files in this project, what's the right template for a [your doc type]?"*

## Updating this bundle later

When NextDecade brand standards change (new logo, new color, new tagline), re-upload the updated files into your Claude Project. The three Jinja templates and the PPTX master are the most important to keep current.

Questions or to update this bundle: contact the Corporate Communications team.
