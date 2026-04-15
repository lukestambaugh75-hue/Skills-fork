# Gap Analysis — Document-Type Validation Sample Set

**Audit date:** 2026-04-15
**Scope:** `samples/document-types-validation/` (15 artifacts, 5 subfolders), plus the `/skills/` folder and `/uploads/` intake against `extracted-specs.md` and `gap-report.md`.
**Purpose:** Tell the user what's still missing, what it costs them if unfixed, and what the smallest credible step is to close each item.

---

## Executive summary

The sample set demonstrates **solid foundational execution** — typography, brand color, voice register, classification footers, and the core document layouts are all correct and consistent with `extracted-specs.md`. But the audit surfaces **five material gaps** that prevent a NextDecade user from producing a complete, production-ready artifact library without manual intervention.

- **2 gaps are HIGH severity** — missing regulatory-comms and ESG-reporting skills (compliance + disclosure risk).
- **4 gaps are MEDIUM** — letterhead/logo on business docx, bilingual EN-ES comms, file-naming enforcement, incident-escalation templates.
- **Remainder are LOW / process** — defined-term consistency, theme-vs-run typography, approval workflow policy.

**The single biggest lever:** 5 of the 12 skill-coverage gaps can be closed **in code alone** (no user uploads required). 7 others are blocked on specific folder uploads that are still empty.

---

## 1. Coverage gaps — artifact types still missing

| Artifact category | Status | Severity | Effect on user |
|---|---|---|---|
| Regulatory filings (FERC / DOE / PHMSA / SEC 8-K / 10-Q) | **Not in sample set** | **HIGH** | IR drafts manually; Reg FD exposure; every filing cycle rework |
| Bilingual EN-ES community materials | **Not in sample set** | MEDIUM | Community team hand-translates; RGV stakeholder message drift |
| ESG / sustainability (GRI / SASB / TCFD / CCS narrative) | **Not in sample set** | **HIGH** | Sustainability team reuses prior-year templates; disclosure completeness gaps; third-party verifier rework |
| SEC 10-K / 10-Q excerpts | **Not in sample set** | HIGH | Periodic-reporting boilerplate not NDLNG-specific; drafting overhead at every quarter close |
| Incident-escalation comms (beyond HSSE-Flash) | **Partial** (HSSE-Flash present) | MEDIUM | No crisis-comms playbook; message discipline at risk during real event |
| Data-room index (M&A due-diligence catalog) | **Not in sample set** | LOW-MEDIUM | BD team hand-assembles indexes; version/confidentiality control weak |
| File-naming + doc-number stamp | **Not in sample set** | MEDIUM | `xxx-xxx-xxx-xxx-xxx-#####` pattern unenforced; audit trail gap |
| Email signatures (desktop + mobile + exec bio) | **Not in sample set** | MEDIUM | No signature tool; inconsistent external email footprint |
| Letterhead on business DOCX | **Placeholder** (text in build scripts) | MEDIUM | Customer-facing letters, press release, fact sheet appear generic |

**Fix path:**
- **User-side (uploads required):** folders 12, 13, 15, 16, 19, 20 — plus a real letterhead PNG into folder 04.
- **Claude-side (code):** once uploads arrive, I can generate skills + add artifacts to the sample set in one pass.

---

## 2. Skill coverage gaps — personalization status

| Skill | SKILL.md? | Personalized to NDLNG? | Status |
|---|---|---|---|
| `docx/` | ✓ | ✓ partial (procedure pipeline personalized; standard/guidance partially) | READY |
| `xlsx/` | ✓ | ✓ | READY |
| `pptx/` | ✓ | ✗ | **NEEDS REWRITE** |
| `internal-comms/` | ✓ | ✗ | **NEEDS REWRITE** |
| `brand-guidelines/` | ✓ | ✗ still Anthropic-generic | **NEEDS REWRITE** |
| `doc-coauthoring/` | ✓ | ✗ | **NEEDS REWRITE** |
| `safety-hse/` | ✗ no folder | — | **CREATE** |
| `legal-boilerplate/` | ✗ no folder | — | **CREATE** |
| `classification/` | ✗ no folder | — | **CREATE** |
| `regulatory-comms/` | ✗ no folder | — | CREATE (blocked on folder 12 upload) |
| `investor-relations/` | ✗ no folder | — | CREATE (blocked on folder 13 upload) |
| `community-stakeholder/` | ✗ no folder | — | CREATE (blocked on folder 15 upload) |
| `esg-reporting/` | ✗ no folder | — | CREATE (blocked on folder 16 upload) |
| `data-visualization/` | ✗ no folder | — | CREATE (blocked on folder 17 upload) |
| `file-naming/` | ✗ no folder | — | CREATE (blocked on folder 19 policy) |
| `email-signatures/` | ✗ no folder | — | CREATE (blocked on folder 20 assets) |

