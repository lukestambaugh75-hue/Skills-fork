# 11 — Legal Boilerplate & Disclosures

**Priority:** REQUIRED. Getting these wrong has regulatory / legal consequences. Must be exact wording.

## What to upload here

### Forward-looking / safe harbor
- [ ] Current forward-looking statements language (the long paragraph that appears in press releases, 8-Ks, presentations)
- [ ] PSLRA safe harbor language
- [ ] Presentation-specific safe harbor slide text

### SEC / public company
- [ ] Reg FD compliance policies / language
- [ ] Selective disclosure guidelines
- [ ] Non-GAAP financial measure disclaimers
- [ ] Earnings release boilerplate blocks

### Confidentiality
- [ ] Internal confidentiality notices (header/footer text)
- [ ] NDA-protected content markers
- [ ] Trade secret / proprietary notices
- [ ] Attorney-client privilege notices

### Trademark & IP
- [ ] Trademark / service mark list (™, ®, SM notations)
- [ ] First-use TM conventions ("Rio Grande LNG®" on first reference)
- [ ] Copyright notice format (© 2026 NextDecade Corporation. All rights reserved.)
- [ ] "About NextDecade" boilerplate paragraph (the one at the bottom of press releases)

### Environmental / regulatory notices
- [ ] Environmental disclaimers
- [ ] Regulatory approval disclaimers (e.g., "subject to FERC approval")
- [ ] Project status qualifiers

### Other
- [ ] Email confidentiality footers
- [ ] External communication disclaimers
- [ ] Anti-trust compliance language (for commercial / partner meetings)
- [ ] Insider trading reminder language

## File types expected

`.pdf`, `.docx`, `.txt`

## What Claude will extract

Each boilerplate block is captured **verbatim** — no paraphrasing, because legal language's precision matters. Claude will store them in a structured library:

```
legal-boilerplate/
  forward-looking.md           # exact PSLRA-compliant paragraph
  safe-harbor-slide.md         # presentation-ready version
  reg-fd-statement.md
  non-gaap-disclaimer.md
  about-nextdecade.md          # press release boilerplate
  confidentiality-internal.md
  confidentiality-external.md
  trademark-notices.md
  copyright-notice.md
  email-footer.md
```

Each will be tagged with:
- When to use it (which document types / contexts)
- Who can modify it (legal approval required? or standard reusable?)
- Version / date last updated
- Related regulations (PSLRA, Reg FD, Reg G, etc.)

## Feeds these skills

- NEW: `skills/legal-boilerplate/` (dedicated skill that returns exact language)
- `skills/docx/` (footer / disclaimer auto-insert)
- `skills/pptx/` (safe harbor slide auto-insert)
- NEW: `skills/investor-relations/` (earnings/8-K language)
- `skills/internal-comms/` (press release footer)

## Notes

- **Critical:** Never paraphrase legal language. If uploaded, Claude stores and returns the exact version. If multiple versions exist (e.g., the FLS has evolved quarter over quarter), upload all and label with dates so Claude can use the most recent.
- Include a "legal review required" flag for any language that Claude should NOT auto-insert without a human lawyer approving. These become "template only — requires review" skills.
- If you have a legal-approved "messaging bank" (e.g., approved Q&A responses), this is the place.
