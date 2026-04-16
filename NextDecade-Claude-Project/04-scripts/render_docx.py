#!/usr/bin/env python3
"""docxtpl render pipeline for NextDecade governance documents.

Supports: procedure, standard, guidance. Each has a Jinja-tagged template and
a JSON schema under ../templates/. Pipeline:
  1. Lint the Jinja template (scripts/lint_docx_template.py).
  2. If clean/warnings only -> render with docxtpl + StrictUndefined.
  3. If errors -> fall back to walk-and-replace on the ORIGINAL template.
  4. Optional: convert the rendered .docx to .pdf via LibreOffice.

CLI:
  python render_docx.py <doc_type> <input.json> <output.docx> [--pdf] [--no-fallback]
    doc_type: procedure | standard | guidance

Module:
  from render_docx import render
  report = render("procedure", data_dict, "/path/to/output.docx", pdf=True)
"""
from __future__ import annotations
import sys, json, subprocess, shutil, os
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
TEMPLATES = HERE.parent / "02-templates"
LINTER = HERE / "lint_docx_template.py"

# Template registry — extend here when adding new document types.
# `original_template` is used only by the walk-and-replace FALLBACK path; if it
# is missing (e.g., a template was renamed/swapped), the pipeline still works
# via docxtpl — the fallback just won't be available for that type.
UPLOADS = HERE.parent / "03-original-templates"
DOC_TYPES = {
    "procedure": {
        "jinja_template": TEMPLATES / "Procedure Template (Jinja).docx",
        "original_template_candidates": [
            UPLOADS / "NextDecade Blank Procedure Template_Rev 1 April 9th 2026.docx",
        ],
        "schema": TEMPLATES / "procedure_schema.json",
        "fallback": "walk_replace_procedure",
    },
    "standard": {
        "jinja_template": TEMPLATES / "Standard Template (Jinja).docx",
        "original_template_candidates": [UPLOADS / "Standard Template.docx"],
        "schema": TEMPLATES / "standard_schema.json",
        "fallback": "walk_replace_standard",
    },
    "guidance": {
        "jinja_template": TEMPLATES / "Guidance Template (Jinja).docx",
        "original_template_candidates": [UPLOADS / "Guidance Template.docx"],
        "schema": TEMPLATES / "guidance_schema.json",
        "fallback": "walk_replace_guidance",
    },
}

def _resolve_original(doc_type: str) -> Path | None:
    for cand in DOC_TYPES[doc_type]["original_template_candidates"]:
        if cand.exists():
            return cand
    return None


def _strict_env():
    from jinja2 import Environment, StrictUndefined
    return Environment(undefined=StrictUndefined, autoescape=False)


def render_via_docxtpl(data: dict, template: Path, output: Path) -> None:
    from docxtpl import DocxTemplate
    tpl = DocxTemplate(str(template))
    tpl.render(data, jinja_env=_strict_env())
    tpl.save(str(output))


def _post_render_cover_fixup(output: Path, data: dict, doc_type: str) -> list[str]:
    """Patch cover-page text boxes and headers in the rendered .docx.

    The Standard and Guidance Jinja templates have plain-text placeholders
    ("NAME", "xxx-xxx-xxx-xxx-xxx-#####") inside text boxes and headers that
    docxtpl cannot reach because they're not Jinja markers. This function
    does a targeted XML search-and-replace inside the .docx zip.

    Returns a list of patches applied (for logging).
    """
    import re, zipfile

    doc_name = data.get("document_name", "")
    doc_num = data.get("doc_number", "")
    if not doc_name and not doc_num:
        return []

    # Define replacements per doc type
    type_label = {"standard": "STANDARD", "guidance": "GUIDANCE"}.get(doc_type)
    if type_label is None:
        return []  # procedure has its own cover-page handling via docxtpl markers

    replacements = []
    if doc_name:
        # Cover text box: "NAME" (standalone or part of "NAME STANDARD DOCUMENT")
        replacements.append(("NAME", doc_name))
        # Header: "[Name] Standard" or "[GUIDANCE Document NAME]"
        replacements.append((f"[Name] {type_label.title()}", f"{doc_name}"))
        replacements.append((f"[{type_label} Document NAME]", f"{doc_name}"))
    if doc_num:
        # Cover text box uses "xxx-xxx-xxx-xxx-xxx-#####"; headers may use
        # "xxx-xxx-xxx-xxx-xxx-" (trailing dash, no #####). Replace both.
        replacements.append(("xxx-xxx-xxx-xxx-xxx-#####", doc_num))
        replacements.append(("Doc. No. xxx-xxx-xxx-xxx-xxx-", f"Doc. No. {doc_num}"))

    patches = []
    with zipfile.ZipFile(output) as zin:
        files = {n: zin.read(n) for n in zin.namelist()}
        infos = {n: zin.getinfo(n) for n in zin.namelist()}

    target_parts = [n for n in files if n.startswith("word/") and n.endswith(".xml")]
    for part_name in target_parts:
        content = files[part_name].decode("utf-8")
        changed = False
        for old, new in replacements:
            if old in content:
                content = content.replace(old, new)
                patches.append(f"{part_name}: '{old}' -> '{new}'")
                changed = True
        if changed:
            files[part_name] = content.encode("utf-8")

    if patches:
        with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as zout:
            for name, data_bytes in files.items():
                zout.writestr(infos[name], data_bytes)

    return patches


