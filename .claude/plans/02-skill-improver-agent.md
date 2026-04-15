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
- `.claude/skill-improver.last-run` (timestamp sentinel for the 7-day trigger; gitignored)

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

5. If sanity-checks pass, split changes into two commits by target path:
   - **Commit A (sample READMEs, direct to main)**: any file under `samples/*/README.md`.
     Message: "Skill improvements (sample docs) from failure log <date>"
     Trailer: "Learned-from: fail_A, fail_B"
     Push directly to `main`.
   - **Commit B (skill docs, via PR)**: any file under `skills/*/SKILL.md`.
     Message: "Skill improvements (SKILL.md) from failure log <date>"
     Trailer: "Learned-from: fail_C, fail_D"
     Push to branch `skill-improver/<date>` and open a PR.

   If only one target type was touched, make only that commit.

6. Archive processed entries: move them from failure-log.jsonl to
   failure-log.archive.jsonl, setting status = "processed_<date>".
   Retain archive indefinitely (do not rotate) — future audit tool depends on it.

7. For Commit B only: open a PR titled "skill-improver updates <date>".
   - Base: `main`. Head: `skill-improver/<date>`.
   - Assign `@lukestambaugh75-hue` as reviewer.
   - Apply label `skill-improver`.
   - Do NOT request Copilot review. Do NOT enable auto-merge.
   - PR body: list the Learned-from fail_IDs and a one-line summary per lesson.

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
        "type": "command",
        "command": "~/.claude/hooks/skill-improver-trigger.sh"
      }]
    }]
  }
}
```

## `skill-improver-trigger.sh` (draft)

Gates the subagent on the Q3 threshold — ≥5 unprocessed entries OR >7 days since last run. Exits silently otherwise, so SessionStart stays cheap on quiet weeks.

```bash
#!/bin/bash
set -euo pipefail
LOG="$HOME/.claude/failure-log.jsonl"
KILL="$HOME/.claude/skill-improver.kill"
LAST="$HOME/.claude/skill-improver.last-run"

[[ -f "$KILL" ]] && exit 0
[[ -f "$LOG" ]] || exit 0

# Q3 threshold A: count unprocessed entries
unprocessed=$(jq -c 'select(.status == "unprocessed")' "$LOG" 2>/dev/null | wc -l)

# Q3 threshold B: days since last run (default: forever ago)
if [[ -f "$LAST" ]]; then
  now=$(date +%s); then_=$(date -r "$LAST" +%s); days=$(( (now - then_) / 86400 ))
else
  days=9999
fi

if (( unprocessed >= 5 )) || (( days > 7 )); then
  # emit JSON telling Claude Code to spawn the skill-improver subagent
  cat <<JSON
{"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": "Run the skill-improver subagent on .claude/failure-log.jsonl. ${unprocessed} unprocessed entries; ${days} days since last run."}}
JSON
  date -u +%FT%TZ > "$LAST"
fi
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
- `.gitignore` includes `.claude/failure-log*.jsonl`, `.claude/skill-improver.kill`, and `.claude/skill-improver.last-run`
- SessionStart trigger is **threshold-gated**: no subagent spawn when unprocessed < 5 AND last run ≤ 7 days ago; subagent spawns exactly once per session when the threshold is crossed
- `skill-improver.last-run` is stamped on every spawn (not on every SessionStart)
- Subagent respects all hard limits; refuses to touch source code
- Subagent splits commits correctly: `samples/*/README.md` → direct to `main`; `skills/*/SKILL.md` → branch + PR assigned to `@lukestambaugh75-hue`, labelled `skill-improver`, no auto-merge, no Copilot review
- Archive is append-only — processed entries move to `failure-log.archive.jsonl` but are never deleted
- Kill switch works: `touch .claude/skill-improver.kill` disables the loop
- End-to-end smoke: seed 5 failures, start a new session, see the subagent produce a direct-to-main sample-README commit and/or a SKILL.md PR as appropriate

## Risks to address during build

1. **Second-order failures**: subagent's own failures could populate the log and cause a feedback loop. Mitigation: subagent ignores entries where `tool_name = Task` or the agent name is "skill-improver".
2. **Self-drift**: subagent updating SKILL.md drifts from brand guidelines. Mitigation: commit to a branch, open a PR, human review required.
3. **Log growth**: unbounded log eats disk. Mitigation: archive is **not** rotated (per decision Q4 — future audit tool needs the history), but the active `failure-log.jsonl` is drained on every run and a max-entry cap (10) per run prevents any single run from ballooning. If archive size ever becomes a real problem, compress in place (`gzip failure-log.archive.jsonl`) rather than delete.
4. **Sensitive data in stderr**: tool errors may contain paths, API keys, PII. Mitigation: logger strips obvious secrets via regex (SEC_KEY_RE, API_TOKEN_RE) before writing.
5. **Wrong attribution**: subagent blames a skill for a failure that's actually in a sample file. Mitigation: group by skill ONLY when the failed file is inside `skills/*/`; otherwise group by sample path.

## Time estimate

- Hook scripts + settings.json: ~45 minutes
- Subagent CLAUDE.md + schema: ~30 minutes
- Smoke test (seed failures, verify end-to-end): ~45 minutes
- Documentation: ~30 minutes

**Total**: one focused session.

## Resolved decisions (2026-04-15)

1. **PR reviewer**: User (`@lukestambaugh75-hue`) as single maintainer. Subagent opens PRs against `main`, assigns `@lukestambaugh75-hue` as reviewer, applies the `skill-improver` label, and does **not** request Copilot review. No auto-merge.
2. **Sample-artifact READMEs — direct commit to `main`**: Approved (docs-only, low risk). Subagent commits changes under `samples/*/README.md` directly. Changes under `skills/*/SKILL.md` go through PR. If a single run touches both, the subagent splits into two commits and only the skill-doc commit is pushed to the branch + PR; the sample-README commit lands on `main` separately.
3. **Trigger**: Threshold-based, not every SessionStart. Subagent runs only when **either**:
   - `.claude/failure-log.jsonl` has **≥5 unprocessed entries**, OR
   - **>7 days** since the last skill-improver run (stamp in `.claude/skill-improver.last-run`).

   This avoids noisy PRs on low-failure weeks while guaranteeing periodic review.
4. **Audit tool (future, out of scope for v1)**: Yes. `failure-log.archive.jsonl` is retained indefinitely (not rotated out) so a future audit tool can compute trends — failure rate per skill, recurring error patterns, time-to-fix after a "Lesson learned" lands. V1 simply preserves the data; the tool itself is a later plan.
