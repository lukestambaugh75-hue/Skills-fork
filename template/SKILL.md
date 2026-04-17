---
name: template-skill
description: "Replace with a complete description of what this skill does and exactly when Claude should invoke it. TRIGGER when: <explicit phrases / file types / code imports that should fire this skill>. DO NOT TRIGGER when: <adjacent cases this skill should skip>."
license: Complete terms in LICENSE.txt
# allowed-tools: Read, Grep, Bash  # uncomment and scope if this skill must run with a tool allowlist
---

# Skill Name

One-sentence summary of what this skill does. Keep it concrete.

## When to use

- Primary trigger phrase or situation.
- Secondary trigger phrase or situation.
- Do NOT use this skill when... (list the adjacent cases it should skip so Claude does not over-trigger).

## How it works

Step-by-step of what Claude should do when this skill fires. Use imperative voice ("Read the file", "Ask the user", "Call the script"). Reference any supporting files by relative path, e.g. `scripts/foo.py` or `references/schema.md`.

1. First step.
2. Second step.
3. Third step.

## Examples

Concrete end-to-end examples. One happy path plus one edge case is usually enough.

- **Example 1**: User says "...", Claude should respond by ... producing output like ...
- **Example 2**: User provides ..., Claude should ...

## Guardrails

Hard rules the skill must obey. These exist to keep the skill predictable and safe.

- Never ... (e.g. "never modify files outside the requested directory").
- Always ... (e.g. "always confirm before deleting").
- If unsure, ... (e.g. "ask the user rather than guessing").

## Supporting files

List every file shipped alongside this SKILL.md and its purpose. Keep this list in sync with what actually exists in the skill folder.

- `scripts/` — executable helpers called by the skill.
- `references/` — longer-form docs Claude can read on demand (keep them out of the main SKILL.md to save context).
- `assets/` — images, fixtures, or other static files.

## Authoring notes (delete before shipping)

- Keep SKILL.md under ~400 lines. Move deep reference material into `references/`.
- The `description:` field is what Claude uses to decide whether to trigger this skill. Be explicit about both triggers and non-triggers.
- Run this skill through `skills/skill-creator` before merging to tune the description and add evals.
