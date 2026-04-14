# NextDecade LNG Enterprise Skills Template

**Status:** Scaffolding — awaiting upload intake for personalization.

This repository is being built as the **NextDecade LNG enterprise skills library**. It is a fork of Anthropic's public skills repo, being customized for NDLNG use and eventual distribution inside the organization as the authoritative template library.

## What this repo will become

A set of skills that enforce NextDecade LNG's:
- Brand identity (colors, typography, logos, imagery)
- Document standards (memos, reports, SOPs, MSAs, board packets)
- Presentation standards (investor, board, earnings, community, safety)
- Written voice & tone
- Legal boilerplate (forward-looking, safe harbor, Reg FD, confidentiality)
- Document classification (Public / Internal / Confidential / Restricted)
- Industry-specific conventions (FERC, DOE, SEC, HSE, ESG, community)
- File naming & versioning discipline
- Data visualization standards
- Email signatures & executive bio formats

## Current state

| Component | Status |
|-----------|--------|
| Upload intake scaffolding | Built — see `/uploads/` |
| Personalization workflow skill | Built — see `/skills/enterprise-personalization/` |
| Brand personalization | Pending — awaiting uploads in `/uploads/01-brand/` and `/uploads/02-typography/` |
| Document personalization | Pending — awaiting uploads in `/uploads/04-document-templates/` |
| Presentation personalization | Pending — awaiting uploads in `/uploads/05-presentation-templates/` |
| Comms personalization | Pending — awaiting uploads in `/uploads/09-sample-communications/` + `/uploads/10-style-voice-guide/` |
| Legal boilerplate skill | Not yet created — awaiting uploads in `/uploads/11-legal-boilerplate/` |
| Classification skill | Not yet created — awaiting uploads in `/uploads/18-classification-rules/` |
| Industry skills (SEC/FERC/HSE/ESG/community) | Not yet created — awaiting respective uploads |

## How to contribute to the build-out

1. Read `/uploads/README.md` for the full intake workflow.
2. Drop artifacts into the appropriate `/uploads/XX-*/` subfolder. Each has its own README explaining what's needed.
3. When an initial batch is in place, trigger the `enterprise-personalization` skill to run gap analysis and extraction.
4. Review extracted specs before they propagate into skills.
5. Approve diffs before anything is committed.

## How to use once complete

Once populated and personalized, any NextDecade LNG employee or agent using this skills library will produce on-brand, on-voice, correctly-classified, legally-compliant output by default for:
- Any Word document
- Any PowerPoint deck
- Any Excel report
- Any internal or external communication
- Any regulatory filing draft
- Any investor / IR material
- Any community / stakeholder comms
- Any HSE / safety content
- Any ESG / sustainability disclosure

## Distribution model

This repo is intended to become an internal template library. Expected distribution:
- Clone / fork inside NDLNG
- Loaded as a Claude Code plugin
- Used via the Claude API for automated content generation
- Used by humans as reference templates

## Upstream origin

This is a fork of `anthropics/skills`. Generic skills (`algorithmic-art`, `canvas-design`, `slack-gif-creator`, etc.) that are not relevant to enterprise comms may be pruned during personalization. Mechanical skills (`docx`, `pptx`, `xlsx`, `pdf`) will be kept and have NDLNG defaults baked in.
