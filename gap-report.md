# NextDecade LNG — Gap Report (revised after user resolutions, 2026-04-14)

Generated alongside `extracted-specs.md`. Three sections:
1. **Inconsistencies — status after this round of resolutions**
2. **What's still missing per intake folder** (folders 02, 11, 18 are now out of scope per user direction)
3. **Net-new skills that can/can't be built today**

---

## 1. Inconsistencies — status

### 1a. Color drift between brand PDF and PowerPoint master — **RESOLVED**

| Item | Before | After | How |
|---|---|---|---|
| Primary orange | accent2 = #ED7D31 (Office default) | accent2 = **#FC7134** (brand) | Patched in `theme1.xml` of the .potx |
| Primary green | not in theme | not added | Per user: ignore the accent colors. Apply per-shape fill if green needed. |
| accent3 #9CC3E5 / accent4 #00B0F0 / accent5 #A8D08D / accent6 #C55A11 | undocumented in brand book | retained as-is | Per user: ignore the accent colors. |

### 1b. Word templates: brand chrome present, theme not applied — **NOTED**

Each .docx template carries:
- 3 embedded images including the **NextDecade logo in the header** (the cover graphic ~120KB, the watermark .wdp, and the logo PNG ~70KB)
- NextDecade-specific governance structure (PURPOSE / SCOPE / GOVERNANCE FRAMEWORK …)
- NextDecade footers ("NextDecade Corporation Standard / Procedure / Guidance Document")
- NextDecade headers (logo + "[STANDARD/PROCEDURE/GUIDANCE Document NAME] Rev.: x  Doc. No. xxx-xxx-xxx-xxx-xxx-#####")
- NextDecade-defined terms ("Workforce", "Governance Framework")

What's NOT applied is the theme layer (Aptos / Times New Roman / #0F4761 teal heading). **Severity: low** — chrome and structure are NDLNG, only the typography defaults aren't. Documents produced from these templates inherit the brand chrome including the logo automatically.

### 1c. Footer mission-line wording — **RESOLVED**

Forced to **"…through Rio Grande LNG & NEXT Carbon Solutions."** (spell out, never "RGLNG"). The brand PDF's "RGLNG" abbreviation is superseded; to be corrected in the next brand-PDF revision. Style guide §5.1 ("never abbreviate") wins.

### 1d. Style guide cover dated 2024 vs. body refers to 2023 — **OPEN (low)**

Cover page reads "WRITING STYLE GUIDE & RESOURCES 2023" overlapping with "WRITING STYLE GUIDE 2024". Examples reference 2023. Confirm doc currency at next revision.

### 1e. Slide-master version cross-reference — **RESOLVED**

The .potx is canonical as **Final_Oct 2025**. The brand PDF (p.9) reference to "Final_March 2024" is stale and superseded; to be corrected in the next brand-PDF revision.

### 1f. PPTX has 50 layouts but only ~15 are descriptively named — **OPEN (low)**

Layouts named "Custom Layout," "1_Custom Layout," "23_Custom Layout," etc. are functional but undocumented. Recommend renaming or adding a hidden "layout map" reference slide at next deck revision.

### 1g. Residual second/third theme files in the .potx — **OPEN (low)**

`theme2.xml` and `theme3.xml` inside the .potx are Office defaults (Calibri, blue/red accents). Vestigial; cleanup would prevent layouts from accidentally inheriting non-brand colors.

---

## 2. What's still missing per intake folder

Status legend: **R** = Required by intake README, **r** = Recommended, **—** = out of scope per user direction.

