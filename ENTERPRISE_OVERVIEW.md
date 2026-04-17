# Enterprise Overview

Read this before using, editing, or rolling out this repository.

---

## TL;DR

- **What this repo is:** a fork of Anthropic's public [`anthropics/skills`](https://github.com/anthropics/skills) marketplace, repurposed as our company's canonical source for agent skills and for the Markdown / `SKILL.md` authoring standard we will apply to enterprise documentation.
- **Who it is for:** anyone inside the company who writes a skill, writes documentation that should follow the same patterns, or decides what our enterprise Claude can invoke.
- **Before rollout:** complete the eight items in [Gaps before rollout](#gaps-before-rollout). The repo is content-ready; ownership, sync policy, and marketplace metadata still need company-specific decisions.

---

## 1. What this repo is

This is a **fork**, not a new project. The skills in `skills/` are Anthropic's published examples plus the four document-processing skills (`docx`, `pdf`, `pptx`, `xlsx`) that power Claude's native document capabilities.

We are keeping the fork because it gives us three things at once:

1. **A working marketplace** — `.claude-plugin/marketplace.json` is a real plugin bundle a Claude Code user can install with `/plugin marketplace add ...`. We can ship it to the enterprise deployment with zero additional scaffolding.
2. **A library of reference skills** — 17 skills covering document generation, design, testing, communications, API development, and skill-authoring itself. These are our working examples of "what a good skill looks like."
3. **A style anchor for company Markdown** — every skill's `SKILL.md` is itself a piece of structured documentation. The patterns these files use (YAML frontmatter, trigger descriptions, `When to use` / `How it works` / `Examples` / `Guardrails` sections, relative links into `scripts/` and `references/`) become our house style for company docs.

---

## 2. History & intent

The full commit log is short (28 commits) and tells a clear story:

| Phase | Commits | What happened |
|---|---|---|
| Bootstrap | `37292f3 init repo` → `83291af` | Anthropic published the repo with skill examples organized into folders. |
| Spec introduced | `10e0fbe` | First public draft of the Agent Skills spec. |
| Spec split out | `f232228`, `be229a5`, `69c0b1a` | Spec content moved to [agentskills.io/specification](https://agentskills.io/specification); `spec/agent-skills-spec.md` became a 3-line redirect. |
| Example skills added | `0f77e50`, `e5c6015`, `0075614`, etc. | `frontend-design`, `doc-coauthoring`, and friends. |
| Document skills added | `4e6907a`, `a5bcdd7` | `docx`, `pdf`, `pptx`, `xlsx` — the production document capabilities. |
| `claude-api` skill | `7029232`, `98669c1`, `887114f`, `ca1e7dc` | Long-running skill for SDK-based apps. |
| YAML rendering fix | `0f7c287` | Most recent upstream commit. |
| **This audit** | local commits on `claude/audit-and-document-NqUn5` | See [Appendix: Audit + fix record](#appendix-audit--fix-record). |

**On "everything merged":** the branch `claude/audit-and-document-NqUn5` was at parity with `main` before this audit. Any prior work you may have thought was merged into this branch was **not** here — it was either upstream content or lives elsewhere. Confirm that separately if it matters.

**Meeting the intent:** yes, this repo can serve the stated purpose (enterprise skills + documentation standard), provided the eight rollout gaps below are closed. It is not ready to deploy as-is, but none of the gaps require reshaping the repo — they are ownership, metadata, and policy decisions only.

---

## 3. Repo map

| Path | What it is |
|---|---|
| `README.md` | Top-level readme. Starts with our Enterprise section, then preserves upstream content verbatim below. |
| `ENTERPRISE_OVERVIEW.md` | This file. |
| `.claude-plugin/marketplace.json` | Claude Code plugin manifest. Declares three plugin bundles: `document-skills`, `example-skills`, `claude-api`. 17 skills total, 1:1 with `skills/` on disk. |
| `skills/` | 17 skill directories — see [§4 Catalog](#4-catalog-of-skills). |
| `spec/agent-skills-spec.md` | 3-line redirect to agentskills.io. Intentional. |
| `template/SKILL.md` | Starter template for new skills. Re-authored during this audit to model the enterprise standard. |
| `THIRD_PARTY_NOTICES.md` | License notices for bundled third-party assets (fonts, FFmpeg, Pillow, imageio). Required for the document skills. |
| `.gitignore` | Standard OS/IDE ignores. |

---

## 4. Catalog of skills

All 17 skills live under `skills/`, are declared in `marketplace.json`, and all `name:` fields match the directory name.

### Apache-2.0 example skills (13)

| Skill | One-line purpose | Ships |
|---|---|---|
| `algorithmic-art` | Generative art using p5.js with seeded randomness. | templates/ |
| `brand-guidelines` | Applies Anthropic's brand colors and typography to artifacts. | SKILL.md only |
| `canvas-design` | Produces .png / .pdf static designs, posters, art. | canvas-fonts/ |
| `claude-api` | Building / debugging / optimizing Claude API + SDK apps. | per-language docs (python, typescript, java, go, ruby, csharp, php, curl, shared) |
| `doc-coauthoring` | Structured workflow for co-authoring docs, proposals, specs. | SKILL.md only |
| `frontend-design` | Production-grade frontend UI (React, Tailwind, shadcn/ui). | SKILL.md only |
| `internal-comms` | Company-style internal communications (updates, newsletters, FAQs, incident reports). | examples/ |
| `mcp-builder` | Authoring high-quality MCP servers (Python FastMCP or Node SDK). | reference/, scripts/ |
| `skill-creator` | Meta-skill — creating, editing, and evaluating other skills. | agents/, assets/, eval-viewer/, references/, scripts/ |
| `slack-gif-creator` | Animated GIFs sized and tuned for Slack. | core/, requirements.txt |
| `theme-factory` | Applies one of 10 preset themes to slides/docs/HTML. | theme-showcase.pdf, themes/ |
| `web-artifacts-builder` | Complex multi-component claude.ai HTML artifacts. | scripts/ |
| `webapp-testing` | Playwright-driven testing of local web apps. | scripts/, examples/ |

### Source-available document skills (4)

These power Claude's production document capabilities. They are **proprietary / source-available** — not Apache-2.0 — and must not be redistributed as open source.

| Skill | One-line purpose | Ships |
|---|---|---|
| `docx` | Creating, reading, editing, manipulating Word documents. | scripts/ |
| `pdf` | Reading, extracting, merging, splitting, filling, OCR'ing PDFs. | scripts/ |
| `pptx` | Creating and editing PowerPoint decks. | scripts/, editing.md, pptxgenjs.md |
| `xlsx` | Creating and editing Excel/CSV/TSV spreadsheets. | scripts/ |

---

## 5. Guardrails

### Repo-wide

- **Upstream disclaimer (inherited):** from `README.md` — "These skills are provided for demonstration and educational purposes only… Always test skills thoroughly in your own environment before relying on them for critical tasks." Treat this as our floor, not our ceiling.
- **License split is not cosmetic.** The four document skills are source-available. Do not bundle them into an externally distributed marketplace without legal sign-off. All others are Apache-2.0.
- **Third-party obligations** in `THIRD_PARTY_NOTICES.md` travel with the document skills. Preserve the notices if you ship them.

### Per-skill guardrails

The skill bodies already encode their own rules. A few patterns to know:

- **`algorithmic-art` / `canvas-design`** — both explicitly instruct Claude to create original work and not copy existing artists to avoid copyright issues.
- **`claude-api`** — the only skill that fully models the `TRIGGER when: … DO NOT TRIGGER when: …` description pattern. Use it as the reference example for new skills.
- **`skill-creator`** — has its own evaluation loop (`eval-viewer/`, `scripts/run_eval.py`). Run new skills through it before merging.
- **`webapp-testing`** — runs Playwright. Keep it pointed at local / staging endpoints.
- **`slack-gif-creator`** — evaluate whether this belongs in the enterprise cut at all (see rollout checklist).

### SKILL.md authoring rules

Every skill we ship must:

1. Have a `SKILL.md` whose YAML `name:` matches its directory name.
2. Declare `description:` with enough context for Claude to fire the skill accurately. New skills should use explicit `TRIGGER when: …` / `DO NOT TRIGGER when: …` clauses (see `skills/claude-api/SKILL.md:3`).
3. Declare `license:` — `Complete terms in LICENSE.txt` for Apache-2.0 skills, `Proprietary. LICENSE.txt has complete terms` for source-available skills.
4. Ship a `LICENSE.txt` beside the SKILL.md.
5. Appear in `.claude-plugin/marketplace.json` under the right plugin block.

### Upstream sync guardrail

Do **not** edit the bodies of upstream skills. When you need different behaviour, fork the skill into a new directory (e.g. `skills/internal-comms-acme/`) and register the fork in `marketplace.json`. This keeps future Anthropic pulls clean.

---

## 6. Gaps before rollout

Eight items require a company-specific decision before enterprise deployment. None require code changes — they are policy or metadata.

1. **Ownership.** Add `CODEOWNERS` at the repo root. Decide who reviews new skills vs. upstream syncs.
2. **PR template.** Add `.github/pull_request_template.md` with checkboxes for the authoring rules in §5.
3. **Marketplace metadata.** `.claude-plugin/marketplace.json` still declares `name: anthropic-agent-skills` and `owner: Keith Lazuka <klazuka@anthropic.com>`. Rename to the company's bundle name and owner before publishing internally.
4. **Upstream sync policy.** Pick a cadence (monthly? on-demand?) and an owner for running `git fetch upstream && git merge upstream/main`. Document the exclusions: our Enterprise section of `README.md`, this file, and any company-forked skills.
5. **Marketplace publishing.** Decide whether Claude users run `/plugin marketplace add <our-internal-URL>` or whether we ship skills via a different channel. Configure auth accordingly.
6. **License posture.** Confirm with legal that mixing Apache-2.0 and source-available skills in one marketplace is acceptable for our distribution model (internal only? partner-facing?).
7. **Skill cut.** Audit the 17 skills for enterprise fit. `slack-gif-creator` is the obvious candidate for removal; `brand-guidelines` currently encodes Anthropic brand and should either be replaced with our own or retitled.
8. **Documentation standard adoption.** If this repo is going to set the Markdown standard for the whole company, announce it. The rules in §5 + the template in `template/SKILL.md` become the canon. Point teams at them.

---

## 7. What "good" looks like for a company SKILL.md

Use this as a one-page style guide.

- **Frontmatter:** `name`, `description`, `license` required. `allowed-tools` optional. Nothing else.
- **Description style for new skills:**
  `Short summary sentence. TRIGGER when: <explicit phrases/files/imports>. DO NOT TRIGGER when: <adjacent cases to skip>.`
  Keep it a single YAML string. Quote it if it contains a colon.
- **Length budget:** aim under 400 lines. If you need more, push long reference material into a sibling `references/` folder and link to it. `skill-creator` at 486 lines is at the upper bound.
- **Section order:** When to use → How it works → Examples → Guardrails → Supporting files. The upgraded `template/SKILL.md` models this exactly. Upstream Anthropic skills sometimes use different headings (e.g. `brand-guidelines` uses `Overview / Features`). That's fine for inherited content; **new** skills should follow the template.
- **Supporting files:** keep `scripts/`, `references/`, `assets/`, `examples/`, `templates/` — the names the existing skills already use. Reference them by relative path from SKILL.md.
- **Tone:** imperative ("Read the file", "Ask the user"). No hedging. The skill is instructions to Claude, not prose for humans.

---

## Appendix: Audit + fix record

Conducted on branch `claude/audit-and-document-NqUn5`. All findings from two audit passes (initial + re-audit).

| # | Issue | Severity | Fix | Commit |
|---|---|---|---|---|
| 1 | `skills/doc-coauthoring/` missing `LICENSE.txt` and `license:` frontmatter | Medium | Copied Apache-2.0 LICENSE.txt from skill-creator; added `license:` field | `88ad9ed` |
| 2 | `skills/skill-creator/SKILL.md` missing `license:` frontmatter | Low | Added `license: Complete terms in LICENSE.txt` | `88ad9ed` |
| 3 | License phrasing inconsistent across skills | Low | Kept both forms — the difference is semantic (Apache-2.0 vs source-available). Documented the rule in §5. | — |
| 4 | `.claude-plugin/marketplace.json:44` had orphan comma on its own line | Cosmetic | Reformatted | `a4e10b7` |
| 5 | `README.md` referenced non-existent `template-skill` | Cosmetic | Pointed to `./template` | `1f76335` |
| 6 | `template/SKILL.md` was a 6-line stub | Gap | Replaced with full enterprise template | `1f76335` |
| 7 | `README.md` had no enterprise framing | Gap | Prepended Enterprise Use section; preserved upstream content below | `1f76335` |
| 8 | Branch had zero divergence from main | Information | Audit fixes now provide the divergence | — |
| 9 | README contradicted itself on required frontmatter field count (2 vs 3) | P0 | Reconciled: 2 is the upstream minimum; 3 is the enterprise standard | `1df51f0` |
| 10 | TRIGGER/DO NOT TRIGGER mandate was too strict (only claude-api follows it) | P0 | Softened to "new skills should"; upstream skills exempted | `1df51f0` |
| 11 | `ENTERPRISE_OVERVIEW.md` referenced by README but did not exist | P0 | This file | pending commit |
| 12 | `CODEOWNERS`, PR template, sync cadence, marketplace metadata, license posture, skill cut, adoption announcement | P0–P1 | **Not code changes** — tracked in [Gaps before rollout](#gaps-before-rollout) for your decision | — |

### Non-issues (verified clean)

- No merge conflict markers, no `.orig` / `.rej` / `.bak` files, no TODO / FIXME / XXX / HACK anywhere.
- All 17 skills have valid YAML frontmatter with matching directory names.
- All referenced supporting files (scripts/, references/, assets/, examples/, templates/, core/, themes/) exist.
- `marketplace.json` parses as valid JSON and remains 1:1 with disk.
