# Jinja-tagged templates for docxtpl rendering

Templates here are **edit-in-Word, render-via-Python**. Markers like `{{ purpose_text }}` and `{%tr for d in definitions %}` get replaced at render time. The brand chrome (logo in header, cover graphic, watermark, footer text, fonts) is preserved byte-identically because docxtpl operates on the binary template.

## Files

| File | Purpose |
|---|---|
| `Procedure Template (Jinja).docx` | Procedure template, derived from `../03-original-templates/NextDecade Blank Procedure Template_Rev 1 April 9th 2026.docx`. |
| `procedure_schema.json` | Schema for the input dict — required and optional markers, field types, item shapes. |
| `Standard Template (Jinja).docx` | Standard template (legacy layout — Standard Template.docx). |
| `standard_schema.json` | Schema for Standard inputs. |
| `Guidance Template (Jinja).docx` | Guidance template (legacy layout — Guidance Template.docx). |
| `guidance_schema.json` | Schema for Guidance inputs. |

## Render pipeline

```bash
python ../scripts/render_docx.py procedure input.json output.docx [--pdf]
```

Pipeline does: lint → docxtpl (strict). If the template is damaged, fix it in Word and re-lint — there is no fallback path.

## Editing the template in Word

You CAN edit this template in Word — change layouts, add sections, fix typos in static text, update the cover graphic. **Do not change the markers themselves.** When you save, run the linter:

```bash
python ../scripts/lint_docx_template.py "Procedure Template (Jinja).docx" procedure_schema.json
```

Exit code 0 = clean. Exit 2 = warnings (render still works). Exit 3 = errors (render refuses to proceed — fix the template in Word).

## docxtpl marker patterns used in `Procedure Template (Jinja).docx`

| Pattern | Where used | Notes |
|---|---|---|
| `{{ field }}` | Single-paragraph text fields (purpose, scope, header date, etc.). | docxtpl substitutes the string in place. |
| `{%tr for x in xs %}` ... `{%tr endfor %}` | Row-loop tables (revision history, change log, roles, steps, definitions, abbreviations, references). | The two directives live in **separate rows** above and below the data row. The directive rows are removed at render time; the data row repeats per iteration. |
| `{%p for x in xs %}` ... `{%p endfor %}` | Variable-paragraph blocks (PPE paragraphs, appendices, responsibilities cell within roles). | The two directives live on **separate paragraphs** above and below the body paragraphs. The directive paragraphs are removed; the body paragraphs repeat per iteration. |

## Common Word edits that break markers

1. **Autocorrect smart-quoting** — Word turns `{{purpose}}` into `{{purpose"}}`. Disable autocorrect when typing markers, or paste them from a plain-text editor.
2. **Run splits** — Word may split a marker across multiple text runs after editing. Visible as: marker appears in two pieces in the XML even though it looks fine on screen. Fix: delete the marker entirely, retype it in one motion, save.
3. **Marker deletion** — A non-technical author sees `{{ scope_text }}`, thinks it's junk, deletes it. Linter catches this against the schema.
4. **Putting `{%tr for%}` and `{%tr endfor %}` in the same row** — docxtpl silently drops the opening tag, leaving an unbalanced template. Always keep them on separate rows.

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

