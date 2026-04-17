# Enterprise Use (read first)

This repository is a fork of Anthropic's public [`anthropics/skills`](https://github.com/anthropics/skills) marketplace. Inside our company it is the **canonical source** for three things:

1. **Agent skills** shipped to our enterprise Claude deployment.
2. **`SKILL.md` authoring standards** — the format every skill we ship must follow.
3. **Markdown / documentation standards** — the base style rules for company documentation. Skills in this repo are the reference examples.

For the full tour (what each item is, guardrails, rollout checklist), read [`ENTERPRISE_OVERVIEW.md`](./ENTERPRISE_OVERVIEW.md).

## Share with a Claude Project

The [`ClaudeProjectBundle/`](./ClaudeProjectBundle/) folder holds the 14 files a teammate needs to upload to a Claude Project on claude.ai so the Project can write in this repo's voice and produce correctly-structured document inputs. It is the consolidated, Projects-sized distribution — it does not include the Python renderers or binary brand templates, which Projects cannot execute anyway.

To produce a zip: `./build-claude-project-bundle.sh` (output `Claude Project knowledge bundle.zip` is gitignored).

## Upstream relationship

We pull from Anthropic upstream. Do **not** rewrite the bodies of upstream skills in place — that makes future merges painful. Instead:

- **Add** new company skills under `skills/<slug>/` and list them in `.claude-plugin/marketplace.json`.
- **Override** behaviour by forking a skill into a new directory (e.g. `skills/internal-comms-acme/`) rather than editing the upstream copy.
- **Sync cadence and owner** are tracked in `ENTERPRISE_OVERVIEW.md`.

## Adding a new company skill

1. Copy [`./template`](./template) to `skills/<your-slug>/`.
2. Fill in `name`, `description`, and `license` in the frontmatter. For `description`, **new** company skills should use explicit `TRIGGER when: …` / `DO NOT TRIGGER when: …` clauses — see [`skills/claude-api/SKILL.md`](./skills/claude-api/SKILL.md) as the canonical example. Most upstream Anthropic skills predate this pattern and use informal "Use when …" phrasing; that is fine and does not need to be rewritten.
3. Add the skill path to the appropriate plugin block in `.claude-plugin/marketplace.json`.
4. Open a PR. Reviews are owned by the Skills maintainers (set in `CODEOWNERS` when that file is added — see rollout checklist in `ENTERPRISE_OVERVIEW.md`).

## Required SKILL.md frontmatter

