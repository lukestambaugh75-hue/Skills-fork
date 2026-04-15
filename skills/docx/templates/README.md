# Jinja-tagged templates for docxtpl rendering

Templates here are **edit-in-Word, render-via-Python**. Markers like `{{ purpose_text }}` and `{%tr for d in definitions %}` get replaced at render time. The brand chrome (logo in header, cover graphic, watermark, footer text, fonts) is preserved byte-identically because docxtpl operates on the binary template.

## Files

| File | Purpose |
|---|---|
| `Procedure Template (Jinja).docx` | Main procedure template with 32 Jinja markers. |
| `procedure_schema.json` | Schema for the input dict — required and optional markers, field types, item shapes. |

## Render pipeline

```bash
python ../scripts/render_docx.py input.json output.docx
```

Pipeline does: lint → docxtpl → fallback to walk-and-replace if template damaged.

## Editing the template in Word

You CAN edit this template in Word — change layouts, add sections, fix typos in static text, update the cover graphic. **Do not change the markers themselves.** When you save, run the linter:

```bash
python ../scripts/lint_docx_template.py "Procedure Template (Jinja).docx" procedure_schema.json
```

Exit code 0 = clean. Exit 2 = warnings (render still works). Exit 3 = errors (render falls back to walk-and-replace).

## Common Word edits that break markers

1. **Autocorrect smart-quoting** — Word turns `{{purpose}}` into `{{purpose"}}`. Disable autocorrect when typing markers, or paste them from a plain-text editor.
2. **Run splits** — Word may split a marker across multiple text runs after editing. Visible as: marker appears in two pieces in the XML even though it looks fine on screen. Fix: delete the marker entirely, retype it in one motion, save.
3. **Marker deletion** — A non-technical author sees `{{ scope_text }}`, thinks it's junk, deletes it. Linter catches this against the schema.

## Adding a new field

1. Add the marker in Word: `{{ my_new_field }}`
2. Add it to `procedure_schema.json` under `required_markers` and `fields`
3. Pass `my_new_field` in your input dict
4. Re-lint to confirm clean

## Adding a new template (Standard, Guidance, etc.)

1. Copy the source template (e.g. `Standard Template.docx`)
2. Apply the same marker pattern (Jinja markers in placeholder text, table-row markers in their own rows)
3. Define a schema JSON next to it
4. Add an entry in `render_docx.py` to route to it

## Known divergences between docxtpl and walk-and-replace fallback

- **Revision History table**: docxtpl produces exactly N rows for N revisions. Walk-and-replace leaves the template's 26 rows in place (with later rows blank). Both are valid; docxtpl is cleaner. If you need the walk-and-replace path to also trim, add a row-cleanup step in `render_via_walk_and_replace`.