# ---------------------------------------------------------------------------
# Walk-and-replace fallback (per-doc-type)
# ---------------------------------------------------------------------------
def _wr_common_setup(original: Path, output: Path):
    from docx import Document
    from copy import deepcopy
    from docx.text.paragraph import Paragraph
    shutil.copy2(original, output)
    doc = Document(str(output))

    def _set(p, text):
        runs = p.runs
        if not runs: p.add_run(text); return
        runs[0].text = text
        for r in runs[1:]:
            r._element.getparent().remove(r._element)

    def _h1(token):
        for i, p in enumerate(doc.paragraphs):
            if p.style and p.style.name == "Heading 1" and token.lower() in p.text.strip().lower():
                return i
        return None

    def _fill_after(idx, text):
        if idx is None: return
        for k in range(idx + 1, len(doc.paragraphs)):
            p = doc.paragraphs[k]
            if p.style and p.style.name == "Heading 1": return
            if p.text.strip(): _set(p, text); return

    return doc, _set, _h1, _fill_after, deepcopy, Paragraph


def _wr_fill_content_sections(doc, data, _set, deepcopy, Paragraph):
    sections = data["content_sections"]
    slots = [i for i, p in enumerate(doc.paragraphs)
             if p.style and p.style.name == "Heading 1" and "[CONTENT TITLE]" in p.text]

    def fill(heading_idx, section):
        h = doc.paragraphs[heading_idx]
        _set(h, section["title"])
        intro_set = False
        bullet_paragraphs = []
        for k in range(heading_idx + 1, len(doc.paragraphs)):
            p = doc.paragraphs[k]
            if p.style and p.style.name == "Heading 1": break
            if not p.text.strip(): continue
            if not intro_set:
                _set(p, section["intro"]); intro_set = True
            else:
                bullet_paragraphs.append(p)
        bullets = section["bullets"]
        if len(bullets) <= len(bullet_paragraphs):
            for i, b in enumerate(bullets):
                _set(bullet_paragraphs[i], b)
            for extra in bullet_paragraphs[len(bullets):]:
                extra._element.getparent().remove(extra._element)
        else:
            for i, p in enumerate(bullet_paragraphs):
                _set(p, bullets[i])
            last = bullet_paragraphs[-1]
            for b in bullets[len(bullet_paragraphs):]:
                new_el = deepcopy(last._element)
                last._element.addnext(new_el)
                last = Paragraph(new_el, last._parent)
                _set(last, b)

    n_slots, n_sections = len(slots), len(sections)
    if n_sections <= n_slots:
        for i in range(n_sections):
            slot_idx = [j for j, p in enumerate(doc.paragraphs)
                        if p.style and p.style.name == "Heading 1"
                        and "[CONTENT TITLE]" in p.text][0]
            fill(slot_idx, sections[i])
        while True:
            remaining = [j for j, p in enumerate(doc.paragraphs)
                         if p.style and p.style.name == "Heading 1"
                         and "[CONTENT TITLE]" in p.text]
            if not remaining: break
            s = remaining[0]
            h = doc.paragraphs[s]
            to_remove = [h._element]
            for k in range(s + 1, len(doc.paragraphs)):
                p = doc.paragraphs[k]
                if p.style and p.style.name == "Heading 1": break
                to_remove.append(p._element)
            for el in to_remove:
                el.getparent().remove(el)
    else:
        for i in range(n_slots):
            slot_idx = [j for j, p in enumerate(doc.paragraphs)
                        if p.style and p.style.name == "Heading 1"
                        and "[CONTENT TITLE]" in p.text][0]
            fill(slot_idx, sections[i])
        last_title = sections[n_slots - 1]["title"]
        last_h_idx = max(j for j, p in enumerate(doc.paragraphs)
                         if p.style and p.style.name == "Heading 1"
                         and p.text.strip() == last_title)
        end_idx = len(doc.paragraphs)
        for k in range(last_h_idx + 1, len(doc.paragraphs)):
            p = doc.paragraphs[k]
            if p.style and p.style.name == "Heading 1":
                end_idx = k; break
        block_elements = [doc.paragraphs[i]._element for i in range(last_h_idx, end_idx)]
        insert_after = block_elements[-1]
        for sec in sections[n_slots:]:
            new_elements = [deepcopy(el) for el in block_elements]
            for el in new_elements:
                insert_after.addnext(el); insert_after = el
            new_h_idx = max(j for j, p in enumerate(doc.paragraphs)
                            if p.style and p.style.name == "Heading 1"
                            and p.text.strip() == last_title)
            fill(new_h_idx, sec)


