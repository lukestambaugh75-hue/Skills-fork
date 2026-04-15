# Document-type validation set

A single, coherent sample set that produces **one of every major NextDecade document type** so the user can review each artifact head-to-head against the extracted NDLNG specifications (see [`extracted-specs.md`](../../extracted-specs.md) and [`gap-report.md`](../../gap-report.md) at the repo root).

Scope: one sample of each artifact type that the personalized skills are expected to produce. This is **not** a topical set (the `safety-hot-work/` folder already does that, on a single subject). This set is a breadth sweep: different topics intentionally, so you can see whether each **document type** renders correctly regardless of subject matter.

## Quick index

| # | Artifact | Skill that produced it | Register | Classification |
|---|---|---|---|---|
| 1 | `01-governance-docx/Records Retention Standard.docx` | `docx` (standard) | Formal | Confidential |
| 2 | `01-governance-docx/Vendor Onboarding Procedure.docx` | `docx` (procedure) | Formal | Confidential |
| 3 | `01-governance-docx/Remote Work Guidance.docx` | `docx` (guidance) | Formal | Confidential |
| 4 | `02-business-docx/Q1 2026 Board Memo.docx` | `docx` + `doc-coauthoring` | Formal | Confidential |
| 5 | `02-business-docx/Press Release - Q1 2026 Construction Update.docx` | `internal-comms` + FLS from `pptx` | Formal external | Public (ready) |
| 6 | `02-business-docx/Rio Grande LNG Fact Sheet.docx` | `docx` + `brand-guidelines` | Formal external | Public |
| 7 | `02-business-docx/Operating Committee Minutes - 2026-04-10.docx` | `docx` + `doc-coauthoring` | Formal | Confidential |
| 8 | `02-business-docx/Customer Letter - Valoria Phase 2.docx` | `docx` + `internal-comms` | Formal external | Confidential |
| 9 | `03-pptx/Investor Update - Q1 2026.pptx` | `pptx` | Formal external | Public (with FLS) |
| 10 | `03-pptx/Q1 2026 Board Deck.pptx` | `pptx` | Formal | Confidential |
| 11 | `03-pptx/All-Hands Town Hall - April 2026.pptx` | `pptx` | Casual internal | Internal |
| 12 | `04-xlsx/Construction KPI Dashboard.xlsx` | `xlsx` | Formal | Confidential |
| 13 | `04-xlsx/Phase 2 Financial Model Summary.xlsx` | `xlsx` | Formal | Confidential |
| 14 | `05-internal-comms/All-Hands Email - Q1 2026.docx` | `internal-comms` | Casual internal | Internal |
| 15 | `05-internal-comms/NEXT Digest - April 2026.docx` | `internal-comms` | Casual internal | Internal |

## Specs each artifact is meant to validate

Each artifact is built to enforce a specific subset of the extracted NDLNG standards. Use this table to spot where output deviates.

### DOCX governance (three-tier)

