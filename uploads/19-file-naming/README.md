# 19 — File Naming & Versioning

**Priority:** Recommended. Low cost to implement, high enterprise hygiene payoff.

## What to upload here

- [ ] File naming convention document (if one exists)
- [ ] Version numbering scheme (v1, v2 vs. v1.0, v1.1 vs. date-based YYYYMMDD)
- [ ] Examples of correctly-named files across doc types
- [ ] Folder / SharePoint / Drive organization conventions
- [ ] Metadata fields (if documents are required to have specific metadata)

### Naming element priorities (capture rules per doc type)
- [ ] Project / entity prefix (NDLNG, RGLNG, CP2, NCS)
- [ ] Document type abbreviation (Memo, Report, SOW, MSA, Deck)
- [ ] Date format (YYYY-MM-DD vs. MMM-YYYY)
- [ ] Author / team code (IR, HSE, LEGAL, COMM)
- [ ] Classification indicator in filename (PUB, INT, CONF, RES)
- [ ] Version suffix (v1, v2, FINAL, DRAFT)

## File types expected

`.pdf`, `.docx`, `.md`, `.txt`

## What Claude will extract

- Naming pattern per document type
- Date format preference
- Version scheme (monotonic? semantic? date-based? FINAL-suffix?)
- How "draft" vs. "final" is indicated
- Max filename length (if any — SharePoint has limits)
- Disallowed characters (spaces? slashes? special characters?)
- Required metadata fields (for tagging in DMS)

## Feeds these skills

- NEW: `skills/file-naming/` (dedicated skill — when Claude saves any file, it uses the convention)
- All file-producing skills inherit naming defaults
- Auto-suggests filename when any document is created

## Notes

- If no convention exists, Claude will propose one based on industry best practice and your typical document types. You'll review and approve before it's baked in.
- Suggested baseline convention: `{Project}_{DocType}_{Topic}_{YYYY-MM-DD}_{Version}_{Classification}.ext`
  - Example: `NDLNG_Memo_Board-Q4Update_2026-10-15_v2_CONF.docx`
- Some teams prefer sortable (date-first) vs. topical (topic-first) — capture the preference by context
