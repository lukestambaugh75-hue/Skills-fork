# NextDecade LNG — Extracted Specifications

Source: `NextDecade-Claude-Project/01-brand-references/` and `NextDecade-Claude-Project/03-original-templates/` (5 artifacts). Generated from a first-pass extraction of the brand PDF, three .docx templates, the .potx slide master, the writing style guide PDF, and the HSSE flash deck. Treat every value as **claude-extracted, not yet human-confirmed** — review and correct before propagation into `/skills/`.

---

## 1. Corporate identity

| Item | Value | Source |
|---|---|---|
| Legal entity | NextDecade Corporation | brand p.1, style guide footer (every page) |
| Short name | NextDecade | style guide §5.1 |
| Stock symbol | NASDAQ: **NEXT** | PPTX disclaimer slide |
| HQ address | 1000 Louisiana Street, Suite 3900, Houston, Texas 77002 USA | PPTX disclaimer slide |
| Website | www.next-decade.com | PPTX back cover |
| Tagline | **"Delivering Energy for What's NEXT"** | PPTX cover + back cover |
| Mission line (footer; canonical) | "NextDecade Corporation (NextDecade) is committed to providing the world access to lower carbon intensive energy through **Rio Grande LNG** & NEXT Carbon Solutions." | ruling: spell out RGLNG (style guide §5.1 wins) |

**Resolved**: footer mission line is forced to "Rio Grande LNG" (spelled out). The brand PDF's "RGLNG" abbreviation is superseded — to be corrected in the next brand-PDF revision.

## 2. Brand architecture

Three brands, each with its own logo (horizontal primary + vertical/stacked secondary):

| Brand | Code | Logo background rules | Notes |
|---|---|---|---|
| NextDecade Corporate | (parent) | white / navy / orange | Logo includes "NextDecade Knot" mark; mark used solo only with Comms approval |
| Rio Grande LNG | RGLNG | white / navy / orange (navy may flip to white on dark bg with approval) | LNG facility brand |
| NEXT Carbon Solutions | NCS | white / **green** | CCS business; uses a *variant* of the Knot |

Naming preference (style guide §5.1): **never abbreviate the parent as "ND" or "NEXT"**. "NEXT" refers only to the NASDAQ ticker.

## 3. Color system

### 3a. Brand-PDF spec (the "source of truth")

| Role | Hex | RGB | CMYK | Pantone |
|---|---|---|---|---|
| Primary navy | **#002060** | 0/32/96 | 100/75/30/35 | 534 C |
| Primary orange | **#FC7134** | 252/113/52 | 0/75/86/0 | 1645 C |
| Primary green | **#00B050** | 0/176/80 | 80/5/100/0 | 361 C |

Usage rule: Pantone preferred → CMYK for 4-color print → Hex for digital → RGB for Word/PowerPoint.

### 3b. PPTX theme (`theme1.xml`, scheme name "Custom 1") — patched

| Slot | Hex | Brand-spec match | Notes |
|---|---|---|---|
| dk1 / Text | #000000 | yes | black |
| lt1 / Background | #FFFFFF | yes | white |
| dk2 | #002060 | yes | brand navy |
| accent1 | #002060 | yes | brand navy |
| accent2 | **#FC7134** | yes | **brand orange (patched 2026-04-14, was #ED7D31)** |
| accent3 | #9CC3E5 | n/a | secondary tint, ignored per brand decision |
| accent4 | #00B0F0 | n/a | secondary tint, ignored per brand decision |
| accent5 | #A8D08D | n/a | secondary tint, ignored per brand decision |
| accent6 | #C55A11 | n/a | secondary tint, ignored per brand decision |
| hlink | #0563C1 | n/a | default Word blue |

**Resolved**: brand orange forced into accent2. Secondary accent3–6 colors are not in the brand book but are retained as-is per brand decision (do not modify, do not promote, do not flag). Brand green #00B050 is not in the theme; if needed in a deck it should be applied as a per-shape fill.

