# 12 — Regulatory Filing Samples

**Priority:** Recommended. Unlocks automated regulatory comms support.

## What to upload here

Sample / redacted filings showing NDLNG's formatting and language conventions for each regulator.

### FERC (Federal Energy Regulatory Commission)
- [ ] Application / amendment filings (Rio Grande LNG, CP2 Brownsville)
- [ ] Environmental resource reports
- [ ] Response to data requests
- [ ] Notice of intent / pre-filing materials
- [ ] Progress / status reports

### DOE (Department of Energy / FE)
- [ ] Non-FTA / FTA export authorization filings
- [ ] Annual export reports
- [ ] Capacity authorization correspondence

### PHMSA (Pipeline & Hazardous Materials Safety Administration)
- [ ] Safety-related filings
- [ ] Incident reports (redacted)
- [ ] Regulatory correspondence

### MARAD / USCG
- [ ] Port / waterway / maritime filings
- [ ] COTP notifications

### SEC
- [ ] 10-K (annual report) excerpts — risk factors, MD&A, business section
- [ ] 10-Q excerpts
- [ ] 8-K examples (by category: material agreements, financing, personnel, project milestones)
- [ ] Proxy statement sections
- [ ] Registration statement excerpts
- [ ] Comment letter responses

### State / local
- [ ] TCEQ (Texas Commission on Environmental Quality) air quality, water
- [ ] Louisiana DEQ (for Calcasieu Parish / CP2)
- [ ] Cameron County / Calcasieu Parish local filings

### Other federal
- [ ] EPA filings (Title V, NSR, NAAQS-related)
- [ ] USACE (Army Corps of Engineers) — Section 404 permits
- [ ] USFWS (Fish & Wildlife Service) — ESA consultations

## File types expected

`.pdf`, `.docx` (if original source available)

## What Claude will extract

- Cover page / docket reference formatting for each regulator
- Standard sections required by each filing type
- Citation conventions (18 CFR § 157.xx for FERC; 10 CFR § 590.xx for DOE; etc.)
- Regulatory language tone (more formal than corporate comms)
- Exhibit / appendix labeling
- Signature block format for each regulator
- Certification language patterns
- Submission cover letter format
- Response-to-data-request format

## Feeds these skills

- NEW: `skills/regulatory-comms/` (dedicated skill per regulator)
- `skills/docx/` (regulatory formatting variants)
- NEW: `skills/investor-relations/` (SEC filing patterns)

## Notes

- Regulatory writing has a distinct voice — much more formal, heavily cited, with specific legal constructions. Samples help Claude not bleed corporate voice into regulatory submissions.
- Include a brief "notes to Claude" file for each regulator if you have preferences (e.g., "FERC prefers active voice except in certifications")
- For SEC filings, the Safe Harbor language in 11-legal-boilerplate will be paired with actual filing structure from here
