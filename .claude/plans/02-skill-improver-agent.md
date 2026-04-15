# Plan: `skill-improver` self-improvement agent loop

**Queued from session**: `session_01SNa2SVk5ioaLKtfafmA3x4` (2026-04-14)

**Goal**: When Claude's tool calls fail during a session, log them. Between sessions, spawn a subagent that reads the failure log, identifies root causes, and updates the relevant skill doc or sample README so the same failure doesn't recur. Result: the skill library gets sharper with every session.

## Target files

Files to create:
- `.claude/agents/skill-improver.md` (subagent definition)
- `.claude/hooks/failure-logger.sh` (PostToolUseFailure shell hook)
- `.claude/hooks/skill-improver-trigger.sh` (SessionStart shell hook)
- `.claude/failure-log.jsonl` (append-only log, gitignored)
- `.claude/failure-log.archive.jsonl` (processed entries, gitignored)
- `.claude/skill-improver.kill` (sentinel file — if present, agent is disabled)

Files to update:
- `.claude/settings.json` — register the two hooks, register the agent
- `.gitignore` — exclude the logs and sentinel

## Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│  During session (my turn):                                       │
│    tool call → fails → PostToolUseFailure hook → appends to      │
│    .claude/failure-log.jsonl                                     │
│                                                                  │
│  Between sessions (SessionStart):                                │
│    if log non-empty AND no kill-switch → spawn skill-improver   │
│    subagent in a worktree                                        │
│                                                                  │
│  Subagent:                                                       │
│    1. Reads log, groups by (skill, file, tool, error pattern)   │
│    2. For each group: identifies root cause                     │
│    3. Proposes skill-doc or sample-README update                │
│    4. Sanity-check diff (no mass rewrites, no skill deletions)  │
│    5. Commits with trailer "Learned-from: <failure_ids>"        │
│    6. Archives processed entries                                │
│    7. Opens a PR for human review (skill-doc changes only)      │
│       OR commits directly (sample README updates only)          │
└──────────────────────────────────────────────────────────────────┘
```

## Log entry schema

```json
{
  "id": "fail_01SNa_0001",
  "timestamp": "2026-04-14T21:35:12Z",
  "session_id": "session_01SNa2SVk5ioaLKtfafmA3x4",
  "tool_name": "Bash",
  "tool_input": {"command": "soffice --headless --convert-to pdf ..."},
  "exit_code": 2,
  "stderr_tail": "Error: source file could not be loaded",
  "stdout_tail": "",
  "context": {
    "skill": "docx",
    "file_touched": "skills/docx/scripts/render_docx.py",
    "recent_user_message": "convert this to PDF"
  },
  "status": "unprocessed"
}
```

## Subagent CLAUDE.md (draft)

```markdown
---
name: skill-improver
model: haiku
---

You are a post-mortem analyst. You do NOT write new features. You read
.claude/failure-log.jsonl, identify patterns, and update skill docs or
sample READMEs so the same failure doesn't recur.

## Process per run

1. Read .claude/failure-log.jsonl. Skip entries where status != "unprocessed".
2. Group failures by (skill, error-pattern). Example pattern:
   - "libreoffice-writer package missing" → docx + pptx PDF export
   - "docxtpl TemplateSyntaxError endfor" → docx template authoring
3. For each group, write a ≤150-word "Learned-from" note to append to the
   relevant SKILL.md. Format:

   ```
   ## Lesson learned 2026-04-14: <short title>
   **Symptom**: <stderr phrase> when <tool> runs on <input>.
   **Root cause**: <one sentence>.
   **Fix**: <the change you're making or recommending>.
   **Related failures**: <3 sample fail_IDs>
   ```

4. Sanity-check your diff:
   - No file deletions
   - No more than 3 files modified total per run
   - No changes to files outside skills/*/SKILL.md, samples/*/README.md
   - Net insertion ≤ 500 lines
   If any check fails, write your notes to .claude/plans/skill-improvements-<date>.md
   instead of committing, and exit.

5. If sanity-checks pass, commit with:
   - Message: "Skill improvements from failure log <date>"
   - Trailer: "Learned-from: fail_A, fail_B, fail_C"

6. Archive processed entries: move them from failure-log.jsonl to
   failure-log.archive.jsonl, setting status = "processed_<date>".

7. If you made commits, push the branch and open a PR titled "skill-improver
   updates <date>". Do NOT auto-merge.

## Hard limits