### 3c. DOCX themes

All three .docx templates now use **Segoe UI** (major and minor) and **Heading 1–4 colors set to #002060 navy**, patched 2026-04-16 at the theme and style layer in both Jinja templates (`skills/docx/templates/`, `NextDecade-Claude-Project/02-templates/`) and the walk-and-replace source templates (`NextDecade-Claude-Project/03-original-templates/`). Previously the templates inherited the Office default (Aptos/Aptos Display, heading teal #0F4761); that chrome was replaced so rendered output matches the brand regardless of which render path (docxtpl or walk-and-replace fallback) is taken.

**Inconsistency #3 (medium)**: ~~.docx templates carry NDLNG chrome but underlying theme is Office default~~ — **RESOLVED 2026-04-16**: theme fonts patched to Segoe UI and Heading 1–4 colors patched to #002060. Logo / footer / header / governance chrome were already correct.

## 4. Typography

### 4a. Brand-PDF spec

| Role | Family | Notes |
|---|---|---|
| Everyday communications | **Segoe UI** | "installed on most people's computers" |
| Display variants | Segoe / Segoe Light / Segoe Bold | shown as samples |
| Source of font files | Corporate Comms Dept (no font files in repo) | |

### 4b. Writing-style-guide spec (§5.4)

- **Headlines**: Segoe UI, "Blue, Accent 1, Darker 50%", **20pt**
- **Subheads**: Segoe UI, "Blue, Accent 1, Darker 50%", **16pt**
- **Body**: unbold black, **11pt**

### 4c. PPTX theme actually shipping

- Major + minor font: **Segoe UI** ✓ (matches spec)
- Slide master also references "Arial" as a fallback (residual)

### 4d. DOCX templates actually shipping

- Theme major: **Segoe UI** | minor: **Segoe UI** (patched 2026-04-16) — matches spec ✓
- Heading 1–4: color **#002060 navy** (patched 2026-04-16) — matches spec ✓
- Body runs: Body Text style defers to theme fonts (Segoe UI); no hardcoded Times New Roman remains at the style level.

**Inconsistency #4 (material)**: ~~Word templates ignore the Segoe UI brand standard~~ — **RESOLVED 2026-04-16**: theme and heading-color layers patched in both Jinja and walk-and-replace-source templates. Any remaining body-run font overrides (e.g., Times New Roman in direct formatting on individual runs in the source documents) would still surface in the rendered output; none were observed in the shipping templates.

## 5. Voice & writing style

### 5a. Two registers

| Audience | Register | Markers |
|---|---|---|
| Internal (employees) | **Casual / informal** | Inclusive pronouns "us / we / our"; contractions "it's, that's, we've"; "relatable, honest, transparent" |
| External (public, investors, media, regulators, community, analysts) | **Formal** | No contractions ("it is, that is"); reference disciplines ("engineering team," "NextDecade's engineers"); "NextDecade employees/people" |

### 5b. Style/usage rules (style guide §5)

