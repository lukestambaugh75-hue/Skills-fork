# NextDecade LNG — Enterprise Skills Personalization Intake

This folder is the **intake mechanism** that turns this generic skills repo into **the NextDecade LNG enterprise template library**. You drop real company artifacts into the subfolders below, Claude extracts every brand/style/format/voice detail, and every skill in `/skills/` gets rewritten to enforce NDLNG standards by default.

## How this works

```
  You upload artifacts          Claude extracts details          Every skill in /skills/
  into uploads/XX-*/     ───►   (colors, fonts, voice,    ───►   is rewritten to enforce
  (real NDLNG files)            layout, boilerplate, etc.)       NDLNG standards by default
```

**End state:** someone on your team asks Claude "draft a board memo" or "build an investor deck" and the output is on-brand, on-voice, correctly classified, legally compliant, and indistinguishable from what a senior NDLNG comms professional would produce — without them having to know any of the rules.

## Before you start

1. **Upload what you have, skip what you don't.** Every folder is optional. Missing material becomes a gap list I'll surface back to you.
2. **Redact anything sensitive first.** Real finished documents are the most valuable input, but strip material-non-public information, PII, customer names, or anything under NDA before uploading.
3. **More is better than less.** If you have three versions of an investor deck, upload all three — I'll identify what's consistent (those are the rules) vs. what varies (those are options).
4. **Originals beat PDFs.** A `.pptx` template is worth 10 exported PDFs because I can read the master slides, theme colors, fonts, and layout logic. Same for `.docx` over PDF and `.xlsx` over screenshots.
5. **Include the "don't" examples.** If you have things that are explicitly off-brand or a "we used to do it this way and stopped," flag them — negative examples train the skills.

## The 20 intake categories

| # | Folder | What it captures | Required? |
|---|--------|------------------|-----------|
| 01 | `01-brand/` | Brand guidelines PDF, color spec, tagline, brand architecture | **Required** |
| 02 | `02-typography/` | Actual font files, type scale, pairing rules | **Required** |
| 03 | `03-imagery/` | Approved photos (site, plant, aerials, headshots), icons, illustrations | Recommended |
| 04 | `04-document-templates/` | `.docx` masters: letterhead, memo, report, SOP, MSA, press release | **Required** |
| 05 | `05-presentation-templates/` | `.pptx` masters: investor deck, board deck, internal, all-hands, town hall | **Required** |
| 06 | `06-spreadsheet-templates/` | `.xlsx` masters: financial model, operational dashboard, tracker | Recommended |
| 07 | `07-sample-documents/` | Finished real documents to reverse-engineer (redact first) | Recommended |
| 08 | `08-sample-presentations/` | Finished real decks — last 2–3 investor updates especially valuable | Recommended |
| 09 | `09-sample-communications/` | Press releases, all-hands emails, customer letters, newsletters | Recommended |
| 10 | `10-style-voice-guide/` | Editorial style guide, tone of voice, terminology, do/don't words | **Required** |
| 11 | `11-legal-boilerplate/` | Safe harbor, forward-looking statements, confidentiality, TM notices | **Required** |
| 12 | `12-regulatory-samples/` | FERC, DOE, PHMSA, MARAD, TCEQ, EPA filings — formatting conventions | Recommended |
| 13 | `13-investor-relations/` | Earnings scripts, fact sheet, analyst deck, 10-K/10-Q/8-K excerpts | Recommended |
| 14 | `14-safety-hse/` | Safety moment templates, HSE messaging, incident comms language | Recommended |
| 15 | `15-community-stakeholder/` | RGV community engagement, bilingual EN/ES materials, public comments | Recommended |
| 16 | `16-esg-sustainability/` | ESG report, CCS narrative, SASB/TCFD/GRI disclosures | Recommended |
| 17 | `17-data-viz-charts/` | Approved chart styles, dashboards, data labeling conventions | Recommended |
| 18 | `18-classification-rules/` | Public / Internal / Confidential / Restricted footers & watermarks | **Required** |
| 19 | `19-file-naming/` | File naming & versioning convention | Recommended |
| 20 | `20-org-signatures/` | Org chart, email signature template, executive bios | Recommended |

**"Required"** = the personalization can't produce credible NDLNG output without this. Skills that depend on it will stay as scaffolding until filled.

## What Claude will extract from your uploads

For each upload, Claude systematically pulls out:

### From visual assets (brand guide, logos, templates)
- Exact hex / RGB / CMYK / Pantone color values
- Font family names, weights, sizes, line heights, letter spacing
- Logo clear space, minimum size, approved backgrounds, prohibited treatments
- Grid systems, margins, gutter widths
- Image treatment rules (duotone, overlays, cropping)
- Iconography style (stroke weight, corner radius, fill style)

### From document/presentation templates
- Page / slide dimensions, margins, safe zones
- Header and footer composition (logo position, page numbers, classification labels)
- Heading hierarchy (H1/H2/H3 sizes, colors, spacing)
- Table styles (border, shading, header row treatment)
- Bullet list styles, indentation
- Cover page layout rules
- Section divider treatment

### From written samples
- Sentence length distribution (average + range)
- Paragraph length conventions
- Voice markers (first-person plural? active vs. passive?)
- Terminology preferences (e.g., "Rio Grande LNG Facility" vs. "Rio Grande LNG" vs. "RGLNG")
- Capitalization rules (product names, project phases, acronyms)
- Punctuation conventions (Oxford comma, em vs. en dash, quotation style)
- Forbidden words / phrases
- Standard phrases / repeated structures
- How numbers, dates, units are formatted (MMBtu, MTPA, Bcf/d, etc.)

