# NextDecade LNG — Gap Report (after first extraction pass)

Generated alongside `extracted-specs.md`. Three sections:
1. **Inconsistencies in what you uploaded** (must be reconciled before any skill is rewritten)
2. **What's still missing per intake folder**
3. **Net-new skills that can/can't be built today**

---

## 1. Inconsistencies in what you uploaded

These must be resolved before extraction propagates into the skill files — otherwise we bake conflicting rules into 20+ skills.

### 1a. Color drift between brand PDF and PowerPoint master (material)

| Item | Brand PDF says | PPTX theme has | Action |
|---|---|---|---|
| Primary orange | #FC7134 (Pantone 1645 C) | accent2 = #ED7D31 (Office default) | **Pick one and re-master both files.** Most likely the brand PDF is the source of truth and the .potx accent2 needs to change to FC7134. |
| Primary green | #00B050 (Pantone 361 C) | not present in theme at all | Add as accent or extra theme color in the .potx. |
| accent3 #9CC3E5 / accent4 #00B0F0 / accent5 #A8D08D / accent6 #C55A11 | not documented | present in theme | Either document them in the brand guide (as approved tints/extensions) or remove. |

### 1b. Word templates: brand chrome present, but theme not applied

Each .docx template carries:
- 3 embedded images (cover graphic ~120KB, watermark .wdp, logo PNG ~70KB)
- NextDecade-specific governance structure (PURPOSE / SCOPE / GOVERNANCE FRAMEWORK …)
- NextDecade footers ("NextDecade Corporation Standard / Procedure / Guidance Document")
- NextDecade headers ("[STANDARD/PROCEDURE/GUIDANCE Document NAME] Rev.: x  Doc. No. xxx-xxx-xxx-xxx-xxx-#####")
- NextDecade-defined terms ("Workforce", "Governance Framework")

What's NOT applied is the **theme layer**:
- Theme fonts: Aptos / Aptos Display (brand PDF and style guide §5.4 specify Segoe UI)
- Heading 1: 20pt #0F4761 (Word default teal) instead of navy #002060
- Body runs: hardcoded Times New Roman 11pt instead of Segoe UI 11pt
- Theme color slots: Office defaults

**Severity: medium**, not critical. The chrome and structure are NDLNG; the typography defaults aren't. Re-theming would harmonize the typography with brand standard, but the templates already function as branded governance docs.

### 1c. Footer mission-line wording differs

- Brand PDF page-footer: "…through **RGLNG** & NEXT Carbon Solutions."
- Style guide page-footer: "…through **Rio Grande LNG** & NEXT Carbon Solutions."

Both can't be the boilerplate. Style guide §5.1 says never abbreviate; suggests the spelled-out version wins, but the brand book itself contradicts it.

### 1d. "Feb. 27 2024" style guide cover dated **2024**, body refers to **2023**

The cover page reads "WRITING STYLE GUIDE & RESOURCES 2023" overlapping with "WRITING STYLE GUIDE 2024" (looks like a layered title). Examples reference 2023. Confirm the doc is current for 2024 and that all dates ("Jan. 5, 2023") are illustrative, not stale.

### 1e. Slide master file says **Final_Oct 2025** but the brand-guide PowerPoint instructions reference **Final_March 2024**

Brand PDF (p.9) tells employees to look for the file named "NextDecade Power Point Slide Master_Final_March 2024." The uploaded master is named "…Final_Oct 2025." Either the brand PDF is out-of-date or a cross-reference fix is needed.

### 1f. PPTX has 50 layouts but only ~15 are descriptively named

Layouts named "Custom Layout," "1_Custom Layout," "23_Custom Layout," etc. are functional but undocumented — content authors can't know what they're for. Recommend renaming or adding a hidden "layout map" reference slide.

### 1g. Residual second/third theme files in the .potx

`theme2.xml` and `theme3.xml` inside the .potx are Office defaults (Calibri, blue/red accents). They're vestigial. Cleaning them up would prevent layouts from accidentally inheriting non-brand colors.

---

## 2. What's still missing per intake folder

Status legend: **R** = Required by intake README, **r** = Recommended.

