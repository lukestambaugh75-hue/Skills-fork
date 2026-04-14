# 08 — Sample Finished Presentations

**Priority:** Recommended. Last 2–3 investor / board updates are especially valuable.

## What to upload here

**⚠️ Redact material non-public information before uploading.** Especially for IR decks that contained forward-looking guidance.

### Examples to gather
- [ ] Most recent 2–3 investor / analyst decks
- [ ] Last 2–3 board decks
- [ ] Recent earnings / quarterly update decks
- [ ] Conference presentation decks (e.g., Gastech, CERAWeek, Wood Mackenzie)
- [ ] Customer / counterparty pitch decks
- [ ] Recent all-hands decks
- [ ] Safety / HSE presentations
- [ ] Town hall decks
- [ ] Regulatory briefing decks (FERC, DOE, PHMSA meetings)
- [ ] Community meeting decks (RGV, Calcasieu Parish)

## File types expected

`.pptx` (preferred — Claude can read layouts used, theme applied, charts) or `.pdf` (fallback)

## What Claude will extract

- Which slide layouts are actually used most (signals "the practical deck pattern")
- Title writing conventions ("What if..." vs. declarative vs. question)
- Content density per slide
- Use of speaker notes (if `.pptx` has them)
- Chart types actually used (bar / line / waterfall / Sankey / pie — and the ratio)
- Data labeling practices
- Footer content (date, classification, page numbering style)
- Disclaimer / safe harbor slide format (when included vs. omitted)
- Agenda slide conventions
- Section divider usage
- Back-cover / thank-you slide style
- Appendix conventions

## Feeds these skills

- `skills/pptx/` (practical defaults from real usage)
- NEW: `skills/investor-relations/` (IR deck conventions)
- NEW: `skills/safety-hse/` (safety deck patterns)
- NEW: `skills/community-stakeholder/` (community meeting patterns)

## Notes

- Natively `.pptx` is 10× more valuable than `.pdf` — always upload the source if available
- If redacting, leave structure intact and replace sensitive content with `[REDACTED]` rather than deleting slides — layout intelligence comes from structure
- Include the speaker notes if they exist — they often contain approved phrasing
