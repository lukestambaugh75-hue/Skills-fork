# 02 — Typography & Fonts

**Priority:** REQUIRED. Templates can't render correctly without the actual fonts.

## What to upload here

- [ ] Actual font files: `.ttf`, `.otf`, `.woff`, `.woff2`
- [ ] Font licensing documentation (critical for distribution rights inside the enterprise)
- [ ] Type scale specification (H1 size, H2 size, body, caption, etc.)
- [ ] Pairing rules (which font for headings vs. body vs. UI vs. print)
- [ ] Fallback stack for web/email (e.g., if Aktiv Grotesk → Arial → sans-serif)
- [ ] Line height, letter spacing, paragraph spacing defaults
- [ ] Italic / bold usage rules
- [ ] Drop cap / pull quote treatments if used

## File types expected

`.ttf`, `.otf`, `.woff`, `.woff2`, plus any `.pdf`/`.docx` with type specs

## What Claude will extract

- Font family names (exact strings, case-sensitive, as they'll appear in `docx`/`pptx` XML)
- Full weight/style inventory (Thin / Light / Regular / Medium / Bold / Black; Italic variants)
- Approved type scale with point sizes for each heading level and body
- Pairing logic encoded as rules ("headings: Font A, body: Font B, data: Font C")
- Fallback stack (what to substitute if the licensed font isn't installed)
- Letter spacing / tracking for headlines vs. body
- Default line height multiplier

## Feeds these skills

- `skills/brand-guidelines/` (typography section)
- `skills/docx/` (default Paragraph style fonts + sizes, Heading1/2/3 specs)
- `skills/pptx/` (slide master font definitions)
- `skills/xlsx/` (header/body cell font defaults)
- Any new skill that emits formatted text

## Notes / gaps to flag

- If only desktop fonts licensed but not web: Claude will advise on web-safe fallbacks
- If font is custom/proprietary: document licensing scope (internal only? partner share? public?)
- Pre-install instructions will be generated for the enterprise so skills render identically across workstations