### From legal/compliance material
- Exact wording of forward-looking statements
- Safe harbor language verbatim
- Confidentiality / NDA notices
- Trademark and service mark usage
- SEC Reg FD treatment
- Privacy / data handling disclosures

### From classification material
- Label text (e.g., "CONFIDENTIAL — INTERNAL USE ONLY")
- Position on page (header, footer, watermark)
- Color and opacity
- Which document types get which classification by default

## How extraction flows into the repo

Here's what gets rewritten in `/skills/` after extraction:

| Source (uploads/) | Target skill (skills/) | What changes |
|-------------------|------------------------|--------------|
| `01-brand`, `02-typography`, `03-imagery` | `brand-guidelines/` | Replaces Anthropic colors/fonts with NDLNG specifics; adds logo usage, imagery rules |
| `04-document-templates`, `07-sample-documents`, `11-legal-boilerplate`, `18-classification-rules` | `docx/` | Default page setup, fonts, headers/footers, classification footers baked in; templates pre-staged |
| `05-presentation-templates`, `08-sample-presentations` | `pptx/` | Default master, cover/divider/content layouts, logo placement, footer requirements |
| `06-spreadsheet-templates`, `17-data-viz-charts` | `xlsx/` | Default number formats, chart palette, dashboard templates |
| `09-sample-communications`, `10-style-voice-guide` | `internal-comms/` | NDLNG tone of voice, approved phrasing, forbidden words, templates for 3P, newsletter, FAQ, town-hall |
| `10-style-voice-guide`, `07-sample-documents` | `doc-coauthoring/` | Co-authoring workflow starts with NDLNG templates; voice coaching matches style guide |
| `19-file-naming` | NEW: `file-naming/` | New skill enforcing naming convention |
| `18-classification-rules` | NEW: `classification/` | New skill that classifies & stamps every output |
| `11-legal-boilerplate` | NEW: `legal-boilerplate/` | New skill providing the exact approved language |
| `12-regulatory-samples` | NEW: `regulatory-comms/` | New skill for FERC/DOE/SEC/PHMSA filing conventions |
| `13-investor-relations` | NEW: `investor-relations/` | New skill: earnings, 8-K, Reg FD, material information handling |
| `14-safety-hse` | NEW: `safety-hse/` | New skill: safety moments, incident comms, HSE tone |
| `15-community-stakeholder` | NEW: `community-stakeholder/` | New skill: bilingual EN/ES, community engagement, public comment response |
| `16-esg-sustainability` | NEW: `esg-reporting/` | New skill: ESG narrative, CCS framing, framework alignment |
| `17-data-viz-charts` | NEW: `data-visualization/` | New skill: chart colors, labeling, dashboard standards |
| `20-org-signatures` | NEW: `email-signatures/` | New skill: email signature generator, exec bio formatting |

## The "massive hole" gap list (beyond just file mechanics)

The existing repo teaches Claude HOW to build a .docx or .pptx. It doesn't teach:

**Governance & integrity**
- [ ] Document classification (Public / Internal / Confidential / Restricted) — folder 18
- [ ] Approval & review workflows (who signs off on what) — captured in folder 10
- [ ] Version control & file naming conventions — folder 19
- [ ] Accessibility (WCAG, alt text, contrast, readable fonts) — extracted across folders

**Industry-specific (LNG / energy / public company)**
- [ ] SEC / IR comms (8-K, 10-Q/K, earnings, Reg FD) — folder 13
- [ ] Regulatory filing formats (FERC, DOE, PHMSA, MARAD, TCEQ) — folder 12
- [ ] HSE / safety messaging — folder 14
- [ ] Community / stakeholder engagement (bilingual EN/ES for RGV) — folder 15
- [ ] Crisis / incident communications — folder 14
- [ ] ESG / sustainability reporting (SASB / TCFD / GRI / CCS narrative) — folder 16

**Design & content quality**
- [ ] Chart & data visualization standards — folder 17
- [ ] Photography / imagery standards — folder 3
- [ ] Iconography library — folder 3
- [ ] Meeting artifacts (agendas, minutes, action items, board packets) — capture in 04/07
- [ ] Email signature & exec bio formatting — folder 20

All of these become new skills once the uploads are in place.

## Workflow — how to actually run this

1. **Upload phase** (you): Drop files into the subfolders. Read each folder's README for specifics. Do this over days/weeks as you gather material — it doesn't have to be one sitting.
2. **Gap review** (Claude): Once you signal "initial upload done," Claude audits what's present vs. missing and reports back a prioritized gap list.
3. **Extraction phase** (Claude): Claude reads every asset, extracts specifications into a single structured `extracted-specs.md` for your review.
4. **Review & correction** (you): You review the extracted specs. Correct anything Claude got wrong before it propagates into 20+ skill files.
5. **Personalization phase** (Claude): Claude rewrites each skill in `/skills/` using the approved specs. Creates new skills for the gaps. Produces a diff report.
6. **Smoke test** (both): Ask Claude to produce one of each artifact type (memo, investor slide, press release, safety moment). Review and fine-tune.
7. **Ship as template**: The repo is now the NDLNG enterprise skills template for your organization to distribute.

## What I need from you to start

Signal when you've uploaded your first batch (even partial — e.g., just folders 01, 02, 10, 11, 18). I'll run the gap review and extraction from there.