- **Acronyms**: Spell out on first reference, parens, then abbreviate. Skip parens if the term is used only once.
- **Company name**: Always full "NextDecade." **Never** abbreviate to "ND" or "NEXT". "NEXT" = NASDAQ ticker only.
- **Months**: Spell out as standalone period; with a date use Jan., Feb., March, April, May, June, July, Aug., Sept., Oct., Nov., Dec. (don't abbreviate the short ones).
- **Dates**: Always 4-digit year ("Jan. 5, 2023") for archive/audit.
- **Times**: a.m. / p.m. (lowercase, periods). Drop repeat abbreviation if start and end are same period.
- **Titles**: Capitalize employee titles in all positions ("Director of Corporate Communications Jane Doe" or "Jane Doe, Director of Corporate Communications").
- **Distribution format**: Save informal docs as **PDF when possible** to prevent edits; informal naming convention should not embed version/date — put version in the footer.
- **Headlines**: short, engaging, action-oriented. Creative play on words OK internally.
- **Photo captions**: short and engaging; identify people with full first/last name + title; do not state the obvious.

### 5c. Channels documented

Internal: Intranet, NEXT digest (monthly newsletter), e-mail (with department banner template), digital screens, town halls, lunch-and-learns, info sessions, SWAG.
External: next-decade.com, LinkedIn, Facebook, X (Twitter), conferences, recruiting, community presence, IR/analyst meetings, event sponsorships, media (1:1 exec interviews), fact sheets, brochures, white papers, promo items.

### 5d. Defined products / phrasing

- "Rio Grande LNG Facility" / "Rio Grande LNG" / "RGLNG" are all in use; preferred external = spell out.
- "lower carbon intensive energy" (verbatim brand phrase, used in footer)
- "carbon capture and storage (CCS)" — defined acronym
- "liquefied natural gas (LNG)" — defined acronym
- "Workforce" capitalized in document templates as defined term

## 6. Logo & mark rules

- Three "do not"s explicit in brand PDF: don't outline, don't distort dimensions, don't use over busy/gradient backgrounds.
- Minimum clear space on apparel/promo: **¼ inch** around the logo.
- Knot mark used standalone requires Corporate Comms approval.
- All logo questions → Corporate Communications Dept (no logo files included in upload — only the rules PDF).

## 7. E-mail signature

- Uniform signature required across all teams.
- Two formats specified: Desktop and Mobile (no text content extracted — they were images).
- Source-of-truth Word file lives on Policy & Corporate Affairs intranet.
- IT updates via ithelp@next-decade.com.
- Mobile signature uses the assigned company mobile number when issued.
- (No actual signature template was uploaded in `20-org-signatures/`.)

## 8. Document architecture (DOCX templates)

### 8a. Page setup (identical across all three)

- Letter, **8.5 × 11 in**, portrait
- Margins: **1.0 in** all sides; header **0.5 in**, footer **0.5 in**
- 4 sections (cover / TOC / body / appendix structure implied)

### 8b. Three governance document types

All three templates carry the **NextDecade logo** as an embedded PNG in the header (the "308444 41275" numbers I initially read as text were drawing-anchor coordinates for the logo image), plus a cover-page graphic and a watermark — all already inside the .docx, so any output produced from these templates inherits the brand chrome automatically.

| Type | Purpose statement | Header | Footer |
|---|---|---|---|
| **Standard** | Mandatory levels of quality & expectations | NextDecade logo + "NextDecade Corporation \n [Name] Standard" | "NextDecade Corporation Standard Document … PAGE x" |
| **Procedure** | Step-by-step instructions, mandatory compliance | NextDecade logo + "dd-mmm-yyyy [PROCEDURE Document NAME] Rev.: x  Doc. No. xxx-xxx-xxx-xxx-xxx-#####" | "NextDecade Corporation Procedure Document … PAGE x" |
| **Guidance** | Best-practice recommendations (advisory) | NextDecade logo + "dd-mmm-yyyy [GUIDANCE Document NAME] Rev.: x  Doc. No. xxx-xxx-xxx-xxx-xxx-#####" | "NextDecade Corporation Guidance Document … PAGE x" |

### 8c. Document section skeleton (canonical order)

1. PURPOSE
2. SCOPE (Procedure/Standard) — Guidance combines into Purpose
3. INTEGRATED GOVERNANCE FRAMEWORK
4. DEFINITIONS (Procedure/Standard)
5. REFERENCES AND RELATED DOCUMENTS
6. [CONTENT TITLE] (one or more)
7. EXCEPTION REQUEST AND COMPLIANCE AUDITS *(Standard only)*
8. CONTINUOUS IMPROVEMENT AND REVIEW *(Standard only)*
9. OWNERSHIP
10. APPROVAL
11. REVISION HISTORY

### 8d. Required tables in every doc

- **Definitions**: No. | Term | Definition (5 rows)
- **References**: Title | Document Number (5 rows)
- **RACI**: Responsible | Accountable | Consulted | Informed (1 data row)
- **Approval**: Issuer/Title | Adopted By | Effective/Amended Date (with "s/" signature column)
- **Revision History**: Revision | Description of Changes and Notes (26 rows)

### 8e. Defined terms used in templates

- "Workforce" = employees, officers, directors, agents, consultants, contractors, representatives, and any other individuals acting on behalf of NextDecade.
- "Governance Framework" = NextDecade's integrated set of Standards / Procedures / Guidance.
- Quote conventions: smart quotes, em-dashes used.

## 9. Presentation architecture (PPTX master)

- Slide size: **16:9 widescreen** (13.333 × 7.5 in)
- 1 slide master, **50 layouts**, 32 embedded media assets (logos + photos)
- Font: **Segoe UI** (matches brand)
- 4 brand layout families:
  - **Cover**: layouts 1–2 ("Custom Layout" / "1_Custom Layout") — show tagline "Delivering Energy for What's NEXT" + editable title + editable date
  - **Public Disclaimer** (layout 3): full forward-looking-statements legal text + HQ address + page number — use as standard slide 2 of any external deck
  - **Back cover** (layout 4, "23_Custom Layout"): tagline + www.next-decade.com
  - **Content layouts**, repeated three times for the three brands:
    - **ND** (layouts 12–17): Blank, Single Narrative 18 Font, Dual Narrative, Tri Right, Tri Left, Quad
    - **RG** (layouts 24–29): Blank, Single, Dual, Tri Left, Tri Right, Quad
    - **NCS** (layouts 34–39): Blank, Single, Dual, Tri Right, Tri Left, Quad
  - ~30 additional "_Custom Layout" placeholders (numbered, no descriptive name) — likely picture/section dividers

### Forward-Looking Statements language (verbatim, captured)

The full FLS block from layout 3 is reproduced in `extracted-specs-fls.md` companion (saved verbatim — too long for this summary). Key phrases include the canonical Section 27A / 21E preamble, the mandatory "anticipate, assume, budget, contemplate…" trigger-word list, the FID/Terminal/Pipeline/CCS risk factor list, and the boilerplate that the Company "does not undertake any obligation to publicly correct or update any forward-looking statement."

## 10. HSSE Flash template

- One-slide format on the same 16:9 master.
- Standard fields: **Date & Time**, **Company**, **Category**, **Potential Consequence**, **Life Saving Rules**, **What Happened?**, **Immediate Action**, plus up to two photos.
- Mandatory photo disclaimer (when reenactments used): **"Note: photos are reenactments captured in a controlled environment."**
- Mandatory classification footer: **"Confidential and Proprietary – This document is intended solely for internal use. Unauthorized disclosure, distribution, or reproduction is strictly prohibited. Content is preliminary and subject to revision."**

## 11. Classification language (only one example surfaced)

Only one classification stamp is in evidence (the HSSE flash one above). No tier system (Public / Internal / Confidential / Restricted), no watermarks, no header/footer rules per tier, no rule for which doc-types default to which tier. **This is a major gap** (folder 18 still empty).

## 12. Approval & governance workflow (partial)

- Promotional items: minimum **5 weeks lead time** before event; checklist (contact Comms → confirm previously-approved item OR submit new for evaluation → consult on design → submit final design + vendor proof → submit production order → confirm receipt meets expectations).
- Document control: every Standard/Procedure/Guidance has an Issuer/Title, Adopted By (NextDecade Corporation), Effective/Amended Date, Doc. No. format `xxx-xxx-xxx-xxx-xxx-#####`, Revision number. Implies a Document Control function but workflow not described.

---