def _wr_fill_tables(doc, table_plans, _set):
    for t in doc.tables:
        headers = tuple(c.text.strip() for c in t.rows[0].cells)
        for plan in table_plans:
            if headers[:len(plan["match"])] == plan["match"]:
                plan["apply"](t)
                break


def walk_replace_procedure(data: dict, output: Path):
    """Walk-and-replace fallback for the NextDecade Blank Procedure Template
    (Rev 1, April 9 2026 layout). Used when the Jinja template is damaged.

    Targets the new schema (procedure_title, doc_number, header_date, revision,
    revision_history, change_log, purpose_text, scope_text, roles_intro, roles,
    ppe_paragraphs, procedure_section_title, procedure_intro, steps_intro,
    steps, recordkeeping_text, terms_intro, definitions, abbreviations_intro,
    abbreviations, references, appendices).
    """
    original = _resolve_original("procedure")
    if original is None:
        raise RuntimeError("No procedure template available for walk-and-replace fallback.")
    from docx import Document
    from copy import deepcopy
    from docx.text.paragraph import Paragraph
    shutil.copy2(original, output)
    doc = Document(str(output))

    def _set(p, text):
        runs = p.runs
        if not runs: p.add_run(text); return
        runs[0].text = text
        for r in runs[1:]:
            r._element.getparent().remove(r._element)

    # ---- Cover page ----
    for p in doc.paragraphs:
        if p.style and p.style.name == "Title Cover Page (Proc Title)":
            _set(p, data["procedure_title"]); break
    for p in doc.paragraphs:
        if p.style and p.style.name == "DocNumberOnCover":
            _set(p, data["doc_number"]); break

    # ---- Body H1 / body paragraph replacements (style-scoped to avoid TOC) ----
    def _set_body_after_h1(h1_text: str, new_text: str, body_substring: str = None):
        """Replace the first BodyText paragraph after the H1 matching ``h1_text``.
        If ``body_substring`` is set, instead match the BodyText paragraph that
        contains that substring (anywhere)."""
        if body_substring is not None:
            for p in doc.paragraphs:
                if p.style and p.style.name == "Body Text" and body_substring in p.text:
                    _set(p, new_text); return
            return
        for i, p in enumerate(doc.paragraphs):
            if p.style and p.style.name == "RGLNG 1 (Hdg1)" and h1_text.lower() in p.text.lower():
                # find next BodyText
                for q in doc.paragraphs[i+1:]:
                    if q.style and q.style.name == "RGLNG 1 (Hdg1)": return
                    if q.style and q.style.name == "Body Text":
                        _set(q, new_text); return
                return

    _set_body_after_h1(None, data["purpose_text"],
                       body_substring="The purpose of this procedure is to XXXX.")
    _set_body_after_h1(None, data["scope_text"],
                       body_substring="This procedure applies to all individuals")
    _set_body_after_h1(None, data["roles_intro"],
                       body_substring="Roles and responsibilities for this procedure")
    _set_body_after_h1(None, data["procedure_intro"],
                       body_substring="Procedure body goes here.")
    _set_body_after_h1(None, data["steps_intro"],
                       body_substring="The XXX completes the following:")
    _set_body_after_h1(None, data["recordkeeping_text"],
                       body_substring="Record keeping and training requirements")
    _set_body_after_h1(None, data["terms_intro"],
                       body_substring="The following terms are specific to this document.")
    _set_body_after_h1(None, data["abbreviations_intro"],
                       body_substring="The following abbreviations and acronyms are specific to this document.")

    # Section 5.0 H1 — replace via style filter so we don't hit the TOC
    for p in doc.paragraphs:
        if p.style and p.style.name == "RGLNG 1 (Hdg1)" \
                and "Procedure Title (Enter procedure here.)" in p.text:
            _set(p, data["procedure_section_title"]); break

    # 4.1 PPE — two source paragraphs; replace each, then clone/extend if more
    ppe_paragraphs = [p for p in doc.paragraphs
                      if p.style and p.style.name == "Body Text"
                      and ("In all areas except administrative offices" in p.text
                           or p.text.startswith("Refer to ORG-NDT-000010-SAF-PRC-00012"))]
    target_ppe = data["ppe_paragraphs"]
    for i, txt in enumerate(target_ppe):
        if i < len(ppe_paragraphs):
            _set(ppe_paragraphs[i], txt)
        else:
            last = ppe_paragraphs[-1]
            new_el = deepcopy(last._element)
            last._element.addnext(new_el)
            new_p = Paragraph(new_el, last._parent)
            _set(new_p, txt)
            ppe_paragraphs.append(new_p)
    # Trim extra source PPE paragraphs if data has fewer
    for extra in ppe_paragraphs[len(target_ppe):]:
        extra._element.getparent().remove(extra._element)

    # ---- Tables ----
    def _find_table(predicate):
        for t in doc.tables:
            headers = [c.text.strip() for c in t.rows[0].cells]
            if predicate(headers):
                return t
        return None

    def _fill_simple_table(t, data_rows: list[tuple]):
        """Fill table data rows starting from row 1 with ``data_rows``
        (each tuple has one string per cell). Adds rows if needed; deletes
        extra prefilled rows."""
        prefilled = list(t.rows)[1:]
        for i, tup in enumerate(data_rows):
            if i < len(prefilled):
                row = prefilled[i]
                for j, cell_text in enumerate(tup):
                    if j < len(row.cells):
                        _set(row.cells[j].paragraphs[0], cell_text)
            else:
                new_row = t.add_row()
                for j, cell_text in enumerate(tup):
                    if j < len(new_row.cells):
                        new_row.cells[j].text = cell_text
        for r in prefilled[len(data_rows):]:
            r._element.getparent().remove(r._element)

    # Revision History
    rev_t = _find_table(lambda h: h and h[0] == "Revision History")
    if rev_t is not None:
        # Skip the merged "Revision History" row AND the column-header row
        # (rows 0 and 1). Data starts at row 2.
        data_rev_rows = [(r["rev"], r["date"], r["description"],
                          r["originator"], r["reviewer"], r["approver"])
                         for r in data["revision_history"]]
        prefilled = list(rev_t.rows)[2:]
        for i, tup in enumerate(data_rev_rows):
            if i < len(prefilled):
                row = prefilled[i]
                for j, cell_text in enumerate(tup):
                    _set(row.cells[j].paragraphs[0], cell_text)
            else:
                new_row = rev_t.add_row()
                for j, cell_text in enumerate(tup):
                    new_row.cells[j].text = cell_text
        for r in prefilled[len(data_rev_rows):]:
            r._element.getparent().remove(r._element)

    # Change Log
    clog_t = _find_table(lambda h: tuple(h) == ("Revision", "Description of Changes and Notes"))
    if clog_t is not None:
        _fill_simple_table(clog_t, [(c["revision"], c["description"]) for c in data["change_log"]])

    # Roles & Responsibilities (responsibilities cell takes a list rendered as paragraphs)
    roles_t = _find_table(lambda h: tuple(h) == ("Role", "Responsibilities"))
    if roles_t is not None:
        prefilled = list(roles_t.rows)[1:]
        for i, role in enumerate(data["roles"]):
            if i < len(prefilled):
                row = prefilled[i]
            else:
                row = roles_t.add_row()
            _set(row.cells[0].paragraphs[0], role["role"])
            # Wipe the responsibilities cell and write each responsibility as a paragraph
            r_cell = row.cells[1]
            for extra in list(r_cell.paragraphs[1:]):
                extra._element.getparent().remove(extra._element)
            lines = role["responsibilities"]
            if lines:
                _set(r_cell.paragraphs[0], lines[0])
                for extra in lines[1:]:
                    r_cell.add_paragraph(extra)
            else:
                _set(r_cell.paragraphs[0], "")
        for r in prefilled[len(data["roles"]):]:
            r._element.getparent().remove(r._element)

    # Steps
    steps_t = _find_table(lambda h: tuple(h) == ("Step", "Description"))
    if steps_t is not None:
        _fill_simple_table(steps_t, [(s["step"], s["description"]) for s in data["steps"]])

    # Definitions
    terms_t = _find_table(lambda h: tuple(h) == ("Term", "Definition"))
    if terms_t is not None:
        _fill_simple_table(terms_t, [(d["term"], d["definition"]) for d in data["definitions"]])

    # Abbreviations
    abbr_t = _find_table(lambda h: tuple(h) == ("Abbreviation/Acronym", "Definition"))
    if abbr_t is not None:
        _fill_simple_table(abbr_t, [(a["abbreviation"], a["definition"]) for a in data["abbreviations"]])

    # References
    refs_t = _find_table(lambda h: tuple(h) == ("Document Number", "Document Title"))
    if refs_t is not None:
        _fill_simple_table(refs_t, [(ref["number"], ref["title"]) for ref in data["references"]])

    # Appendices: source has two prefilled headings ("Example 1", "Example 2");
    # extend or trim to match data["appendices"]. Each appendix = 1 heading + 1 body.
    apdx_paras = [p for p in doc.paragraphs
                  if p.style and p.style.name == "RGLNG Appendix Hdg 1"]
    target_n = len(data["appendices"])
    if apdx_paras:
        # Each prefilled appendix has structure: heading, body, body (3 paras)
        # Find body paragraphs immediately after each appendix heading
        def _bodies_after(heading_p, n_max=2):
            bodies = []
            after = heading_p._element.getnext()
            while after is not None and len(bodies) < n_max:
                from docx.oxml.ns import qn
                if after.tag != qn("w:p"): break
                # Check style
                pPr = after.find(qn("w:pPr"))
                if pPr is not None:
                    pStyle = pPr.find(qn("w:pStyle"))
                    if pStyle is not None and pStyle.get(qn("w:val")) == "RGLNGAppendixHdg1":
                        break
                bodies.append(Paragraph(after, heading_p._parent))
                after = after.getnext()
            return bodies

        # Reuse / extend / trim the appendix slots
        if target_n == 0:
            # Delete every appendix block
            for h in apdx_paras:
                bodies = _bodies_after(h)
                for b in bodies:
                    b._element.getparent().remove(b._element)
                h._element.getparent().remove(h._element)
        else:
            # Make sure we have target_n appendix slots; clone the LAST one as needed
            while len(apdx_paras) < target_n:
                last_h = apdx_paras[-1]
                last_bodies = _bodies_after(last_h)
                # Clone heading + bodies and append at end of body
                new_h_el = deepcopy(last_h._element)
                last_anchor = (last_bodies[-1]._element
                               if last_bodies else last_h._element)
                last_anchor.addnext(new_h_el)
                new_h = Paragraph(new_h_el, last_h._parent)
                anchor = new_h_el
                for b in last_bodies:
                    new_b_el = deepcopy(b._element)
                    anchor.addnext(new_b_el); anchor = new_b_el
                apdx_paras.append(new_h)
            # Trim extras
            for h in apdx_paras[target_n:]:
                bodies = _bodies_after(h)
                for b in bodies:
                    b._element.getparent().remove(b._element)
                h._element.getparent().remove(h._element)
            apdx_paras = apdx_paras[:target_n]
            # Fill
            for h, app in zip(apdx_paras, data["appendices"]):
                _set(h, app["title"])
                bodies = _bodies_after(h)
                if bodies:
                    _set(bodies[0], app["body"])
                    # Delete extra prefilled body paragraphs
                    for extra in bodies[1:]:
                        extra._element.getparent().remove(extra._element)

    # ---- Delete the source-template "Sample Styles" section so the fallback
    # output matches the docxtpl path (which removes that section in the Jinja
    # template). The section runs from H1 "Sample Styles" through (exclusive of)
    # H1 "Definitions".
    from docx.oxml.ns import qn as _qn
    body_el = doc.element.body
    body_children = list(body_el)
    def _txt(el):
        return "".join(t.text or "" for t in el.iter(_qn("w:t")))
    def _is_h1(el, label):
        if el.tag != _qn("w:p"): return False
        pStyle = el.find(_qn("w:pPr") + "/" + _qn("w:pStyle"))
        if pStyle is None or pStyle.get(_qn("w:val")) != "RGLNG1Hdg1": return False
        return _txt(el).strip() == label
    start, end = None, None
    for i, el in enumerate(body_children):
        if _is_h1(el, "Sample Styles"): start = i
        elif start is not None and _is_h1(el, "Definitions"):
            end = i; break
    if start is not None and end is not None:
        for el in body_children[start:end]:
            body_el.remove(el)

    # ---- Header (header2.xml is referenced from the section's headerReference)
    # Header text replacement requires editing header2.xml inside the .docx.
    # python-docx doesn't make this trivial; do it via lxml on the part XML.
    _patch_header2(doc, data)

    doc.save(str(output))