| # | Folder | Status | Have? | What you still need |
|---|---|---|---|---|
| 01 | brand | **R** | ✓ Brand & Style Guidelines 2024.pdf (logos are also embedded in the .docx and .potx and reusable at production time) | Optional: vector logo files (.ai/.svg/.eps) for resizing/recoloring without quality loss. |
| 02 | typography | — | — | Out of scope. Skills will assume Segoe UI (per brand book) is available system-side. |
| 03 | imagery | r | — | Approved photo library, iconography, image treatment rules. |
| 04 | document templates | **R** | ✓ Standard / Procedure / Guidance (logo in header, NDLNG chrome) | Optional add-ons: letterhead, memo template, press release template, MSA, board memo, meeting agenda + minutes, fact-sheet template. |
| 05 | presentation templates | **R** | ✓ Slide Master Final_Oct 2025.potx (theme patched to brand orange) | Specimens of finished decks (investor / board / all-hands / town-hall). |
| 06 | spreadsheet templates | r | — | Operational dashboard, financial model, KPI tracker, data-room index. (xlsx skill personalized with brand colors regardless.) |
| 07 | sample documents | r | — | Last 2–3 finished real Standards/Procedures/Guidance, redacted. Press releases, board memos, customer letters. |
| 08 | sample presentations | r | — | Last 2–3 finished investor decks, most recent earnings deck, analyst-day deck, all-hands deck. |
| 09 | sample communications | r | (style guide moved to folder 10) | Sample press releases, sample all-hands emails, customer letters. |
| 10 | style/voice guide | **R** | ✓ Writing Style Guide & Resources 2024.pdf (moved here from folder 09) | Optional: terminology glossary, forbidden-words list, EN→ES bilingual glossary if relevant. |
| 11 | legal boilerplate | — | — | Out of scope. FLS text captured from the .potx is the working version. |
| 12 | regulatory samples | r | — | FERC, DOE, PHMSA / MARAD, TCEQ / EPA filing samples (1–2 of each). |
| 13 | investor relations | r | — | Earnings call script, fact sheet, analyst deck, 10-K/10-Q/8-K excerpts, Reg FD policy, IR website copy. |
| 14 | safety/HSE | r | ✓ HSSE-Flash-Template_R5 | Safety moment template, incident-comms language, HSE messaging guide, Life-Saving Rules visual. |
| 15 | community/stakeholder | r | — | Bilingual EN/ES samples, public-comment response template, community newsletter, open-house collateral. |
| 16 | ESG/sustainability | r | — | ESG report, CCS narrative, SASB/TCFD/GRI alignment tables, climate disclosure language. |
| 17 | data viz / charts | r | — | Approved chart palette, dashboard examples, data-labeling conventions, axis/legend rules. |
| 18 | classification rules | — | — | Out of scope. Default classification footer (HSSE-flash language) is the working stamp until policy lands. |
| 19 | file naming | r | — | Naming convention; doc-number pattern `xxx-xxx-xxx-xxx-xxx-#####` from templates is the only signal today. |
| 20 | org / signatures | r | — | Org chart, executive bios, full email signature template, exec-letter signature blocks. |

### Required-folder snapshot (post-resolution)

| Required folder | Status |
|---|---|
| 01-brand | ✓ |
| 02-typography | — out of scope |
| 04-document-templates | ✓ (theme typography is a known low-severity gap) |
| 05-presentation-templates | ✓ patched |
| 10-style-voice-guide | ✓ (style guide PDF moved here) |
| 11-legal-boilerplate | — out of scope |
| 18-classification-rules | — out of scope |

**All required folders are now either complete or explicitly out of scope.**

---

## 3. Skills status — what can be built today

### Can be built / personalized now

| Skill | Why ready |
|---|---|
| `pptx/` | Template, theme (now color-corrected), layouts, FLS language, tagline, address, ticker all captured. |
| `xlsx/` | Personalized in commit `81f5819` — Segoe UI + brand colors + classification footer + helper snippet. |
| `internal-comms/` | Voice rules, channels, headline conventions, e-mail rules, capitalization/date/time rules captured. |
| `safety-hse/` (NEW) | HSSE Flash template fields, photo disclaimer, classification footer all captured. |
| `doc-coauthoring/` | Voice + style guide is enough to coach drafting. |
| `docx/` | Templates carry NextDecade chrome + embedded logo + structure. Theme-typography override (Aptos→Segoe UI, teal→navy headings) can be applied at write-time. |
| `brand-guidelines/` | Color/font rules captured; logos reusable from existing templates. |
| `legal-boilerplate/` (NEW) | FLS verbatim from .potx is the working canonical version per user direction (folder 11 out of scope). |
| `classification/` (NEW) | HSSE-flash classification stamp is the working default per user direction (folder 18 out of scope). |

### Still cannot be built (data not in scope yet)

| Skill | Blocker |
|---|---|
| `regulatory-comms/` (NEW) | Folder 12 empty. |
| `investor-relations/` (NEW) | Folder 13 empty. |
| `community-stakeholder/` (NEW) | Folder 15 empty. |
| `esg-reporting/` (NEW) | Folder 16 empty. |
| `data-visualization/` (NEW) | Folder 17 empty (xlsx skill provides starter chart palette in the meantime). |
| `file-naming/` (NEW) | Folder 19 empty. |
| `email-signatures/` (NEW) | Folder 20 empty. |

---

## 4. Recommended next actions

1. **Personalize the next batch of "ready" skills**: `pptx`, `internal-comms`, `safety-hse`, `docx`, `brand-guidelines`, `doc-coauthoring`, `legal-boilerplate`, `classification` — using the values in `extracted-specs.md` and the resolutions in this report.
2. **Smoke-test**: produce one of each artifact type (memo, investor slide, press release, safety moment) and review.
3. Optional: upload finished sample decks to `08-sample-presentations/` — they are the single highest-value input for tightening IR-quality output once the basics are in place.
