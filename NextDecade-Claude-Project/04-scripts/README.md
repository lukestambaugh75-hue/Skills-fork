# Scripts — for Claude Code users only

These scripts are **not needed** if you're using Claude Projects on claude.ai. They're for running the render pipeline locally (via Claude Code, or any Python machine) to produce DOCX / PDF / PPTX files from a JSON input.

## Setup (one-time)

```bash
pip install python-docx python-pptx docxtpl openpyxl jinja2
# Optional — for PDF export:
# apt-get install libreoffice-writer libreoffice-impress  (Linux)
# brew install libreoffice                                 (macOS)
```

## Generate a Procedure / Standard / Guidance document

```bash
python render_docx.py procedure input.json output.docx --pdf
python render_docx.py standard  input.json output.docx
python render_docx.py guidance  input.json output.docx --pdf
```

`input.json` follows the schema in `../02-templates/<doc_type>_schema.json`. See `../05-samples/input-example.json` for a full working example of the **current procedure schema (v2.0.0, Rev 1 Blank template)**.

## Generate a PowerPoint deck

```bash
python render_pptx.py deck_input.json output.pptx --pdf
```

`deck_input.json` shape:

```json
{
  "brand": "NextDecade",
  "title": "Deck title",
  "slides": [
    {"layout": "Custom Layout", "title": "Cover title", "subtitle": "Date line"},
    {"layout": "Public Disclaimer"},
    {"layout": "ND Single Narrative 18 Font", "title": "...", "bullets": ["..."]},
    {"layout": "23_Custom Layout"}
  ]
}
```

**`brand` is required** and must be one of `"NextDecade"`, `"RioGrandeLNG"`, or `"NCS"`. It gates which layout prefix is allowed for non-shared slides:

| `brand` | Allowed content-layout prefix |
|---|---|
| `NextDecade` | `ND …` |
| `RioGrandeLNG` | `RG …` |
| `NCS` | `NCS …` |

Shared layouts allowed in any family: `Custom Layout`, `1_Custom Layout`, `Public Disclaimer`, `23_Custom Layout`. Any other layout whose prefix doesn't match the declared brand raises `ValueError` before rendering — this enforces the ask-first brand-family gate described in `skills/pptx/SKILL.md` and `NextDecade-Claude-Project/CLAUDE-INSTRUCTIONS.md`.

## Validate templates before deploying

```bash
python lint_docx_template.py "../02-templates/Procedure Template (Jinja).docx" "../02-templates/procedure_schema.json"
python lint_pptx_master.py  "../02-templates/NextDecade PowerPoint Master (Oct 2025, brand-corrected).potx"
```

Exit 0 = clean. Exit 3 = template corruption (smart-quote contamination, run-split markers, missing markers, etc.) — fix in Word before rendering. The render pipeline will automatically fall back to walk-and-replace if the Jinja template is damaged, so production keeps working while you fix it.

## How the pipeline makes decisions

1. Lint the Jinja template
2. If clean → render via docxtpl (fast, best quality)
3. If damaged → fall back to walk-and-replace on the original un-tagged template (slower, still brand-correct)
4. If `--pdf` → export via headless LibreOffice

## Paths in the scripts

The scripts assume the templates live at paths inside the NextDecade repo structure (`/home/user/Skills-fork/...`). If you're using this bundle outside that repo, edit the `TEMPLATES`, `MASTER`, and `UPLOADS` constants at the top of `render_docx.py` and `render_pptx.py` to point at your local `02-templates/` and `03-original-templates/` folders.