def _patch_header2(doc, data: dict):
    """Replace static text in word/header2.xml with the values from ``data``."""
    from lxml import etree
    W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    # Find the header part; python-docx exposes section.header.part
    for section in doc.sections:
        for header in (section.header, section.first_page_header, section.even_page_header):
            try:
                part = header.part
            except Exception:
                continue
            xml = part.element
            for p in xml.iter(W + "p"):
                runs = list(p.iter(W + "r"))
                if not runs: continue
                full = "".join("".join(t.text or "" for t in r.iter(W + "t")) for r in runs)
                target = None
                if full.strip().startswith("Date:") and "header_date" in data:
                    target = ("Date: ", data["header_date"])
                elif full.strip() == "Blank Procedure Template":
                    target = (None, data["procedure_title"])
                elif full.strip().startswith("Rev.:"):
                    target = ("Rev.: ", data["revision"])
                elif "000-NTD-000-xxx-xxx-000xx" in full:
                    target = (None, data["doc_number"])
                if target is None: continue
                prefix, value = target
                first_run = runs[0]
                for t in first_run.findall(W + "t"):
                    first_run.remove(t)
                t_el = etree.SubElement(first_run, W + "t")
                t_el.text = (prefix or "") + value
                t_el.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
                for r in runs[1:]:
                    parent = r.getparent()
                    if parent is not None:
                        parent.remove(r)


