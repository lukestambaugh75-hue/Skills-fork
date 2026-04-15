# Plan: Modern graphic layouts in the PPTX master

**Queued from session**: `session_01SNa2SVk5ioaLKtfafmA3x4` (2026-04-14)

**Target files**:
- `NextDecade-Claude-Project/02-templates/NextDecade PowerPoint Master (Oct 2025, brand-corrected).potx`
- `skills/pptx/scripts/render_pptx.py`
- `skills/pptx/scripts/lint_pptx_master.py`
- `NextDecade-Claude-Project/05-samples/Hot Work Safety Moment.pptx` (regenerate to demonstrate)

## Why

The current master has 50 layouts covering headline/body/dual/tri/quad content, but no "modern graphic" layouts (process arrows, quadrants, timelines, card rows, Sankey flows). Content authors who want these today either build them manually on a blank slide or fall back to SmartArt, which python-pptx can't manipulate. Building them as native auto-shape groups in the master makes them:
- Usable by `render_pptx.py` like any other layout (caller picks layout name, fills data)
- Editable in PowerPoint (no SmartArt magic)
- On-brand (use theme accent1/accent2 colors, Segoe UI)

## Layouts to build (five v1 layouts)

Each is a new slide layout in `theme1.xml` scheme, built with native PowerPoint shapes (not SmartArt).

| Layout name | Graphic | Schema fields |
|---|---|---|
| `ND Process 3-Step` | 3 horizontal chevron/arrow shapes with step number + title + 1-line description | `title`, `steps` = [{num, title, description}, ...] (exactly 3) |
| `ND Process 5-Step` | Same, 5 steps | Same, 5 items |
| `ND Quadrant 2x2` | 2×2 matrix with x-axis and y-axis labels + 4 quadrant labels | `title`, `x_axis`, `y_axis`, `quadrants` = {tl, tr, bl, br} |
| `ND Timeline 5-Item` | 5 milestone markers on a horizontal line with year + label above/below alternating | `title`, `milestones` = [{year, label}, ...] |
| `ND Card Row 3` | 3 icon-topped cards in a row, each with heading + 2-line body | `title`, `cards` = [{icon_ref, heading, body}, ...] |

Brand treatment for all:
- Chevrons / primary fills: navy `#002060` with white text
- Accent fills / highlights: orange `#FC7134`
- Positive-status fills (if used): green `#00B050`
- Card body text: Segoe UI 11pt black on white
- Axis / caption text: Segoe UI 9pt mid-gray `#A5A5A5`

## Implementation steps

1. **Build the layouts in PowerPoint** (one-time human work, not automatable cleanly):
   - Open the master .potx in PowerPoint
   - Slide Master view → new Layout → build one of the five layouts
   - Use placeholder shapes (`TEXT` placeholder with idx 20+ to keep out of the existing 10–15 range) for every variable field so `render_pptx.py` can target them
   - Save as .potx (preserve template content-type)

2. **Extend `render_pptx.py`**:
   - Add placeholder-filler dispatch entries per layout:
     ```python
     LAYOUT_FILLERS = {
       "ND Process 3-Step": _fill_process_steps,
       "ND Process 5-Step": _fill_process_steps,
       "ND Quadrant 2x2":   _fill_quadrant,
       "ND Timeline 5-Item": _fill_timeline,
       "ND Card Row 3":     _fill_cards,
     }
     ```
   - Each filler reads specific keys from the slide_spec dict and writes to the named placeholders. The dispatch happens in `_fill_placeholders` after the generic title/subtitle/bullets fill attempts.

3. **Extend `lint_pptx_master.py`**:
   - Add the five new layout names to `REQUIRED_LAYOUTS`
   - Add a check that each has the expected placeholder indices (so if a layout gets renamed or placeholders deleted in Word, we catch it before render)

4. **Build a demo deck** — regenerate `NextDecade-Claude-Project/05-samples/Hot Work Safety Moment.pptx` with one slide per new layout:
   - 3-step: Permit → Fire Watch → Close-out
   - Quadrant: frequency × severity of hot-work risks
   - Timeline: revision history milestones
   - Cards: three life-saving rules

5. **Commit to main** with message `Add 5 modern graphic layouts to PPTX master + dispatcher`.

## Time estimate

- Layout design in PowerPoint: ~2 hours of human time (this is the gating step)
- Dispatcher + linter updates: ~30 minutes once layouts exist
- Demo deck: ~15 minutes

**Cannot be fully automated** — step 1 requires a human in PowerPoint. The next session can either (a) guide a human through building them, (b) build stub .potx modifications via XML surgery (high-risk — easy to corrupt the master), or (c) use LibreOffice Impress's UI via screenshots (slow but feasible).

Recommended for next chat: ask the user whether they'd like to build the layouts themselves in PowerPoint (best quality) or have Claude attempt XML-level layout creation (risky; keep a backup).

## Acceptance criteria

- `lint_pptx_master.py` returns exit 0 with all 5 new layouts present and validated
- `render_pptx.py` renders a slide for each new layout when given the matching schema
- Demo deck opens in PowerPoint with all 5 slides rendering correctly
- Samples committed to `NextDecade-Claude-Project/05-samples/` showing the modern graphics in context
