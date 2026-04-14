# 17 — Data Visualization & Chart Standards

**Priority:** Recommended. Charts are where branding most often breaks.

## What to upload here

### Chart examples
- [ ] Charts from IR decks (financial, operational)
- [ ] Dashboard examples (operational, safety, financial)
- [ ] Infographics
- [ ] Project schedule / Gantt examples
- [ ] Process flow / architecture diagrams

### Chart / viz standards (if documented)
- [ ] Chart palette (colors specifically for data viz — often differs from brand palette)
- [ ] Axis / label fonts and sizes
- [ ] Data label conventions (units, formatting, position)
- [ ] Gridline rules (horizontal yes, vertical no? minor gridlines?)
- [ ] Legend placement
- [ ] Chart title conventions
- [ ] Source / footnote conventions

### Specific chart patterns
- [ ] Financial: revenue bars, margin lines, waterfall for earnings bridges
- [ ] Operational: production curves, safety metrics (TRIR over time)
- [ ] Schedule: Gantt, milestone timeline
- [ ] Geography: Rio Grande LNG site map, facility diagrams
- [ ] Comparison: peer benchmarking charts

### Infographics
- [ ] Process flow style examples (feedstock → liquefaction → loading → shipping)
- [ ] Map illustration style
- [ ] Icon-based infographic samples

## File types expected

`.pptx`, `.xlsx` (with source charts), `.pdf`, `.png`, `.ai`, `.svg`

## What Claude will extract

- Chart color palette (often a subset or extension of the brand palette, optimized for data)
- Color assignments for categorical data (e.g., Rio Grande LNG always blue, CP2 always green)
- Font family and size for chart text
- Axis treatment (tick marks, minor/major gridlines, scale conventions)
- Data label positioning and formatting
- Legend conventions (top, bottom, right?)
- Source line format ("Source: Company data as of Dec 31, 2026")
- Unit placement (y-axis label? data labels? both?)
- Diverging vs. sequential color choices
- Accessibility considerations (colorblind-safe pairs)

## Feeds these skills

- NEW: `skills/data-visualization/` (dedicated skill)
- `skills/pptx/` (chart defaults)
- `skills/xlsx/` (chart defaults)
- NEW: `skills/investor-relations/` (IR-specific chart conventions)

## Notes

- Brand palettes rarely work directly for data viz — too few colors, too much contrast, not colorblind-safe. Most enterprises have a distinct "data palette" that extends the brand. Capture it if it exists.
- If no data palette is documented, Claude will derive one from brand colors + accessibility rules and propose it as a starting point for your team to approve.
- Include "bad" chart examples with notes on why they violate standards — super useful training material.