def walk_replace_standard(data: dict, output: Path):
    original = _resolve_original("standard")
    if original is None: raise RuntimeError("No standard template available for walk-and-replace fallback.")
    doc, _set, _h1, _fill_after, deepcopy, Paragraph = _wr_common_setup(original, output)
    _fill_after(_h1("INTRODUCTION"),             data["introduction_text"])
    _fill_after(_h1("SCOPE"),                    data["scope_text"])
    _fill_after(_h1("INTEGRATED GOVERNANCE"),    data["governance_text"])
    _fill_after(_h1("EXCEPTION REQUEST"),        data["exception_text"])
    _fill_after(_h1("CONTINUOUS IMPROVEMENT"),   data["continuous_text"])
    _wr_fill_content_sections(doc, data, _set, deepcopy, Paragraph)
    _wr_fill_tables(doc, _std_proc_table_plans(data, _set), _set)
    doc.save(str(output))


def walk_replace_guidance(data: dict, output: Path):
    original = _resolve_original("guidance")
    if original is None: raise RuntimeError("No guidance template available for walk-and-replace fallback.")
    doc, _set, _h1, _fill_after, deepcopy, Paragraph = _wr_common_setup(original, output)
    _fill_after(_h1("PURPOSE"),                  data["purpose_text"])
    # Remove leftover template boilerplate paragraphs in PURPOSE section
    _boilerplate_markers = [
        "Best Practices Recommendations",  # covers smart-quote variants
        "The Guideline applies to all employees, officers, directors",
    ]
    for p in list(doc.paragraphs):
        for marker in _boilerplate_markers:
            if marker in p.text:
                p._element.getparent().remove(p._element)
                break
    _fill_after(_h1("INTEGRATED GOVERNANCE"),    data["governance_text"])
    # GUIDELINE: intro + bullets (no title repetition)
    gi = _h1("GUIDELINE")
    if gi is not None:
        intro_set = False
        bullet_paragraphs = []
        for k in range(gi + 1, len(doc.paragraphs)):
            p = doc.paragraphs[k]
            if p.style and p.style.name == "Heading 1": break
            if not p.text.strip(): continue
            if not intro_set:
                _set(p, data["guideline_intro"]); intro_set = True
            else:
                bullet_paragraphs.append(p)
        bullets = data["guideline_bullets"]
        if len(bullets) <= len(bullet_paragraphs):
            for i, b in enumerate(bullets):
                _set(bullet_paragraphs[i], b)
            for extra in bullet_paragraphs[len(bullets):]:
                extra._element.getparent().remove(extra._element)
        else:
            for i, p in enumerate(bullet_paragraphs):
                _set(p, bullets[i])
            last = bullet_paragraphs[-1]
            for b in bullets[len(bullet_paragraphs):]:
                new_el = deepcopy(last._element)
                last._element.addnext(new_el)
                last = Paragraph(new_el, last._parent)
                _set(last, b)

    _wr_fill_tables(doc, _table_plans_guidance(data, _set), _set)
    doc.save(str(output))


