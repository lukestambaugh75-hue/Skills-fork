# Test Inputs — Drop Files Here

Drop a JSON file into this folder and run the command below to generate a
formatted NextDecade document.

## Quick start

```bash
# Procedure
python3 NextDecade-Claude-Project/04-scripts/render_docx.py \
  procedure test-inputs/my-procedure.json test-inputs/output/my-procedure.docx

# Standard
python3 NextDecade-Claude-Project/04-scripts/render_docx.py \
  standard test-inputs/my-standard.json test-inputs/output/my-standard.docx

# Guidance
python3 NextDecade-Claude-Project/04-scripts/render_docx.py \
  guidance test-inputs/my-guidance.json test-inputs/output/my-guidance.docx

# PowerPoint safety moment / deck
python3 skills/pptx/scripts/render_pptx.py \
  test-inputs/my-deck.json test-inputs/output/my-deck.pptx
```

Output lands in `test-inputs/output/`. The render script prints a JSON
report — look for `"path": "docxtpl"` (fast path, clean) vs
`"walk_and_replace_fallback"` (template issue, output still usable but fix
the template).

---

## Template files in this folder

| File | Use as starting point for |
|---|---|
| `procedure-template.json` | Any new Procedure |
| `standard-template.json` | Any new Standard |
| `guidance-template.json` | Any new Guidance |
| `pptx-template.json` | Any new PowerPoint deck |

Copy a template, rename it, fill in your content, then run the command above.

---

## Document numbering

Format: `ORG-NTD-000010-XXX-YYY-#####`

| Code | Meaning |
|---|---|
| `XXX` | Functional area: HSE, SAF, SEC, OPS, LGL, FIN, ITS, SCM, COR |
| `YYY` | Type: PRC (Procedure), STD (Standard), GDN (Guidance) |
| `#####` | 5-digit serial |

Revision `0` = initial issue. Subsequent: `1`, `2`, `A`, `B`…

---

## PPTX brand families

You must declare one brand per deck. Layouts must match the chosen prefix.

| brand value | Layout prefix | Use for |
|---|---|---|
| `"NextDecade"` | `ND ` | Corporate content |
| `"RioGrandeLNG"` | `RG ` | LNG facility / project content |
| `"NCS"` | `NCS ` | NEXT Carbon Solutions content |

Shared layouts (any brand): `Custom Layout`, `Public Disclaimer`, `23_Custom Layout`
