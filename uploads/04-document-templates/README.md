# 04 — Document Templates (Word)

**Priority:** REQUIRED. These become the starting point for every Word doc Claude produces.

## What to upload here

Upload BLANK or MINIMALLY-FILLED `.docx` templates. Include the native `.docx` (not just PDFs) so Claude can read styles, themes, and section properties directly.

### Core templates (upload any you have)
- [ ] Corporate letterhead (1st page + continuation page)
- [ ] Internal memo
- [ ] Executive / leadership memo
- [ ] Board memo or board packet cover
- [ ] Standard report template (with cover, TOC, body, appendix)
- [ ] Technical report template
- [ ] SOP / procedure template
- [ ] Meeting agenda template
- [ ] Meeting minutes template
- [ ] Press release template
- [ ] MSA / contract template (blank)
- [ ] NDA template (blank)
- [ ] Statement of Work (SOW) template
- [ ] Proposal / RFP response template
- [ ] Project charter template
- [ ] Change request template
- [ ] Decision document / DACI template
- [ ] Briefing paper

### Supporting material
- [ ] Style documentation (if the templates have a cheat sheet)
- [ ] Which template to use when (a selection guide)

## File types expected

`.docx`, `.dotx` (Word template format), `.docm` (macro-enabled only if needed)

## What Claude will extract

- Page size, margins, orientation for each template
- Headers and footers (logo position, page numbering style, classification footer)
- All paragraph styles defined in `word/styles.xml` (Heading 1–6, Body, Quote, Caption, etc.)
- Table styles
- List styles (bullet characters, numbering formats, indentation)
- Section break patterns (cover vs. TOC vs. body)
- Track changes / comment settings defaults
- Theme colors and fonts embedded in the template
- Bookmark / cross-reference conventions

## Feeds these skills

- `skills/docx/` (full rewrite — templates become the default starting point)
- `skills/doc-coauthoring/` (workflow starts with the right template)
- NEW: `skills/legal-boilerplate/` (MSA/NDA/SOW boilerplate)
- NEW: `skills/classification/` (footers extracted here)

## Notes

- If you have "approved" and "draft" versions, upload both and label which is current
- If templates vary by department (legal, engineering, commercial, IR) — note this in a file so Claude extracts per-department defaults
- The goal is that "Claude, draft a board memo" instantly applies the right template. Same for every doc type above.