def _std_proc_table_plans(data, _set):
    def fill_defs(t):
        data_rows = list(t.rows)[1:]
        for i, d in enumerate(data["definitions"]):
            if i < len(data_rows):
                r = data_rows[i]
                _set(r.cells[0].paragraphs[0], d["no"])
                _set(r.cells[1].paragraphs[0], d["term"])
                _set(r.cells[2].paragraphs[0], d["definition"])
            else:
                new_row = t.add_row()
                new_row.cells[0].text = d["no"]
                new_row.cells[1].text = d["term"]
                new_row.cells[2].text = d["definition"]
        for r in data_rows[len(data["definitions"]):]:
            r._element.getparent().remove(r._element)

    def fill_refs(t):
        data_rows = list(t.rows)[1:]
        for i, ref in enumerate(data["references"]):
            if i < len(data_rows):
                r = data_rows[i]
                _set(r.cells[0].paragraphs[0], ref["title"])
                _set(r.cells[1].paragraphs[0], ref["number"])
            else:
                new_row = t.add_row()
                new_row.cells[0].text = ref["title"]
                new_row.cells[1].text = ref["number"]
        for r in data_rows[len(data["references"]):]:
            r._element.getparent().remove(r._element)

    return [
        {"match": ("No.", "Term", "Definition"), "apply": fill_defs},
        {"match": ("Title", "Document Number"), "apply": fill_refs},
    ] + _table_plans_common(data, _set)