| # | Folder | Status | Have? | What you still need |
|---|---|---|---|---|
| 01 | brand | **R** | ✓ Brand & Style Guidelines 2024.pdf (logos are also embedded in the .docx and .potx and can be reused at production time) | Optional/nice-to-have: vector logo files (.ai/.svg/.eps) for resizing/recoloring without quality loss; brand architecture diagram. |
| 02 | typography | **R** | — | **Segoe UI font files** (or licensing note that they ship with Windows). Type scale (H1–H6 sizes for digital + print). Pairing rules (when to use Segoe Light vs. Bold). Web-safe fallback stack. |
| 03 | imagery | r | — | Approved photo library (RGLNG site, plant aerials, executive headshots, community engagement, RGV scenery). Iconography (the "selection of visual assets" the brand PDF says lives on a SharePoint link). Image treatment rules (duotone? overlays? cropping?). |
| 04 | document templates | **R** | ✓ Standard / Procedure / Guidance | Letterhead .docx, memo template, press release template, MSA / contract templates, board memo template, meeting agenda + minutes templates, fact-sheet template. Templates re-themed (see 1b). |
| 05 | presentation templates | **R** | ✓ Slide Master Oct 2025.potx | Investor deck *as actually used* (not the master), board deck specimen, all-hands template, town-hall template. Cover-art image library. |
| 06 | spreadsheet templates | r | — | Operational dashboard .xlsx, financial model, KPI tracker, data-room index. With branded chart styles (folder 17). |
| 07 | sample documents | r | — | Last 2–3 finished real Standards/Procedures/Guidance (redacted) so we can tell what authors *actually* produce vs. what the template says. Press releases, board memos, customer letters. |
| 08 | sample presentations | r | — | Last 2–3 finished investor decks, the most recent earnings deck, an analyst-day deck, an all-hands deck. |
| 09 | sample communications | r | ✓ Writing Style Guide 2024.pdf | Sample press releases, sample all-hands emails (the cyber-training one in the appendix is a single example — need 5–10 across types). Customer letters. |
| 10 | style/voice guide | **R** | (style guide is in folder 09 — flag) | Move/copy the style guide to folder 10 where it belongs. Add: terminology glossary (defined product names, project phases). Forbidden / discouraged words list. Bilingual glossary EN→ES if RGV-bilingual is in scope. |
| 11 | legal boilerplate | **R** | (FLS captured from .potx — flag) | Standalone source-of-truth versions of: Forward-Looking Statements (we have it from the deck — needs to be the canonical text controlled by Legal), Safe Harbor wording, Confidentiality / NDA notices, TM / SM symbol usage rules, Reg FD treatment, privacy / data handling boilerplate. |
| 12 | regulatory samples | r | — | FERC filing example (formatting only, redacted), DOE export-authorization filing, PHMSA / MARAD example, TCEQ / EPA filings. Just 1–2 of each is plenty to learn the formatting. |
| 13 | investor relations | r | — | Earnings call script template, fact sheet, analyst deck, last 10-K excerpt, last 10-Q excerpt, last 8-K (or two), Reg FD policy, IR website copy. |
| 14 | safety/HSE | r | ✓ HSSE-Flash-Template_R5 | Safety moment template (1-pager opener for meetings), incident-comms language, HSE messaging guide, Life-Saving Rules visual, leadership safety message template. |
| 15 | community/stakeholder | r | — | Bilingual EN/ES samples (RGV community materials), public-comment response template, community newsletter, open-house collateral, FAQ for community questions. |
| 16 | ESG/sustainability | r | — | ESG report (most recent), CCS narrative, SASB / TCFD / GRI alignment tables, climate disclosure language. |
| 17 | data viz / charts | r | — | Approved chart palette (probably reusing the brand colors), dashboard examples, data-labeling conventions, axis/legend rules, "do/don't" for chart types. |
| 18 | classification rules | **R** | (one classification line captured from HSSE flash — flag) | Tier definitions (Public / Internal / Confidential / Restricted or whatever NextDecade uses), exact label text per tier, position (header/footer/watermark), color/opacity, default tier per doc-type, any metadata or rights-management requirements. The HSSE flash provides one example — need the policy. |
| 19 | file naming | r | — | Naming convention (formal docs vs. informal). The Standard/Procedure templates show "xxx-xxx-xxx-xxx-xxx-#####" doc-number format — capture the rule that drives the prefixes. Versioning rule (R5, Rev. x, etc.). |
| 20 | org / signatures | r | — | Org chart, executive bios, full email signature template (text + image), exec-letter signature blocks. |

### Required-folder snapshot

| Required folder | Status |
|---|---|
| 01-brand | ✓ partial (rules but no source files) |
| 02-typography | ✗ empty |
| 04-document-templates | ⚠ present but wrong-themed |
| 05-presentation-templates | ✓ |
| 10-style-voice-guide | ✗ empty (file is in 09) |
| 11-legal-boilerplate | ✗ empty (FLS only available via .potx slide) |
| 18-classification-rules | ✗ empty (one example only via HSSE flash) |