| Spec rule (from `extracted-specs.md`) | How it shows up | Validate by |
|---|---|---|
| Section 8a page setup: Letter, 1.0" margins, 0.5" header/footer | All three docs | Word: Layout → Margins → Custom |
| Section 8b header: NDLNG logo + type + doc no + date + rev | Procedure doc header | Inspect header - logo PNG present |
| Section 8c canonical order (PURPOSE/SCOPE/GOVERNANCE/...) | All three docs | Skim section titles |
| Section 8d required tables (Definitions, References, RACI, Approval, Revision) | Standard + Procedure | Skim to end |
| Section 10 classification footer (HSSE-flash stamp) | Footer of all three | Zoom footer |
| §4.a Segoe UI everywhere (known gap: theme ships Aptos) | Body should render Segoe UI | Check that body text renders Segoe UI at 11pt (the known inconsistency #4 is that the underlying template theme references Aptos/Times; the render path overrides via run-level font) |
| §5.1 "never abbreviate NextDecade" | Body text | Search for "ND" or "NEXT" as abbreviations - should only appear as ticker |

### DOCX business

| Artifact | Spec validated |
|---|---|
| Board Memo | §5 formal register; navy 20pt headline; orange 1-pt rule; classification footer |
| Press Release | Formal register; exact FLS language from `pptx` disclaimer layout; dateline style; "###" end-mark |
| Fact Sheet | Brand chrome without classification; navy 28pt title; orange subtitle; 2-column body |
| Meeting Minutes | Formal register; decisions/actions table; classification footer |
| Customer Letter | Formal register; block-letter format; navy signature line; no ticker abbreviation |

### PPTX

| Artifact | Spec validated |
|---|---|
| Investor Deck | Layout 0 cover + Layout 2 Public Disclaimer (FLS legal) + Layout 3 back cover. Accent2 = brand orange #FC7134 on any orange element. ND / RG / NCS content layouts used where each brand is being referenced. |
| Board Deck | Cover + Disclaimer + ND-family content layouts + back cover. Disclaimer is retained even on a Board deck because the deck may be archived and distributed externally. |
| Town Hall Deck | Cover (no disclaimer) + ND-family content layouts + back cover. Casual register. |

### XLSX

| Artifact | Spec validated |
|---|---|
| KPI Dashboard | Segoe UI 10/11pt; header fill = brand navy; status cells coded green/yellow/red; footer = classification stamp + mission line + page numbers; chart palette. |
| Financial Model Summary | Segoe UI; Assumptions / Capex / Ops sheets; brand navy totals row; illustrative label on every sheet. |

### Internal comms (DOCX)

| Artifact | Spec validated |
|---|---|
| All-Hands Email | §5a casual register - contractions ("we're", "that's"); department banner (orange); classification footer; no page numbers |
| NEXT Digest Newsletter | Casual register; monthly cadence; sections required by channels list (Lead story, Safety Corner, Day in the Life, RGV, CCS update, Events, Shout-outs); tagline close |

## How these were built

Every file in `_build/` is a small, deterministic Python script. Inputs to the three governance docs (Standard / Procedure / Guidance) are JSON dicts in `_inputs/`. Everything else is constructed programmatically via `_build/nextdecade_brand.py` (fonts, colors, chrome) or via clone-and-fill of the `.potx` master.

Rebuild anytime:

```bash
# Governance docx
python skills/docx/scripts/render_docx.py standard  samples/document-types-validation/_inputs/records-retention-standard.json  "samples/document-types-validation/01-governance-docx/Records Retention Standard.docx"
python skills/docx/scripts/render_docx.py procedure samples/document-types-validation/_inputs/vendor-onboarding-procedure.json "samples/document-types-validation/01-governance-docx/Vendor Onboarding Procedure.docx"
python skills/docx/scripts/render_docx.py guidance  samples/document-types-validation/_inputs/remote-work-guidance.json         "samples/document-types-validation/01-governance-docx/Remote Work Guidance.docx"

# Business docx
python samples/document-types-validation/_build/build_board_memo.py       "samples/document-types-validation/02-business-docx/Q1 2026 Board Memo.docx"
python samples/document-types-validation/_build/build_press_release.py    "samples/document-types-validation/02-business-docx/Press Release - Q1 2026 Construction Update.docx"
python samples/document-types-validation/_build/build_fact_sheet.py       "samples/document-types-validation/02-business-docx/Rio Grande LNG Fact Sheet.docx"
python samples/document-types-validation/_build/build_meeting_minutes.py  "samples/document-types-validation/02-business-docx/Operating Committee Minutes - 2026-04-10.docx"
python samples/document-types-validation/_build/build_customer_letter.py  "samples/document-types-validation/02-business-docx/Customer Letter - Valoria Phase 2.docx"

# PPTX / XLSX / comms
python samples/document-types-validation/_build/build_pptx_decks.py samples/document-types-validation/03-pptx/
python samples/document-types-validation/_build/build_xlsx.py       samples/document-types-validation/04-xlsx/
python samples/document-types-validation/_build/build_comms.py      samples/document-types-validation/05-internal-comms/
```

## How to review

1. Open each file in its native Office app (Word / PowerPoint / Excel).
2. Compare against the matching spec row in the tables above.
3. Flag any drift in the "Gap analysis" tracker at the repo root (`gap-report.md`).
4. Typical things to look for:
   - **Typography:** is body text Segoe UI 11pt? Headlines navy 20pt?
   - **Color:** orange accents should be `#FC7134` (not `#ED7D31`); navy should be `#002060`.
   - **Logos/chrome:** header and footer chrome present where expected?
   - **Register:** formal docs should have no contractions; internal should have them.
   - **Footer:** classification stamp on internal/confidential docs; mission line everywhere; omitted on Public artifacts (Fact Sheet, Press Release).
   - **FLS:** press release + investor deck disclaimer should contain the §27A / §21E preamble and the "anticipate, assume, budget..." trigger list.

## Known limitations

- **PDF renders not included.** LibreOffice `soffice` failed to load files in the build sandbox (`javaldx` warning). You can run `soffice --headless --convert-to pdf <file.docx>` locally.
- **Letterhead.** No real NDLNG letterhead logo file is in `uploads/`; the customer letter and fact sheet use a text-rendered brand header in place of a logo image. Drop the logo PNG into `_build/` and update `nextdecade_brand.py` to `inline_image(...)` at top of page when the real logo is available.
- **Governance docx theme.** Templates ship with Aptos/Times New Roman theme defaults (extracted-specs.md inconsistency #4). Body text is force-overridden at render time to Segoe UI; if the native Office theme drift becomes a concern, swap the theme XML in the templates (see `.claude/plans/` for backlog).
- **Email signature artifacts.** Folder `uploads/20-org-signatures/` is empty, so the signature block in the board memo and customer letter uses a text-rendered approximation (name in navy, title in black). Replace when real signature assets land.

## What this set does NOT validate (intentionally)

These are called out in the deep-dive gap write-up at the repo root:

- Regulatory filings (FERC / DOE / PHMSA / SEC 8-K / 10-Q) - no folder-12 samples yet.
- Community / bilingual EN-ES artifacts - no folder-15 samples yet.
- ESG / SASB / TCFD disclosure - no folder-16 samples yet.
- Data visualization style sheet (beyond the KPI dashboard) - no folder-17 samples yet.
- File-naming convention enforcement - no folder-19 rule set yet (filenames here follow the `[Artifact Type] - [Topic] - [Date].ext` convention as a working default).
- Email signatures / executive bios - no folder-20 assets yet.
