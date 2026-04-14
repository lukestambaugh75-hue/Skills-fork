# 20 — Org Chart, Email Signatures & Exec Bios

**Priority:** Recommended. Low effort, enables personalized comms output.

## What to upload here

### Email signatures
- [ ] Corporate email signature template (the approved HTML or Word format)
- [ ] Signature variants: full (external), shorter (internal), mobile
- [ ] Legal disclaimer block in signatures
- [ ] Approved photo / logo dimensions
- [ ] Approved social links (LinkedIn, Twitter/X, company page)
- [ ] Color / font specs for signature text
- [ ] Examples for: executive / manager / individual contributor

### Exec bios
- [ ] Board member bios (as shown on website and proxy)
- [ ] Executive officer bios (CEO, CFO, COO, GC, CTO, CCO, etc.)
- [ ] Short / medium / long versions of each bio
- [ ] Headshot filenames matching each bio
- [ ] Background-info / talking-point variants (for comms, IR, media)

### Org chart / structure
- [ ] Current org chart (at the level appropriate for template sharing)
- [ ] Department / function list
- [ ] Job title conventions (VP vs. Vice President, SVP, EVP usage)
- [ ] Business unit names (RGLNG, CP2, NCS, Corporate)

### Conference / speaker
- [ ] Speaker bio format for conferences
- [ ] Executive biography for moderated panels
- [ ] "About the speaker" short version

## File types expected

`.html`, `.docx`, `.pdf`, `.png`/`.jpg` (headshots), `.txt`

## What Claude will extract

- Exact email signature template (HTML + text)
- Signature fields (name, title, phone, email, address, social)
- Legal disclaimer verbatim
- Bio length conventions (short / medium / long — word counts)
- Title capitalization / punctuation conventions
- Department names and their preferred rendering
- How exec hire / promotion announcements are structured
- Bio "signature phrases" (e.g., how CEO's background is typically opened)
- Org unit naming (NDLNG Corporate vs. NDLNG Operations, etc.)

## Feeds these skills

- NEW: `skills/email-signatures/` (generates correct signature for any employee)
- NEW: `skills/exec-bios/` (returns exec bio at requested length)
- `skills/internal-comms/` (leadership announcement formats)
- `skills/pptx/` (speaker bio slides for decks)

## Notes

- If exec bios are already on the public website, Claude can reference and match them — but having local authoritative copies avoids scraping and ensures consistency
- For non-public employees: do not upload PII. Keep this to public-facing roles or template-level (e.g., "EVP of Operations" not named individual)