**Three Required folders are still empty (02, 11, 18).** Two more (10 and 04) need correction. Do not propagate any classification, legal, or typography rules into `/skills/` until those three folders are populated.

---

## 3. Skills status — what can be built today

### Can be built / personalized now (specs are sufficient)

| Skill | Why ready |
|---|---|
| `pptx/` | Template, theme, layouts, FLS language, tagline, address, ticker all captured. Can produce on-brand decks today. |
| `internal-comms/` | Voice rules, channels, headline conventions, e-mail-message rules, capitalization/date/time rules, sample message all captured from style guide. |
| `safety-hse/` (NEW) | HSSE Flash template fields, photo disclaimer, classification footer all captured. |
| `doc-coauthoring/` | Voice + style guide is enough to coach drafting — but output won't be on-brand until #1b is fixed. |

### Can be built but with major caveats

| Skill | Caveat |
|---|---|
| `docx/` | Templates carry NextDecade chrome + embedded logos and can be used today. Theme typography (Segoe UI + brand colors) not applied — the skill should ship with a pre-write step that overrides Aptos→Segoe UI and the Heading 1 color to navy. |
| `brand-guidelines/` | Color/font rules captured. Logos are reusable from existing templates; vector files would be nice-to-have but aren't a blocker. |
| `legal-boilerplate/` (NEW) | Forward-Looking Statements text was captured verbatim from the .potx. Legal needs to ratify it before it's distributed as canonical. Safe Harbor / Confidentiality / Reg FD / TM rules all still missing. |

### Cannot be built yet (insufficient data)

| Skill | Blocker |
|---|---|
| `classification/` (NEW) | One footer line is not a classification system. Need the full tier definitions (folder 18). |
| `regulatory-comms/` (NEW) | Folder 12 is empty. |
| `investor-relations/` (NEW) | Folder 13 is empty. |
| `community-stakeholder/` (NEW) | Folder 15 is empty (bilingual EN/ES not represented anywhere). |
| `esg-reporting/` (NEW) | Folder 16 is empty. |
| `data-visualization/` (NEW) | Folder 17 is empty (could derive a starter palette from theme accents but no charting standards). |
| `file-naming/` (NEW) | Folder 19 is empty (doc-number pattern visible in templates is the only signal). |
| `email-signatures/` (NEW) | Folder 20 is empty (brand PDF describes signature exists but no template was uploaded). |
| `xlsx/` | Folder 06 is empty. |

---

## 4. Recommended next actions, in order

1. **Reconcile the 7 inconsistencies in §1**, especially 1a (color drift), 1b (.docx not branded), and 1c (footer wording). These propagate into every output.
2. **Fill the three remaining Required folders** (02 typography source files, 11 legal boilerplate ratified by Legal, 18 classification system).
3. **Move/copy the Writing Style Guide PDF into folder 10** (it currently lives in 09).
4. **Upload at least one finished investor deck** into folder 08 — it's the single highest-value sample for IR-quality output.
5. **Provide vector logo files** (.ai/.svg/.eps) into folder 01 — without them no brand-compliant export pipeline is possible.
6. After (1)–(5), I can run **a second extraction pass** that produces a delta against this report and proceed to the personalization phase (rewrite skills in `/skills/`).

---

## 5. What I'd flag specifically to Legal / Comms / Brand before propagation

**To Legal**: confirm the Forward-Looking Statements text in `extracted-specs.md` §9 is the current, ratified version. Provide the standalone Safe Harbor / Confidentiality / Reg FD / TM-usage boilerplate.

**To Brand / Corporate Comms**: resolve the color drift (#FC7134 vs. #ED7D31) and the absent green (#00B050). Provide vector logo files. Decide whether the four "extra" PPTX accents (#9CC3E5, #00B0F0, #A8D08D, #C55A11) are sanctioned or to be removed.

**To Document Control / Governance**: the three .docx templates need re-theming to Segoe UI + brand colors before they're held up as the institutional standard. Otherwise Standards / Procedures / Guidance going forward will be off-brand by default.

**To IT / Comms**: provide the actual e-mail signature .docx and the e-mail department-banner library referenced in the style guide.

**To HSSE**: confirm the photo-reenactment disclaimer and confidentiality footer in the HSSE Flash deck are the canonical company-wide language, or specific to that deck only.
