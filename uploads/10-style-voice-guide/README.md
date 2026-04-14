# 10 — Editorial Style & Voice Guide

**Priority:** REQUIRED. This is the rulebook that makes every word of output sound like NextDecade.

## What to upload here

- [ ] Written editorial style guide (if one exists)
- [ ] Tone of voice guide / voice attributes
- [ ] Terminology glossary (approved terms, forbidden terms, preferred phrasings)
- [ ] Acronym / abbreviation dictionary (NDLNG-specific and industry)
- [ ] Grammar preferences (Oxford comma? em dash vs. en dash? serial comma?)
- [ ] Capitalization rules (project names, phases, titles, departments)
- [ ] Punctuation rules (quotation marks, dashes, ellipses)
- [ ] Number / date / time / currency formatting rules
- [ ] Unit conventions (MMBtu, MTPA, Bcf/d, tCO2e — exact formatting)
- [ ] People / title conventions (Dr. vs. first names, title capitalization)
- [ ] How to refer to the company (NextDecade vs. NextDecade Corporation vs. NDLNG vs. "the Company")
- [ ] How to refer to projects (Rio Grande LNG Facility? RGLNG? Rio Grande LNG Project?)
- [ ] Do / don't word lists
- [ ] Examples of on-voice vs. off-voice writing

## File types expected

`.pdf`, `.docx`, `.md`, `.xlsx` (for terminology dictionary)

## What Claude will extract — this is the biggest extraction

### Brand voice attributes
- 3–5 voice attributes (e.g., "confident but not arrogant," "technical but accessible")
- How attributes manifest in actual writing

### Terminology (exact strings)
- Approved product / project / facility names
- Approved abbreviations and when to use them (first-use full, subsequent abbreviated)
- Forbidden terms and approved replacements (e.g., "natural gas" vs. "gas"; "facility" vs. "plant"; "workforce" vs. "manpower")
- Industry terms with specific NDLNG preferences

### Mechanics
- Oxford comma preference
- Dash conventions (em / en / hyphen)
- Quotation style (curly vs. straight, double vs. single)
- Apostrophe / possessive style (NextDecade's vs. NextDecade')
- Capitalization rules for titles, project phases, regulatory terms

### Numbers
- How to write dates (March 15, 2026 vs. 15 March 2026 vs. 3/15/26)
- Time format (3:00 p.m. CT vs. 15:00 CST)
- Currency (US$ vs. USD vs. $; commas, decimals)
- Large numbers (million vs. M vs. MM; billion vs. B vs. Bn)
- Percentages (25% vs. 25 percent)
- Units: MMBtu, MTPA, Bcf/d, $/MMBtu — exact format with/without spaces

### References
- Company self-reference conventions
- Project reference conventions
- Legal entity references (when to use full legal name)
- Third-party references (customers, partners, regulators — with/without abbreviation)

## Feeds these skills

- `skills/internal-comms/` (voice becomes the default)
- `skills/doc-coauthoring/` (voice coaching)
- `skills/docx/` (style defaults)
- `skills/pptx/` (slide headline conventions)
- ALL new skills (voice inherits everywhere)

## Notes

- If no formal style guide exists, upload the closest proxies:
  - A senior comms/IR person's editing history
  - "Approved messaging" documents
  - Crisis response playbook
  - Recently-edited press releases with track-changes on (editing patterns reveal style rules)
- If different audiences get different voices (e.g., investor vs. community), note that — Claude will build audience-specific voice profiles