**Severity:** HIGH in aggregate. 5 skills already exist but are still generic; 10 required skills either don't exist or can't be finalized without uploads.

**Effect:** Today, asking Claude to "draft a board deck" returns a typographically correct result that doesn't reference the NDLNG style guide or voice rules — because the `pptx` and `internal-comms` SKILL.md files don't tell Claude those rules exist. Asking for "an 8-K" returns a generic template because `regulatory-comms/` doesn't exist.

**Fix path — purely code (no uploads needed), ranked by impact:**
1. Rewrite `pptx/SKILL.md` to reference the .potx master, layout-index map, FLS disclaimer layout, and `#FC7134` color lock.
2. Rewrite `internal-comms/SKILL.md` to embed §5 voice rules, terminology list (RGLNG spelled out, never "ND"), channel list, acronym-on-first-use rule.
3. Rewrite `brand-guidelines/SKILL.md` — replace Anthropic colors/fonts with NDLNG specifics + brand architecture (parent / RGLNG / NCS).
4. Rewrite `doc-coauthoring/SKILL.md` — start every draft from a NDLNG template.
5. Create `safety-hse/`, `legal-boilerplate/`, `classification/` as minimal-scaffolding skills using already-captured specs (HSSE Flash template; FLS verbatim from .potx disclaimer; working classification stamp).

---

## 3. Fidelity gaps inside the artifacts just produced

### 3a. Logos & images

| Artifact group | Issue | Severity |
|---|---|---|
| Governance DOCX (01-) | ✓ Logo inherited from template clone | — |
| Business DOCX (02-) | Text-rendered brand header instead of real logo PNG | MEDIUM |
| PPTX decks (03-) | Master holds logos but explicit logo shapes not verified on each content slide | MEDIUM |
| XLSX (04-) | No logo in header; mission line is text | LOW-MEDIUM |

**Fix:** Drop the real letterhead PNG into `samples/document-types-validation/_build/assets/` and update `nextdecade_brand.py` to `add_picture(...)` at top of first page. ~30 min of code; requires the image file from you.

### 3b. Voice-register correctness (spot-check)

| Register | Should have contractions? | Artifact checked | Result |
|---|---|---|---|
| Formal external | No | Press Release | ✓ clean |
| Formal external | No | Customer Letter | ✓ clean |
| Formal internal | No | Board Memo, Meeting Minutes | ✓ clean |
| Casual internal | Yes | All-Hands Email | ✓ uses "we're", "it's", "we've" |
| Casual internal | Yes | NEXT Digest | ✓ uses contractions |

**No gap here — register rules are being applied correctly.**

### 3c. Defined-term propagation

"Workforce" and "Governance Framework" are defined in governance docs (01-) but **not used** in business docs (02-) that discuss the same org structure. This is a **style enforcement miss**, not a bug.

**Severity:** LOW-MEDIUM. **Fix:** audit and lightly edit the business-docx builders to use the defined terms where they apply.

### 3d. Theme-level typography

DOCX templates still ship with the Aptos / Times New Roman Office default theme. Body text is correct because `nextdecade_brand.py` overrides at the run level, but the theme layer is off-brand — known gap from `extracted-specs.md` §4c / `gap-report.md` §1b.

**Severity:** LOW (invisible to user in normal use). **Fix:** swap theme XML inside templates — optional backlog item.

### 3e. What's not classification-stamped

| Artifact | Stamp | Correct? |
|---|---|---|
| Board Memo, Meeting Minutes, Customer Letter, All-Hands, Newsletter, Governance docs, XLSX | "Confidential and Proprietary…" | ✓ |
| Press Release | none | ✓ (public) |
| Fact Sheet | none | ✓ (public) |
| HSSE-Flash (existing sample) | "Confidential and Proprietary…" | ✓ |

**No gap** — classification coverage is consistent. But note: **the tier system itself is still undefined** (Public / Internal / Confidential / Restricted). That lives in `gap-report.md` as the single major outstanding item from folder 18.

---

## 4. Process / governance gaps

| Gap | Severity | Effect |
|---|---|---|
| Classification tier system not yet defined (only one stamp in use) | **HIGH** | Users have no rule for which doc type defaults to which tier; "Confidential" is being applied universally by default, which is both over-stamping some and under-stamping others |
| No documented approval workflow for artifacts | MEDIUM | Users don't know who signs off on a board memo, press release, or investor deck before it ships |
| No version/change-log on business-docx artifacts (governance docs do carry it) | LOW-MEDIUM | Q1 memo → Q2 memo leaves no audit diff |
| No accessibility audit (alt text, contrast, WCAG) | MEDIUM | Logos have no alt text; screen-reader users get nothing |
| PDF export path unproven in this sandbox (LibreOffice / soffice crashes) | LOW-MEDIUM | Users must export manually; no guarantee brand chrome survives some export paths |