def _table_plans_guidance(data, _set):
    return _table_plans_common(data, _set)


def _table_plans_common(data, _set):
    def fill_raci(t):
        if len(t.rows) > 1:
            r = t.rows[1]
            raci = data["raci"]
            _set(r.cells[0].paragraphs[0], raci["responsible"])
            _set(r.cells[1].paragraphs[0], raci["accountable"])
            _set(r.cells[2].paragraphs[0], raci["consulted"])
            _set(r.cells[3].paragraphs[0], raci["informed"])

    def fill_approval(t):
        if len(t.rows) > 1:
            r = t.rows[1]
            ap = data["approval"]
            _set(r.cells[0].paragraphs[0], ap["issuer"])
            _set(r.cells[1].paragraphs[0], ap["adopted_by"])
            _set(r.cells[2].paragraphs[0], ap["effective_date"])

    def fill_rev(t):
        data_rows = list(t.rows)[1:]
        for i, rev in enumerate(data["revision_history"]):
            if i < len(data_rows):
                r = data_rows[i]
                _set(r.cells[0].paragraphs[0], rev["number"])
                _set(r.cells[1].paragraphs[0], rev["description"])
            else:
                new_row = t.add_row()
                new_row.cells[0].text = rev["number"]
                new_row.cells[1].text = rev["description"]
        for r in data_rows[len(data["revision_history"]):]:
            r._element.getparent().remove(r._element)

    return [
        {"match": ("Responsible", "Accountable", "Consulted", "Informed"), "apply": fill_raci},
        {"match": ("Issuer / Title", "Adopted By", "Effective / Amended Date"), "apply": fill_approval},
        {"match": ("Revision", "Description of Changes and Notes"), "apply": fill_rev},
    ]


FALLBACK_FNS = {
    "walk_replace_procedure": walk_replace_procedure,
    "walk_replace_standard":  walk_replace_standard,
    "walk_replace_guidance":  walk_replace_guidance,
}


