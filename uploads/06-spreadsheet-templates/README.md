# 06 — Spreadsheet Templates (Excel)

**Priority:** Recommended. Less often produced than docs/decks, but critical for financial and operational reporting.

## What to upload here

- [ ] Financial model template (blank structure)
- [ ] Budget / forecast template
- [ ] Variance report template
- [ ] Operational dashboard template (production, safety metrics, schedule)
- [ ] Board / investor metrics dashboard
- [ ] Project schedule / tracker template
- [ ] Risk register template
- [ ] KPI scorecard template
- [ ] Regulatory reporting workbook (if applicable)
- [ ] Any "house style" blank worksheet that has fonts/colors/borders pre-set

### Supporting material
- [ ] Number format conventions (currency, thousands separator, negative number treatment, decimal precision)
- [ ] Units conventions (MMBtu, MTPA, Bcf/d, $M vs. $MM vs. $B)
- [ ] Chart style reference if separate from the template

## File types expected

`.xlsx`, `.xltx` (Excel template format), `.xlsm` (macro-enabled only if needed)

## What Claude will extract

- Worksheet default font and size
- Number formats for currency, percentages, dates, units
- Cell styles (input / output / calculation / header / subtotal / total conventions)
- Named styles if defined
- Conditional formatting patterns
- Chart style defaults (palette matching brand, font for axis labels)
- Print setup (orientation, fit-to, headers/footers)
- Color palette for cells (if using brand colors vs. default Excel blue)
- Header row treatments (bold, fill, border)
- Freeze panes conventions

## Feeds these skills

- `skills/xlsx/` (full rewrite — defaults become NDLNG)
- NEW: `skills/data-visualization/` (chart defaults)
- NEW: `skills/investor-relations/` (IR metrics format)

## Notes

- Energy / LNG-specific unit conventions matter: include any cheat sheet showing how NDLNG formats MMBtu vs. Bcf/d vs. MTPA in official reporting
- If financial reports use a specific "house" format (e.g., $ in millions, parentheses for negatives, footnote conventions), include an example
- Upload one "finished" example alongside each blank template if possible — it's much easier to reverse-engineer style from a filled-in model