**Fix path:** these are **policy** items, not code. You draft the rules; I encode them into skills and templates.

---

## 5. Severity matrix (prioritized fix order)

| # | Gap | Severity | Unblocked by | Effort |
|---|---|---|---|---|
| 1 | Classification tier system (Public/Internal/Confidential/Restricted) not defined | HIGH | Policy from you | Policy: 1 hr. Code: 2 hr. |
| 2 | `regulatory-comms/` skill missing | HIGH | Folder 12 uploads | Policy + 4-6 hr code |
| 3 | `investor-relations/` skill missing | HIGH | Folder 13 uploads | 4-6 hr code |
| 4 | `esg-reporting/` skill missing | HIGH | Folder 16 uploads | 4-6 hr code |
| 5 | `pptx`, `internal-comms`, `brand-guidelines`, `doc-coauthoring` generic (not NDLNG-personalized) | HIGH | **None — code only** | 4-8 hr code |
| 6 | Business DOCX lacks real letterhead logo | MEDIUM | Folder 04 PNG | 30 min once PNG lands |
| 7 | `community-stakeholder/` missing (bilingual EN-ES) | MEDIUM | Folder 15 uploads | 6-10 hr code |
| 8 | Incident-escalation templates (beyond HSSE-Flash) | MEDIUM | Folder 14 extension | 2-4 hr code |
| 9 | `safety-hse/`, `legal-boilerplate/`, `classification/` skills don't exist but specs already captured | MEDIUM | **None — code only** | 3-5 hr code |
| 10 | `file-naming/` skill + doc-number enforcement | MEDIUM | Folder 19 policy | 2-3 hr code |
| 11 | `email-signatures/` skill | MEDIUM | Folder 20 assets | 2 hr code |
| 12 | Defined-term propagation ("Workforce", "Governance Framework") into business docs | LOW-MEDIUM | **None — code only** | 1-2 hr |
| 13 | DOCX template theme still Aptos/Times (not Segoe UI) | LOW | **None — code only** | 2-3 hr XML patch |
| 14 | Approval workflow / version-stamp policy | LOW-MEDIUM | Policy from you | Policy: 1 hr. |
| 15 | Accessibility audit (alt text, contrast) | MEDIUM | **None — code only** | 2-3 hr |

---

## 6. Two paths you can pick today

### Path A — "close everything I can close without you uploading anything" (~15-20 hr code)

I execute all the **code-only** items above in order:
- Rewrite 4 generic skills to enforce NDLNG specs (#5)
- Create 3 new skills from already-captured specs (#9)
- Embed letterhead logo once PNG is available (#6 blocked pending PNG)
- Propagate defined terms into business docs (#12)
- Patch template theme to Segoe UI (#13)
- Add accessibility audit (alt text + contrast check) (#15)

**Outcome:** repo goes from "8 skills partially personalized" to "12 skills fully personalized + theme clean." No uploads needed from you.

### Path B — "unblock the compliance-critical skills" (requires your uploads)

You provide, in priority order:
1. Folder 18: Classification tier policy (a 1-page doc defining Public/Internal/Confidential/Restricted and which doc types default to which)
2. Folder 13: 1 recent 10-Q or 10-K excerpt (MD&A section), earnings call script, Reg FD policy
3. Folder 12: 1 FERC filing, 1 DOE filing, 1 PHMSA filing (all redacted as needed)
4. Folder 16: Latest ESG / sustainability report + TCFD/SASB alignment table
5. Folder 04: Real letterhead PNG (transparent, high-res)
6. Folder 20: Real desktop email signature + mobile email signature + 1-2 exec bio examples

**Outcome:** regulatory-comms, investor-relations, esg-reporting, email-signatures, classification, letterhead all move from blocked to done.

**My recommendation:** run **both in parallel**. Path A is unblocked today; Path B starts the moment any single folder lands.

---

## 7. What would signal "done" on this personalization effort

A single-sitting smoke test, post-remediation:
1. Ask Claude: "draft a Q2 board memo covering construction, commercial, safety."
2. Ask Claude: "generate an 8-K excerpt for our latest material event."
3. Ask Claude: "build an ESG disclosure table aligned to SASB."
4. Ask Claude: "produce a bilingual community update for an open house next month."
5. Ask Claude: "generate a safety moment on a new topic not in the sample set."
6. Ask Claude: "give me a PDF of the investor deck and the board memo with the correct classification stamps."

If all six produce artifacts that you or a senior NDLNG comms professional would sign off on **without edits to brand, voice, or compliance language**, the personalization is complete.

Today the first item (#1) would pass. Items #2–#6 each hit one of the gaps above.
