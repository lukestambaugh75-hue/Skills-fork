# Queued plans for the next chat

This folder holds implementation plans that came out of session
`session_01SNa2SVk5ioaLKtfafmA3x4` (2026-04-14) but were not built — they
were captured here so the next session can pick them up.

| # | File | Topic | Effort | Gating step |
|---|---|---|---|---|
| 01 | `01-modern-graphics-layouts.md` | Add 5 modern graphic layouts (process arrows, quadrant, timeline, card row) to the PPTX master + dispatcher entries in `render_pptx.py` | ~1 session | Layouts must be built in PowerPoint by a human (or via risky XML surgery) |
| 02 | `02-skill-improver-agent.md` | Self-improvement loop: PostToolUseFailure hook logs failures → SessionStart subagent reads log, updates skill docs, opens PRs | ~1 session | Pure code, no external blockers |

## Recommended order

1. **02-skill-improver-agent** first — it's pure code, builds itself, and starts producing value on every subsequent session. Once running, all future failures (including any from building modern-graphics) feed back into improvements automatically.
2. **01-modern-graphics-layouts** second — this one needs human PowerPoint time, which is async. Kick off the human work and pick up the dispatcher/linter changes in parallel.

## To resume

Either:
- Open the plan file and execute the steps directly, or
- Tell Claude `/plan resume <filename>` (if a plan-execution skill is added) or just paste the path
