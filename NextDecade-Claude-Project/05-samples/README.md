# Sample artifacts — Hot Work Permits & Fire Watch

One safety topic, multiple personalized-skill outputs.

| File | Skill | Method | Notes |
|---|---|---|---|
| `Hot Work Procedure (docxtpl).docx` | docx | **Production docxtpl path** | Rendered via `skills/docx/scripts/render_docx.py procedure <input.json> <output.docx>` from `Procedure Template (Jinja).docx`. Source template: `uploads/04-document-templates/NextDecade Blank Procedure Template_Rev 1 April 9th 2026.docx` (Rev 1, Apr 9 2026 layout). Sections: 1.0 Purpose, 2.0 Scope, 3.0 Roles and Responsibilities, 4.0 Safety and Health Precautions, 5.0 Hot Work Procedure (with 7-step table), 6.0 Record Keeping and Training, 9.0 Definitions, 9.2 Abbreviations, 10.0 References, Appendix A (Hot Work Permit Form), Appendix B (Fire Watch Checklist). |
| `Hot Work Safety Standard.docx` / `.pdf` | docx | docxtpl path on the legacy Standard template. | |
| `Hot Work Safety Guidance.docx` / `.pdf` | docx | docxtpl path on the legacy Guidance template. | |
| `Hot Work Safety Moment.pptx` / `.pdf` | pptx | Template-clone of `NextDecade Power Point Slide Master_Final_Oct 2025.potx` (color-corrected). | 3 slides: Cover (`Custom Layout` with tagline), Content (`ND Single Narrative 18 Font` with 6 bullets), Back cover (`23_Custom Layout` with tagline + URL). Brand orange `#FC7134` correct in accent2. |
| `Hot Work All-Hands Email.docx` | internal-comms | New .docx built per Writing Style Guide §5.4. | Segoe UI throughout. Headlines 20pt navy, subheads 16pt navy, body 11pt black. Casual-internal voice. |
| `Hot Work Permit Tracker.xlsx` | xlsx | Built using personalized xlsx skill brand chrome. | 3 sheets: Permit Log (color-coded status), Permit Detail (close-out), Trend Summary (with totals row). |

## On pictures and graphics

- For `.docx` (Procedure): the cloned template carries the NextDecade logo embedded in the header, the cover graphic, and the watermark. docxtpl preserves all of these byte-identically.
- For `.pptx` (Safety Moment): all 32 media assets in the slide master come along by clone. Layouts already contain the brand chrome. Only text in placeholders was replaced.
- For `.xlsx`: there are no images by default. If you want a header logo on every page, drop the logo PNG from `uploads/04-document-templates/NextDecade Blank Procedure Template_Rev 1 April 9th 2026.docx → word/media/imageN.png` into the worksheet header.

## Topic

**Hot work** is the highest-risk routine activity at any LNG facility. The procedure, safety moment, all-hands email, and tracker are all consistent with each other and reference the same fictional near-miss event (HW-2026-0143 on 14-Apr-2026).
