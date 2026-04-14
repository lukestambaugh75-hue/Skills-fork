# 13 — Investor Relations Materials

**Priority:** Recommended. Critical for a publicly-traded company (NASDAQ: NEXT).

## What to upload here

### Earnings
- [ ] Most recent 2–4 earnings release scripts (CEO remarks, CFO remarks)
- [ ] Earnings call Q&A transcripts (or cleared-to-share excerpts)
- [ ] Earnings press release examples
- [ ] Prepared remarks / talking points for earnings

### Investor materials
- [ ] Current IR fact sheet / corporate overview
- [ ] Most recent investor presentation (covered in folder 08 but specific IR-approved version here)
- [ ] Analyst day materials
- [ ] Non-deal roadshow deck
- [ ] Company one-pager
- [ ] ESG / sustainability one-pager for investors

### SEC filings (overlap with folder 12)
- [ ] Recent 8-K examples by trigger event type
- [ ] 10-K / 10-Q management letters
- [ ] Proxy statement messaging sections

### IR operations
- [ ] Approved analyst Q&A / FAQ
- [ ] Material information policy
- [ ] Earnings blackout calendar / quiet period rules
- [ ] Guidance policies (do you provide guidance? what kind?)
- [ ] Non-GAAP reconciliation format
- [ ] Consensus estimate handling conventions

### Shareholder communications
- [ ] Annual shareholder letter
- [ ] Annual report narrative (shareholder-facing)
- [ ] Special situation letters (M&A, financing events)

## File types expected

`.docx`, `.pdf`, `.pptx`, `.txt` (scripts)

## What Claude will extract

- Earnings remarks structure (opening, business update, financials, outlook, Q&A bridge)
- CEO vs. CFO voice differentiation
- Approved phrasing for forward guidance (or non-guidance)
- How to talk about material events before / after disclosure
- IR fact sheet structure and required data points
- Non-GAAP measure treatment
- Safe harbor positioning (beginning vs. end)
- Analyst Q&A response patterns
- 8-K trigger language by category
- How to handle market-moving information (Reg FD)
- Quiet period / blackout language

## Feeds these skills

- NEW: `skills/investor-relations/` (dedicated full skill)
- `skills/pptx/` (IR deck defaults — crosslinks from folder 05)
- `skills/internal-comms/` (IR-aligned comms)
- NEW: `skills/legal-boilerplate/` (Reg FD, Safe Harbor)

## Notes

- IR is the most legally-sensitive comms function outside legal itself. The extracted skill should default to "produce draft, flag for IR + legal review" rather than allowing autonomous posting.
- Highlight any language that's "pre-approved — safe to use" vs. "must always be reviewed"
- If there's a specific analyst/investor FAQ bank that's been pre-approved by legal, upload it — Claude can use that directly without flagging for review
