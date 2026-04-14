# 05 — Presentation Templates (PowerPoint)

**Priority:** REQUIRED. This is one of the highest-impact skills — every exec deck flows through it.

## What to upload here

Upload the native `.pptx` templates (not PDF exports) so Claude can read the slide masters, theme, and layouts directly.

### Core deck templates
- [ ] Investor / analyst deck template
- [ ] Board of directors deck template
- [ ] Quarterly earnings deck template
- [ ] Executive leadership / internal deck template
- [ ] All-hands / town-hall deck template
- [ ] Sales / commercial deck template (for counterparty meetings)
- [ ] Project update deck template (Rio Grande LNG, CP2, etc.)
- [ ] Safety presentation template
- [ ] Regulatory / FERC / DOE presentation template
- [ ] Community / public meeting deck template
- [ ] Conference / keynote speaking template

### Slide layouts (usually inside the master)
If the templates have named slide masters/layouts, Claude will extract them. If you have a "layout library" slide separately, upload it.

## File types expected

`.pptx`, `.potx` (PowerPoint template format), `.thmx` (theme only)

## What Claude will extract

- Slide dimensions (16:9 widescreen vs. 4:3)
- Theme colors (all 12 theme color slots)
- Theme fonts (Latin + East Asian + Complex Script if set)
- Every named slide master / layout: Title, Section Header, Title + Content, Two Content, Comparison, Divider, Blank, etc.
- Logo placement on each layout (coordinates + size)
- Footer composition (page number position, classification label, date rules)
- Default placeholder positions (title, body, content)
- Bullet list style per layout
- Table style defaults
- Chart style defaults (this is huge — branded chart palettes go here)
- Divider / section slide treatments
- Cover and back-cover slides

## Feeds these skills

- `skills/pptx/` (full rewrite — defaults become NDLNG)
- `skills/brand-guidelines/` (deck examples section)
- NEW: `skills/investor-relations/` (investor deck conventions)
- NEW: `skills/data-visualization/` (chart style comes from here)

## Notes

- If you only have exported PDFs of decks, upload them to `08-sample-presentations/` instead — templates need to be native `.pptx`
- Include a "sample content" slide or two if possible — it helps Claude see how content fills the layouts in practice
- If different business units have different deck templates (e.g., IR vs. Commercial vs. Engineering), upload each and label the intended audience
