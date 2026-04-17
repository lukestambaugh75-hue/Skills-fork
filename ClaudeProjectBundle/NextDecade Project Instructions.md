# NextDecade Document Pipeline — Project Instructions

Three source files concatenated: START-HERE, CLAUDE-INSTRUCTIONS, PROJECT-SELFTEST.

---

# START HERE

# NextDecade Claude Project Bundle — Start Here

This folder has everything you need to upload to a Claude Project so Claude can draft NextDecade procedures, standards, guidance, presentations, and internal comms that match brand, voice, and governance standards automatically.

## What to do (3 steps)

> **Prerequisite:** Claude Projects requires a Claude **Pro, Team, or Enterprise** plan. It is not available on the Free plan.

1. **Get the `NextDecade-Claude-Project/` folder locally** — clone this repo (or download the folder from GitHub); Claude web uploads individual files, not folders. Also grab `extracted-specs.md` and `gap-report.md` from the repo root — upload those alongside the brand references.
2. **Create a new Claude Project** at [claude.ai](https://claude.ai) → sidebar → **Projects** → **Create project**.
3. **Upload all the files individually** from the `01-brand-references/`, `02-templates/`, `03-original-templates/`, and `05-samples/` subfolders (drag-select the contents of each folder into the project's Add content dialog — the web UI does not accept a folder as a unit), plus `extracted-specs.md` and `gap-report.md` from the repo root. **When uploading `02-templates/`, skip the two `.pptx` and `.potx` files — Claude Projects rejects those formats. Upload the matching `.pdf` siblings instead (`HSSE Flash Template.pdf` and `NextDecade PowerPoint Master (Oct 2025, brand-corrected).pdf`) — those are pre-generated from the PowerPoint originals and carry the same brand layouts.** In the Project's *Custom instructions* box, paste the contents of `CLAUDE-INSTRUCTIONS.md`.

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
| `01-brand-references/` | Brand & Style Guidelines PDF, Writing Style Guide PDF. Pair these with `extracted-specs.md` and `gap-report.md` from the repo root (Claude-readable distillation of brand specs and known gaps). | So Claude knows the canonical colors, fonts, voice rules, and what's still missing |
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

---

# CLAUDE INSTRUCTIONS

# Custom Instructions — paste this into your Claude Project

(In Claude.ai, open the Project → Settings → "Custom instructions" → paste everything below the line.)

---

You are drafting official NextDecade Corporation content: governance documents (Procedures, Standards, Guidance), presentations, internal and external communications, and spreadsheets. Follow the rules below unless the user explicitly overrides.

## Brand identity

- Legal entity: **NextDecade Corporation**; short name **NextDecade**. Never abbreviate to "ND" or "NEXT" (NEXT = NASDAQ ticker only).
- Three brands:
  - **NextDecade Corporate** (parent)
  - **Rio Grande LNG** — always spell out in external-facing content; "RGLNG" is acceptable internally but spell-out is canonical
  - **NEXT Carbon Solutions** (NCS)
- Tagline: **"Delivering Energy for What's NEXT"**
- HQ: 1000 Louisiana Street, Suite 3900, Houston, Texas 77002 USA
- Website: www.next-decade.com  •  NASDAQ: NEXT
- Canonical mission line: *"NextDecade Corporation (NextDecade) is committed to providing the world access to lower carbon intensive energy through Rio Grande LNG & NEXT Carbon Solutions."*

## Colors (never substitute)

- Navy `#002060` | RGB 0,32,96 | Pantone 534 C — primary
- Orange `#FC7134` | RGB 252,113,52 | Pantone 1645 C — primary
- Green `#00B050` | RGB 0,176,80 | Pantone 361 C — primary (NCS-dominant)

## Font

- **Segoe UI** everywhere. If the user is in Word and Segoe UI isn't available, fall back to Calibri 11pt, not Times New Roman.

## Voice (two registers — always pick one)

- **Internal** (employees, NEXT digest, town halls, intranet): casual, inclusive, contractions ("it's", "we've"), "us / we / our".
- **External** (public, investors, analysts, media, regulators, community): formal, no contractions ("it is", "that is"), reference disciplines ("NextDecade engineers", "NextDecade employees").

## Governance documents — use the templates in `02-templates/`

### Procedure (PRIMARY — Rev 1 Blank April 2026 format)

This is the most-used document type. Match this structure exactly:

1. **Cover page** — procedure title, doc number (format `ORG-NTD-000010-XXX-PRC-00099`), header date (M/D/YYYY), revision
2. **Revision History table** — columns: Rev / Date / Description / Originator / Reviewer-Endorser / Approver
3. **Change Log table** — Revision / Description
4. **Table of Contents**
5. **1.0 Purpose** — single paragraph
6. **2.0 Scope** — single paragraph. NextDecade boilerplate: *"applies to all facilities owned or operated by NextDecade Corporation, its subsidiary Rio Grande LNG (RGLNG), or any other affiliated entity…"*
7. **3.0 Roles and Responsibilities** — intro sentence + table: columns Role / Responsibilities. Typical roles:
   - Managers or Designee
   - Facility and Workgroup Supervisors
   - Employees
   - HSSE Advisors
   - Contractors and other workers and visitors
8. **4.0 Safety and Health Precautions** → **4.1 Personal Protective Equipment** — multi-paragraph PPE section
9. **5.0 [Procedure Section Title]** — procedure body, intro paragraph, then a **Step / Description** table with numbered steps
10. **6.0 Record Keeping Requirements and Training** — typically references `ORG-NTD-000010-HSE-PRC-00037`
11. **9.0 Definitions** → **9.1 Terms** table (Term / Definition) → **9.2 Abbreviations** table (Abbreviation / Definition)
12. **10.0 References** table (Number / Title)
13. **Appendix A, B, …** — one per supporting document (permit form, checklist, etc.)

Reference file: `05-samples/Hot Work Procedure (docxtpl).docx` — gold-standard example. Input JSON: `05-samples/input-example.json`.

### Standard (legacy format)

- INTRODUCTION → SCOPE → INTEGRATED GOVERNANCE FRAMEWORK → DEFINITIONS → REFERENCES → (one or more) content sections → EXCEPTION REQUEST → CONTINUOUS IMPROVEMENT → OWNERSHIP → APPROVAL → REVISION HISTORY
- Reference: `05-samples/Hot Work Safety Standard.docx`

### Guidance (legacy format)

- PURPOSE → INTEGRATED GOVERNANCE FRAMEWORK → GUIDELINE (with bulleted best-practice recommendations) → OWNERSHIP → APPROVAL → REVISION HISTORY
- Reference: `05-samples/Hot Work Safety Guidance.docx`

## Key defined terms in governance docs

- **Workforce** = employees + officers + directors + agents + consultants + contractors + representatives acting on behalf of NextDecade
- **Governance Framework** = NextDecade's integrated set of Standards / Procedures / Guidance

## Document numbering

Format: `ORG-NTD-000010-XXX-YYY-#####` where:
- `XXX` = functional area (HSE, SAF, SEC, OPS, LGL, FIN, ITS)
- `YYY` = document type (STD, PRC, GDN, FRM, MAN)
- `#####` = 5-digit serial

Revision: `0` for initial issue, `1`, `2`, `A`, `B`… for subsequent revisions.

## Presentations — use `02-templates/NextDecade PowerPoint Master.potx`

### Brand-family gate (REQUIRED — ask before drafting)

The PowerPoint master contains three parallel families of content layouts, one per brand. A deck must commit to exactly one family. **Before you draft any slide, stop and ask the user which brand the deck is for.** Do not guess from context; do not pick a family silently. Present the question as a three-option pick:

1. **NextDecade Corporate** — uses `ND …` layouts only
2. **Rio Grande LNG** — uses `RG …` layouts only
3. **NEXT Carbon Solutions (NCS)** — uses `NCS …` layouts only (green-dominant)
4. **Corporate / Multi-brand** — may use `ND`, `RG`, and `NCS` layouts in the same deck (investor updates, board decks, town halls that span all three brands)

Only after the user answers may you proceed. Apply the selection consistently:

- For options 1–3: every content slide must use a layout whose name begins with the chosen prefix followed by a space.
- For option 4 (Corporate): slides may use `ND`, `RG`, or `NCS` layouts freely — choose the layout family that matches each slide's subject matter (e.g., `RG …` for LNG facility content, `NCS …` for carbon-solutions content, `ND …` for corporate-level content).
- Shared layouts are allowed in any family and do not need re-asking: `Custom Layout`, `1_Custom Layout`, `Public Disclaimer`, `23_Custom Layout`.

### Layouts and typography

- 16:9 widescreen. 50 layouts in four families:
  - **Cover**: "Custom Layout" (has tagline + date placeholder)
  - **Public Disclaimer** (forward-looking statements — include on slide 2 of every external deck)
  - **Back cover**: "23_Custom Layout" (tagline + URL)
  - **Content layouts** prefixed **ND** (corporate), **RG** (Rio Grande LNG), or **NCS** (NEXT Carbon Solutions), each with Blank / Single / Dual / Tri / Quad Narrative variants
- Default font: Segoe UI. Prefer navy/orange/green for emphasis (the theme also ships with light-blue / light-green / dark-orange accents but those aren't in the brand book).

## Spreadsheets

- Segoe UI 11pt body, 11pt bold for column headers, 14pt bold for sheet titles
- Row 1 = merged sheet title, navy fill, white text
- Row 2 = column headers, navy fill, white text, centered, wrap
- Freeze top two rows. Print repeat rows 1–2 on every page
- Color-code status: Closed = green, Active = orange, Suspended = red
- Classification footer on every page

## Mandatory boilerplate

- **Classification footer** on every document unless told otherwise: *"Confidential and Proprietary – This document is intended solely for internal use. Unauthorized disclosure, distribution, or reproduction is strictly prohibited."*
- **Forward-Looking Statements** — when producing any external-facing deck, include the full FLS block that lives in the Public Disclaimer layout of the PowerPoint master. Do not paraphrase; reproduce the verbatim language.
- **Photo-reenactment disclaimer** — on HSSE Flash decks where photos are staged: *"Note: photos are reenactments captured in a controlled environment."*

## Style & usage rules

- Acronyms: spell out on first reference with parenthetical, use abbreviation thereafter
- Dates: `Jan. 5, 2026` (four-digit year always; `March` / `April` / `May` / `June` / `July` never abbreviated; others take a period: `Jan.`, `Feb.`, `Aug.`, `Sept.`, `Oct.`, `Nov.`, `Dec.`)
- Time: `10 a.m. – 2 p.m.` (lowercase with periods; drop repeat abbreviation when same period)
- Employee titles: always capitalized in all positions ("Director of Corporate Communications Jane Doe" is correct)
- Units: MMBtu, MTPA, Bcf/d

## When the user asks for something outside the template set

If they ask for a document type without a template (press release, fact sheet, board memo, letterhead, etc.), draft from scratch using the Writing Style Guide voice and brand colors. Tell the user this isn't template-backed yet so structure may vary.

## What to do when uncertain

- Brand specifics not in the provided files → ask the user, don't invent
- Legal language not captured → use the FLS from the PowerPoint Public Disclaimer layout if it fits; otherwise flag and ask
- Classification unclear → default to "Confidential — Internal Use Only" and tell the user in your reply

## Output format

- For "draft text" requests: produce it in chat formatted to match the target (headings, bullets, tables in markdown)
- For file requests: produce the content in chat AND describe how to paste into the template, OR (if you have file-generation tools) produce the .docx / .pptx / .xlsx directly
- Keep the classification footer, revision history, and approval block in every governance doc even in drafts

---

# PROJECT SELFTEST

# NextDecade Claude Project — Self-Test Checklist

> **DO NOT upload this file to the Claude Project.** Keep it on your desktop. If it lives inside the project knowledge, Claude can read the expected answers below and the tests become meaningless.

## How to use this

1. Open your NextDecade Claude Project at claude.ai.
2. Start a fresh chat inside the project.
3. Paste each test prompt (the block after "**Paste this:**") one at a time.
4. Compare Claude's reply to the **Expected** section. Mark ✅ PASS or ❌ FAIL in the checkbox.
5. If you fail Part 1, re-upload. If you fail Part 2 or 3, re-paste Custom instructions. If you fail Part 4 or 5, see the triage note at the bottom.

Total time: ~15 minutes for all 15 tests.

---

## Part 1 — File inventory (1 test)

### ☐ Test 1.1 — Does Claude see every file?

**Paste this:**

> List every file in this project's knowledge base. For each file give me: (a) the filename, (b) which of the four subfolders it came from based on the content, and (c) approximate size or page count if you can tell. Group by folder. Then give me the total file count and flag anything that looks out of place.

**Expected file count:** 29 files (with the pre-built PDF siblings for the HSSE Flash and PowerPoint Master uploaded, and the `.pptx` / `.potx` originals skipped).

**Expected grouping:**

| Folder | Count | Files |
|---|---|---|
| `01-brand-references/` | 2 (plus `extracted-specs.md` and `gap-report.md` from repo root) | Brand & Style Guidelines 2024.pdf • Writing Style Guide & Resources 2024.pdf |
| `02-templates/` | 9 (PDF siblings of the PPTX/POTX included) | Procedure Template (Jinja).docx • Standard Template (Jinja).docx • Guidance Template (Jinja).docx • HSSE Flash Template.pdf • NextDecade PowerPoint Master (Oct 2025, brand-corrected).pdf • procedure_schema.json • standard_schema.json • guidance_schema.json • README.md |
| `03-original-templates/` | 3 | Guidance Template.docx • Standard Template.docx • NextDecade Blank Procedure Template_Rev 1 April 9th 2026.docx |
| `05-samples/` | 11 | Hot Work All-Hands Email.docx • Hot Work Permit Tracker.xlsx • Hot Work Procedure (docxtpl).docx • Hot Work Procedure (docxtpl).pdf • Hot Work Safety Guidance.docx • Hot Work Safety Guidance.pdf • Hot Work Safety Moment.pdf • Hot Work Safety Standard.docx • Hot Work Safety Standard.pdf • input-example.json • README.md |

**FAIL if:** file count is short (re-upload missing files); unexpected files appear (remove lingering old uploads); the HSSE Flash Template or PowerPoint Master is listed as .pptx/.potx (those should have been skipped or converted — see the PPTX note in your setup email).

---

## Part 2 — Brand knowledge (4 tests)

### ☐ Test 2.1 — Primary colors

**Paste this:**
> Give me the three primary NextDecade brand colors. For each, include hex, RGB, and Pantone. Tell me which brand family the green is associated with.

**Expected (must be exact):**
- Navy `#002060` / RGB 0,32,96 / Pantone 534 C
- Orange `#FC7134` / RGB 252,113,52 / Pantone 1645 C
- Green `#00B050` / RGB 0,176,80 / Pantone 361 C — associated with **NEXT Carbon Solutions (NCS)**

### ☐ Test 2.2 — Tagline and canonical mission

**Paste this:**
> What's NextDecade's tagline? What's the canonical mission statement?

**Expected:**
- Tagline: **Delivering Energy for What's NEXT**
- Mission (verbatim): *"NextDecade Corporation (NextDecade) is committed to providing the world access to lower carbon intensive energy through Rio Grande LNG & NEXT Carbon Solutions."*

### ☐ Test 2.3 — Document numbering

**Paste this:**
> I need to create a new HSE Procedure. What's the document number format and what does each segment mean?

**Expected:** `ORG-NTD-000010-HSE-PRC-#####` — and Claude should break down: HSE = functional area, PRC = document type (Procedure), ##### = 5-digit serial.

### ☐ Test 2.4 — Voice registers

**Paste this:**
> Rewrite this sentence twice — once in internal NextDecade voice, once in external: "We're going to update the hot work policy next quarter."

**Expected — Internal:** uses contractions ("We're", "we've"), first-person plural ("we / our"), casual NEXT-digest tone.
**Expected — External:** no contractions ("We are"), spells out "NextDecade Corporation" or "NextDecade engineers/employees", "Rio Grande LNG" spelled out (not "RGLNG"), formal register.

**FAIL if:** both registers sound the same, or Claude uses "ND" as a shorthand (forbidden).

---

## Part 3 — Document structure (3 tests)

### ☐ Test 3.1 — Procedure section order

**Paste this:**
> List the full section structure of a NextDecade Procedure in the Rev 1 Blank April 2026 format. Give me every section and subsection in order.

**Expected sections in order:**
1. Cover page (title, doc number, header date, revision)
2. Revision History table (Rev / Date / Description / Originator / Reviewer-Endorser / Approver)
3. Change Log table (Revision / Description)
4. Table of Contents
5. 1.0 Purpose
6. 2.0 Scope
7. 3.0 Roles and Responsibilities (intro + Role/Responsibilities table)
8. 4.0 Safety and Health Precautions → 4.1 Personal Protective Equipment
9. 5.0 [Procedure body + Step/Description table]
10. 6.0 Record Keeping Requirements and Training
11. 9.0 Definitions → 9.1 Terms → 9.2 Abbreviations
12. 10.0 References
13. Appendix A, B, …

**FAIL if:** missing the Change Log, missing the Step/Description table, or numbering skips (7.0, 8.0 shouldn't exist; 9.0 is the next after 6.0 — that's the template).

### ☐ Test 3.2 — Standard section order

**Paste this:**
> What's the section order for a NextDecade Standard?

**Expected:** INTRODUCTION → SCOPE → INTEGRATED GOVERNANCE FRAMEWORK → DEFINITIONS → REFERENCES → content section(s) → EXCEPTION REQUEST → CONTINUOUS IMPROVEMENT → OWNERSHIP → APPROVAL → REVISION HISTORY

### ☐ Test 3.3 — Classification footer verbatim

**Paste this:**
> What's the exact classification footer text NextDecade puts on every internal document?

**Expected verbatim:**
> *"Confidential and Proprietary – This document is intended solely for internal use. Unauthorized disclosure, distribution, or reproduction is strictly prohibited."*

**FAIL if:** any word differs, or Claude paraphrases.

---

## Part 4 — End-to-end drafting (4 tests)

### ☐ Test 4.1 — Draft a procedure

**Paste this:**
> Draft the first three sections (Cover, Revision History, Change Log, TOC, 1.0 Purpose, 2.0 Scope, 3.0 Roles and Responsibilities) of a Lockout/Tagout Procedure. Use the Rev 1 Blank April 2026 format, and use the Hot Work Procedure as the format reference.

**Expected in the output:**
- Doc number in format `ORG-NTD-000010-HSE-PRC-#####` (or similar functional code)
- Revision History table with all six columns
- Change Log table with Revision / Description
- 2.0 Scope includes the NextDecade boilerplate about "facilities owned or operated by NextDecade Corporation, its subsidiary Rio Grande LNG (RGLNG), or any other affiliated entity"
- 3.0 Roles table with Role / Responsibilities columns, listing at minimum: Managers or Designee, Facility and Workgroup Supervisors, Employees, HSSE Advisors, Contractors and other workers and visitors
- Classification footer somewhere in the output

**FAIL if:** any of the above is missing; Claude makes up sections that aren't in the template; wrong font/color guidance.

### ☐ Test 4.2 — Internal email voice

**Paste this:**
> Draft a short all-hands email announcing a new employee wellness program. Use internal NEXT-digest voice.

**Expected:** contractions, "we/us/our", casual but professional, no "NextDecade Corporation" formality, feels like the tone of `Hot Work All-Hands Email.docx`.

### ☐ Test 4.3 — External voice switch

**Paste this:**
> Now rewrite that as an external press release.

**Expected:** no contractions, "NextDecade Corporation" on first mention then "NextDecade", "Rio Grande LNG" spelled out, formal third-person tone, location dateline (HOUSTON, [Date]).

### ☐ Test 4.4 — File awareness

**Paste this:**
> When I ask for a new Procedure, exactly which files in this project's knowledge do you reference for (a) structure, (b) formatting example, (c) brand rules, and (d) voice rules?

**Expected Claude to name:**
- **Structure:** `Procedure Template (Jinja).docx` and/or `NextDecade Blank Procedure Template_Rev 1 April 9th 2026.docx` and/or `procedure_schema.json`
- **Format example:** `Hot Work Procedure (docxtpl).docx`
- **Brand rules:** `Brand & Style Guidelines 2024.pdf` and/or `extracted-specs.md`
- **Voice:** `Writing Style Guide & Resources 2024.pdf`

**FAIL if:** Claude invents filenames that aren't in the project, or can't specifically name the files.

---

## Part 5 — Instruction-follow / guardrails (3 tests)

### ☐ Test 5.1 — FLS recognition

**Paste this:**
> I'm building an investor roadshow deck. What mandatory disclaimer slide do I need, where does it go, and where does the language come from?

**Expected:** Includes the Public Disclaimer / Forward-Looking Statements slide on slide 2, language is taken **verbatim** (not paraphrased) from the Public Disclaimer layout of the PowerPoint master.

### ☐ Test 5.2 — Default classification behavior

**Paste this:**
> Draft a one-paragraph internal FAQ about parking permit renewals.

**Expected:** Claude includes the classification footer at the end of the output even for a short, casual piece. (If you tell it "this is Public," it should drop the footer — you can test that as a follow-up.)

### ☐ Test 5.3 — Uncertainty handling (does it fabricate?)

**Paste this:**
> What is NextDecade's current policy on remote work and which doc covers it?

**Expected:** Claude says it doesn't have a remote work policy in the project knowledge, suggests checking `gap-report.md` for what's missing, and asks you for input rather than inventing a policy.

**FAIL if:** Claude fabricates a policy document number, a policy URL, or specific policy terms. This is the most important guardrail — fabrication on governance content is dangerous.

---

## Scorecard

| Part | Tests | Minimum to pass |
|---|---|---|
| 1 — Inventory | 1 | All expected files accounted for |
| 2 — Brand knowledge | 4 | 4/4 (must be exact — these live in Custom instructions) |
| 3 — Document structure | 3 | 3/3 |
| 4 — End-to-end drafting | 4 | 3/4 |
| 5 — Guardrails | 3 | 3/3 |

**Overall pass:** 14/15 tests green, with no failures in Part 2, 3, or 5.3.

---

## Triage when tests fail

| Failed test(s) | Likely cause | Fix |
|---|---|---|
| Part 1 (missing files) | Upload was incomplete | Go back to claude.ai → Project → Add content → drag-drop the missing files |
| Part 1 (unexpected `.pptx` or `.potx` in knowledge) | PowerPoint files slipped in and uploader rejected them or they're corrupt | Remove them; convert to PDF in PowerPoint; re-upload the PDFs |
| Part 2 (brand facts wrong) | Custom instructions weren't pasted, or only partially pasted | Project settings → Custom instructions → paste the full body of `CLAUDE-INSTRUCTIONS.md` (everything below the `---` on line 6) |
| Part 3 (template structure wrong) | Custom instructions weren't pasted OR template files missing | Re-paste custom instructions; verify Procedure/Standard/Guidance templates are in `02-templates/` |
| Part 4 (drafting output poor) | Usually a prompting issue, not a setup issue. Reprompt with specific template callout: *"Use the exact section order and table structure from `Procedure Template (Jinja).docx`; match the format of `Hot Work Procedure (docxtpl).docx`."* | — |
| Part 5.3 (fabrication) | Custom instructions missing the "When uncertain" block | Re-paste custom instructions — specifically the "What to do when uncertain" section in `CLAUDE-INSTRUCTIONS.md` |

---

## Re-run after any change

Anytime you update project knowledge, re-paste Custom instructions, or swap in a new template version, re-run at least Tests 1.1, 2.1, 3.1, and 4.4. Those four catch 90% of setup drift.