- Max 10 entries processed per run
- Max 3 files modified per run
- If failure-log.jsonl has > 100 entries, process the 10 most recent only
  and warn in the PR body about the backlog
- If you can't determine a root cause in ≤5 minutes of reading, skip the
  entry (leave status = "unprocessed"). Do not guess.

## Out of scope

- Adding new skills
- Modifying CLAUDE.md or settings.json
- Any write to production source code (only docs)
- Running tests, linters, or builds

Your job is a reader and a documentarian. If an entry suggests a
code change, write a plan under .claude/plans/ instead of making the change.
```

## Hook definitions (for settings.json)

```json
{
  "hooks": {
    "PostToolUseFailure": [{
      "matcher": "Bash|Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "~/.claude/hooks/failure-logger.sh"
      }]
    }],
    "SessionStart": [{
      "matcher": "",
      "hooks": [{
        "type": "agent",
        "prompt": "$ARGUMENTS\n\nCheck .claude/failure-log.jsonl. If it has unprocessed entries AND .claude/skill-improver.kill is absent, run the skill-improver agent on the unprocessed entries. Otherwise exit silently.",
        "timeout": 300,
        "model": "claude-haiku-4-5-20251001"
      }]
    }]
  }
}
```

## `failure-logger.sh` (draft)

```bash
#!/bin/bash
set -euo pipefail
LOG="$HOME/.claude/failure-log.jsonl"
# stdin is hook JSON per Claude Code spec
input=$(cat)
entry=$(jq -c --arg ts "$(date -u +%FT%TZ)" --arg sess "${CLAUDE_SESSION_ID:-unknown}" \
  '{id: ("fail_" + ($sess | split("_")[1] // "x") + "_" + (now|floor|tostring)),
    timestamp: $ts,
    session_id: $sess,
    tool_name: .tool_name,
    tool_input: .tool_input,
    exit_code: (.tool_response.exit_code // .tool_response.stderr | tostring | length > 0),
    stderr_tail: ((.tool_response.stderr // "") | .[-800:]),
    stdout_tail: ((.tool_response.stdout // "") | .[-400:]),
    status: "unprocessed"}' <<< "$input")
mkdir -p "$(dirname "$LOG")"
echo "$entry" >> "$LOG"
```

## Acceptance criteria for v1

- PostToolUseFailure hook writes a valid JSONL entry to `.claude/failure-log.jsonl` on any failed Bash/Write/Edit
- `.gitignore` includes `.claude/failure-log*.jsonl` and `.claude/skill-improver.kill`
- SessionStart trigger spawns the subagent exactly once per session (no loops)
- Subagent respects all hard limits; refuses to touch source code
- Running the subagent manually on a seeded log produces a sensible commit + PR
- Kill switch works: `touch .claude/skill-improver.kill` disables the loop
- End-to-end smoke: intentionally fail a Bash command, start a new session, see the subagent produce an updated SKILL.md

## Risks to address during build

1. **Second-order failures**: subagent's own failures could populate the log and cause a feedback loop. Mitigation: subagent ignores entries where `tool_name = Task` or the agent name is "skill-improver".
2. **Self-drift**: subagent updating SKILL.md drifts from brand guidelines. Mitigation: commit to a branch, open a PR, human review required.
3. **Log growth**: unbounded log eats disk. Mitigation: archive rotation, max-entry cap per run.
4. **Sensitive data in stderr**: tool errors may contain paths, API keys, PII. Mitigation: logger strips obvious secrets via regex (SEC_KEY_RE, API_TOKEN_RE) before writing.
5. **Wrong attribution**: subagent blames a skill for a failure that's actually in a sample file. Mitigation: group by skill ONLY when the failed file is inside `skills/*/`; otherwise group by sample path.

## Time estimate

- Hook scripts + settings.json: ~45 minutes
- Subagent CLAUDE.md + schema: ~30 minutes
- Smoke test (seed failures, verify end-to-end): ~45 minutes
- Documentation: ~30 minutes

**Total**: one focused session.

## Open questions for the next chat

1. Who reviews the subagent's PRs — the user, or a designated reviewer?
2. Should the subagent be allowed to update sample-artifact READMEs directly without PR? (My recommendation: yes; docs-only; low risk.)
3. Auto-run on every SessionStart, or only when `.claude/failure-log.jsonl` crosses a size threshold (e.g., 5 entries)?
4. Include the failure logs in a future audit tool that shows trends over time?