The upstream Agent Skills spec only requires `name` and `description`. Our enterprise standard extends that with a required `license` field so every shipped skill is explicit about its redistribution terms. (If you read the "Creating a Basic Skill" section further down — that's the upstream minimum; the table below is what we ship.)

| Field | Required | Notes |
|---|---|---|
| `name` | yes | Lowercase, hyphenated. **Must** match the directory name. |
| `description` | yes | Full sentence(s). New skills should include explicit trigger / non-trigger clauses so Claude fires the skill accurately. |
| `license` | yes (enterprise) | `Complete terms in LICENSE.txt` for Apache-2.0 skills; `Proprietary. LICENSE.txt has complete terms` for source-available document skills. Keep the LICENSE.txt file beside the SKILL.md. |
| `allowed-tools` | optional | Scope tool access if the skill must run under a restricted allowlist. |

## License split (important)

- `skills/docx`, `skills/pdf`, `skills/pptx`, `skills/xlsx` are **source-available / proprietary** — not Apache-2.0. They power Claude's document capabilities and must not be redistributed as open source.
- All other skills are **Apache-2.0**.
- See [`THIRD_PARTY_NOTICES.md`](./THIRD_PARTY_NOTICES.md) for the bundled third-party obligations (fonts, FFmpeg, Pillow, etc.).

---

> **Note:** This repository contains Anthropic's implementation of skills for Claude. For information about the Agent Skills standard, see [agentskills.io](http://agentskills.io).

# Skills
Skills are folders of instructions, scripts, and resources that Claude loads dynamically to improve performance on specialized tasks. Skills teach Claude how to complete specific tasks in a repeatable way, whether that's creating documents with your company's brand guidelines, analyzing data using your organization's specific workflows, or automating personal tasks.

For more information, check out:
- [What are skills?](https://support.claude.com/en/articles/12512176-what-are-skills)
- [Using skills in Claude](https://support.claude.com/en/articles/12512180-using-skills-in-claude)
- [How to create custom skills](https://support.claude.com/en/articles/12512198-creating-custom-skills)
- [Equipping agents for the real world with Agent Skills](https://anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

# About This Repository

This repository contains skills that demonstrate what's possible with Claude's skills system. These skills range from creative applications (art, music, design) to technical tasks (testing web apps, MCP server generation) to enterprise workflows (communications, branding, etc.).

Each skill is self-contained in its own folder with a `SKILL.md` file containing the instructions and metadata that Claude uses. Browse through these skills to get inspiration for your own skills or to understand different patterns and approaches.

Many skills in this repo are open source (Apache 2.0). We've also included the document creation & editing skills that power [Claude's document capabilities](https://www.anthropic.com/news/create-files) under the hood in the [`skills/docx`](./skills/docx), [`skills/pdf`](./skills/pdf), [`skills/pptx`](./skills/pptx), and [`skills/xlsx`](./skills/xlsx) subfolders. These are source-available, not open source, but we wanted to share these with developers as a reference for more complex skills that are actively used in a production AI application.

## Disclaimer

**These skills are provided for demonstration and educational purposes only.** While some of these capabilities may be available in Claude, the implementations and behaviors you receive from Claude may differ from what is shown in these skills. These skills are meant to illustrate patterns and possibilities. Always test skills thoroughly in your own environment before relying on them for critical tasks.

# Skill Sets
- [./skills](./skills): Skill examples for Creative & Design, Development & Technical, Enterprise & Communication, and Document Skills
- [./spec](./spec): The Agent Skills specification
- [./template](./template): Skill template

# Try in Claude Code, Claude.ai, and the API

## Claude Code
You can register this repository as a Claude Code Plugin marketplace by running the following command in Claude Code:
```
/plugin marketplace add anthropics/skills
```

Then, to install a specific set of skills:
1. Select `Browse and install plugins`
2. Select `anthropic-agent-skills`
3. Select `document-skills` or `example-skills`
4. Select `Install now`

Alternatively, directly install either Plugin via:
```
/plugin install document-skills@anthropic-agent-skills
/plugin install example-skills@anthropic-agent-skills
```

After installing the plugin, you can use the skill by just mentioning it. For instance, if you install the `document-skills` plugin from the marketplace, you can ask Claude Code to do something like: "Use the PDF skill to extract the form fields from `path/to/some-file.pdf`"

## Claude.ai

These example skills are all already available to paid plans in Claude.ai. 

To use any skill from this repository or upload custom skills, follow the instructions in [Using skills in Claude](https://support.claude.com/en/articles/12512180-using-skills-in-claude#h_a4222fa77b).

## Claude API

You can use Anthropic's pre-built skills, and upload custom skills, via the Claude API. See the [Skills API Quickstart](https://docs.claude.com/en/api/skills-guide#creating-a-skill) for more.

# Creating a Basic Skill

Skills are simple to create - just a folder with a `SKILL.md` file containing YAML frontmatter and instructions. You can use the skill in [`./template`](./template) as a starting point:

```markdown
---
name: my-skill-name
description: A clear description of what this skill does and when to use it
---

# My Skill Name

[Add your instructions here that Claude will follow when this skill is active]

## Examples
- Example usage 1
- Example usage 2

## Guidelines
- Guideline 1
- Guideline 2
```

The frontmatter requires only two fields:
- `name` - A unique identifier for your skill (lowercase, hyphens for spaces)
- `description` - A complete description of what the skill does and when to use it

The markdown content below contains the instructions, examples, and guidelines that Claude will follow. For more details, see [How to create custom skills](https://support.claude.com/en/articles/12512198-creating-custom-skills).

# Partner Skills

Skills are a great way to teach Claude how to get better at using specific pieces of software. As we see awesome example skills from partners, we may highlight some of them here:

- **Notion** - [Notion Skills for Claude](https://www.notion.so/notiondevs/Notion-Skills-for-Claude-28da4445d27180c7af1df7d8615723d0)