# ---------------------------------------------------------------------------
# PDF export via LibreOffice
# ---------------------------------------------------------------------------
def convert_to_pdf(docx_path: Path, pdf_path: Path | None = None) -> Path:
    """Convert a .docx to .pdf via headless LibreOffice (soffice).

    soffice must be installed with the Writer component. On Debian/Ubuntu:
      apt-get install libreoffice-writer

    Uses an isolated -env:UserInstallation profile so concurrent soffice
    invocations don't collide on shared profile state (required in sandboxes).
    """
    import tempfile
    docx_path = Path(docx_path)
    if pdf_path is None:
        pdf_path = docx_path.with_suffix(".pdf")
    out_dir = pdf_path.parent
    out_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmpdir:
        profile_arg = f"-env:UserInstallation=file://{tmpdir}/lo_profile"
        cmd = ["soffice", "--headless", profile_arg, "--convert-to", "pdf",
               "--outdir", str(out_dir), str(docx_path)]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        if result.returncode != 0:
            raise RuntimeError(
                f"LibreOffice conversion failed (exit {result.returncode}):\n"
                f"stderr: {result.stderr}\nstdout: {result.stdout}"
            )
    actual = out_dir / (docx_path.stem + ".pdf")
    if actual != pdf_path and actual.exists():
        shutil.move(str(actual), str(pdf_path))
    if not pdf_path.exists():
        raise RuntimeError(f"PDF was not produced at {pdf_path}")
    return pdf_path


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------
def render(doc_type: str, data: dict, output: str | Path,
           allow_fallback: bool = True, pdf: bool = False) -> dict:
    if doc_type not in DOC_TYPES:
        raise ValueError(f"Unknown doc_type {doc_type!r}. "
                         f"Expected one of: {sorted(DOC_TYPES)}")
    cfg = DOC_TYPES[doc_type]
    output = Path(output)
    report = {"doc_type": doc_type, "output": str(output), "path": None, "warnings": []}

    # Step 1: lint
    proc = subprocess.run(
        [sys.executable, str(LINTER), str(cfg["jinja_template"]), str(cfg["schema"])],
        capture_output=True, text=True,
    )
    lint_report = json.loads(proc.stdout) if proc.stdout else {}
    lint_exit = proc.returncode
    report["lint"] = {
        "exit": lint_exit,
        "issue_count": len(lint_report.get("issues", [])),
        "warning_count": len(lint_report.get("warnings", [])),
    }

    # Step 2: route
    if lint_exit in (0, 2):
        try:
            render_via_docxtpl(data, cfg["jinja_template"], output)
            report["path"] = "docxtpl"
            if lint_exit == 2:
                report["warnings"] = [w["message"] for w in lint_report.get("warnings", [])]
        except Exception as e:
            if allow_fallback:
                FALLBACK_FNS[cfg["fallback"]](data, output)
                report["path"] = "walk_and_replace_fallback"
                report["warnings"].append(f"docxtpl raised: {e}; used fallback")
            else:
                raise
    else:
        if allow_fallback:
            FALLBACK_FNS[cfg["fallback"]](data, output)
            report["path"] = "walk_and_replace_fallback"
            report["warnings"].append(
                "Jinja template has unrecoverable issues; rendered via walk-and-replace. "
                "Fix the Jinja template to restore the fast path."
            )
            report["lint_issues"] = lint_report.get("issues", [])
        else:
            raise RuntimeError(
                f"Template lint failed with exit {lint_exit}; fallback disabled. "
                f"Issues: {lint_report.get('issues')}"
            )

    # Step 2.5: post-render cover-page fixup (Standard/Guidance text boxes + headers)
    try:
        cover_patches = _post_render_cover_fixup(output, data, doc_type)
        if cover_patches:
            report["cover_patches"] = cover_patches
    except Exception as e:
        report["warnings"].append(f"Cover-page fixup failed: {e}")

    # Step 3: optional PDF
    if pdf:
        try:
            pdf_path = convert_to_pdf(output)
            report["pdf"] = str(pdf_path)
        except Exception as e:
            report["warnings"].append(f"PDF export failed: {e}")
    return report


# Back-compat shim for the original entry point
def render_procedure(data: dict, output, allow_fallback: bool = True) -> dict:
    return render("procedure", data, output, allow_fallback=allow_fallback)


def main():
    if len(sys.argv) < 4:
        print("Usage: render_docx.py <doc_type> <input.json> <output.docx> "
              "[--pdf] [--no-fallback]", file=sys.stderr)
        print(f"  doc_type one of: {sorted(DOC_TYPES)}", file=sys.stderr)
        sys.exit(64)
    doc_type = sys.argv[1]
    data = json.loads(Path(sys.argv[2]).read_text())
    output = sys.argv[3]
    pdf = "--pdf" in sys.argv
    allow_fallback = "--no-fallback" not in sys.argv
    report = render(doc_type, data, output, allow_fallback=allow_fallback, pdf=pdf)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
