# 07 — Sample Finished Documents

**Priority:** Recommended. High-leverage — finished real artifacts reveal the actual (vs. documented) style.

## What to upload here

Real documents that have already been produced, reviewed, and distributed. More variety = better style model.

**⚠️ Redact anything sensitive first.** Strip material non-public info, customer names under NDA, personal data, financial detail you don't want exposed to this template library.

### Examples to gather
- [ ] Executive memos (internal and external-facing)
- [ ] Board memos / board packet content
- [ ] Project status reports (RGLNG, CP2, Next Carbon Solutions)
- [ ] Technical reports / engineering studies (redacted)
- [ ] White papers / thought leadership
- [ ] Annual report narrative sections
- [ ] SOPs / procedures in final form
- [ ] Meeting minutes (any recurring exec / board meeting)
- [ ] Briefing papers / backgrounders
- [ ] Letters (customer, regulator, community, investor)
- [ ] Policy documents (code of conduct, travel, etc.)
- [ ] Completed RFP responses / proposals

## File types expected

`.docx` (preferred — Claude reads styles directly), `.pdf` (fallback if `.docx` unavailable)

## What Claude will extract

- Real-world application of the document templates (how theory meets practice)
- Actual sentence / paragraph length distributions
- Voice markers: first-person plural vs. third-person, active vs. passive ratios
- Typical headline structure
- Transition phrases repeatedly used
- Signature block formats
- Footnote / endnote conventions
- How tables and figures are captioned and referenced
- Typical appendix structure
- Cross-reference patterns
- Acronym introduction conventions ("Rio Grande LNG Facility ('RGLNG Facility')")

## Feeds these skills

- `skills/docx/` (voice patterns, content patterns)
- `skills/doc-coauthoring/` (structural defaults)
- `skills/internal-comms/` (leadership voice)
- Multiple new skills (regulatory, IR, ESG, etc. — depends on document type)

## How to organize

If you're uploading a lot, organize into subfolders:
```
07-sample-documents/
  memos/
  reports/
  letters/
  policies/
  board/
  technical/
```

Label redacted ones so Claude knows what's been removed vs. what was never there.
