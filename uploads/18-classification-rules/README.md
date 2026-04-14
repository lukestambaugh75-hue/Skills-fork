# 18 — Document Classification & Handling

**Priority:** REQUIRED. Enforces confidentiality and information-handling at every document.

## What to upload here

### Classification scheme
- [ ] Data classification policy (Public / Internal / Confidential / Restricted, or your specific tiers)
- [ ] Definitions for each classification level
- [ ] Examples of what belongs in each tier

### Visual treatment
- [ ] How each classification appears on documents:
  - Footer text exact wording
  - Header text (if used)
  - Watermark (if used) — image or text, color, opacity
  - Cover-page treatment (if differs from body)
- [ ] Color coding per classification (if used)

### Handling rules
- [ ] Who can create documents at each level
- [ ] Who can receive / be CCed at each level
- [ ] External sharing rules per level
- [ ] Retention requirements per level
- [ ] Disposal / destruction requirements

### Default classification by document type
- [ ] Which document types default to which classification:
  - Board materials → ?
  - IR materials (pre-release) → ?
  - Safety bulletins → ?
  - Community communications → ?
  - Press releases (pre-publication vs. post) → ?
  - Regulatory filings (as filed) → ?
- [ ] Auto-classification rules (e.g., "anything containing financial guidance pre-release = Restricted")

### Related
- [ ] Email classification labeling rules (Outlook / Gmail labels)
- [ ] Teams / SharePoint classification conventions
- [ ] Printing / hardcopy handling

## File types expected

`.pdf`, `.docx`, `.pptx` (classification policy document or examples)

## What Claude will extract

- Full classification taxonomy (with definitions)
- Exact footer/header/watermark treatment per level (text, color, opacity, position)
- Default classification per document type — Claude will auto-apply
- Escalation triggers (when to upgrade classification)
- External-share rules — what requires NDA, approval, redaction
- Auto-flag rules — words/phrases that trigger classification review (e.g., "guidance," "term sheet," "merger")

## Feeds these skills

- NEW: `skills/classification/` (dedicated skill that labels every output)
- `skills/docx/` (auto-insert classification footer)
- `skills/pptx/` (auto-insert classification slide + footer)
- `skills/xlsx/` (auto-insert classification on print area)
- ALL new skills (inherit classification default per doc type)

## Notes

- This is the one skill that should be **strict** even when overall enforcement mode is "strong default, allow override." Classification exists for regulatory / legal reasons — overriding it should require explicit justification.
- If NDLNG uses Microsoft Purview / AIP / sensitivity labels, capture the label taxonomy — Claude can output docs pre-tagged.
- Suggested default for energy companies: **Internal** unless a clear case for other levels. "Public" should require positive confirmation (published material).
