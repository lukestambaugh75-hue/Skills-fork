#!/usr/bin/env python3
"""Build `Procedure Template (Jinja).docx` from the NextDecade Blank Procedure
Template (Rev 1, April 9 2026 layout) by injecting docxtpl markers.

Re-run this script after the source template (in
`NextDecade-Claude-Project/03-original-templates/`) is updated. The output
overwrites `skills/docx/templates/Procedure Template (Jinja).docx`.

Usage:
    python skills/docx/scripts/build_procedure_jinja.py

Requires: python-docx, lxml.
"""
from __future__ import annotations
import shutil, zipfile, re, tempfile
from copy import deepcopy
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn  # noqa: F401

REPO = Path(__file__).resolve().parents[3]
SRC = REPO / "NextDecade-Claude-Project" / "03-original-templates" / \
    "NextDecade Blank Procedure Template_Rev 1 April 9th 2026.docx"
DST = REPO / "skills" / "docx" / "templates" / \
    "Procedure Template (Jinja).docx"

assert SRC.exists(), f"Source template not found: {SRC}"

_tmp = tempfile.mkdtemp(prefix="build_jinja_")
WORK = Path(_tmp) / "work.docx"
shutil.copy2(SRC, WORK)


def set_paragraph_text(p, text: str):
    """Replace paragraph text with ``text``, preserving the paragraph style and
    the formatting of the FIRST run; remove other runs."""
    runs = p.runs
    if not runs:
        p.add_run(text)
        return
    runs[0].text = text
    for r in runs[1:]:
        r._element.getparent().remove(r._element)


def find_para_by_text(paragraphs, needle: str, style_name: str | None = None):
    """Return index of first paragraph containing ``needle`` (case-sensitive).
    If ``style_name`` is provided, only paragraphs with that style match."""
    for i, p in enumerate(paragraphs):
        if needle not in p.text:
            continue
        if style_name is not None:
            if not (p.style and p.style.name == style_name):
                continue
        return i
    return None


def delete_row(row):
    row._element.getparent().remove(row._element)


def wrap_row_with_tr_loop(row, for_directive: str, endfor_directive: str = "{%tr endfor %}"):
    """Insert a directive row BEFORE ``row`` carrying ``for_directive`` and
    another row AFTER ``row`` carrying ``endfor_directive``. The directive rows
    have the same column structure as ``row`` but the directive text is placed
    in the FIRST cell only.

    docxtpl semantics: a row containing only a `{%tr ... %}` directive is
    REMOVED at render time, and the corresponding Jinja `{% ... %}` is
    injected. Rows between two `{%tr%}` directives get repeated per iteration.
    """
    tr_el = row._element
    tbl = tr_el.getparent()
    # Insert "for" directive row BEFORE the data row
    open_el = deepcopy(tr_el)
    # Wipe text from every cell, then put the directive in cell 0
    for tc in open_el.findall(qn("w:tc")):
        for p in tc.findall(qn("w:p")):
            for r_el in p.findall(qn("w:r")):
                p.remove(r_el)
    first_tc = open_el.find(qn("w:tc"))
    first_p = first_tc.find(qn("w:p"))
    if first_p is None:
        from lxml import etree
        first_p = etree.SubElement(first_tc, qn("w:p"))
    new_r = first_p.makeelement(qn("w:r"), {})
    new_t = first_p.makeelement(qn("w:t"), {})
    new_t.text = for_directive
    new_r.append(new_t)
    first_p.append(new_r)
    tr_el.addprevious(open_el)
    # Insert "endfor" directive row AFTER the data row (clone again)
    close_el = deepcopy(tr_el)
    for tc in close_el.findall(qn("w:tc")):
        for p in tc.findall(qn("w:p")):
            for r_el in p.findall(qn("w:r")):
                p.remove(r_el)
    first_tc = close_el.find(qn("w:tc"))
    first_p = first_tc.find(qn("w:p"))
    if first_p is None:
        from lxml import etree
        first_p = etree.SubElement(first_tc, qn("w:p"))
    new_r = first_p.makeelement(qn("w:r"), {})
    new_t = first_p.makeelement(qn("w:t"), {})
    new_t.text = endfor_directive
    new_r.append(new_t)
    first_p.append(new_r)
    tr_el.addnext(close_el)


# ---------------------------------------------------------------------------
# 1. Open as python-docx Document
# ---------------------------------------------------------------------------
doc = Document(str(WORK))
paras = doc.paragraphs

# ---------------------------------------------------------------------------
# 2. Cover page (paragraphs 0..)
# ---------------------------------------------------------------------------
# Cover-page title and doc number
i = find_para_by_text(paras, "Blank Procedure Template")
assert i is not None, "Cover title paragraph not found"
set_paragraph_text(paras[i], "{{ procedure_title }}")

i = find_para_by_text(paras, "000-NTD-000-xxx-xxx-000xx")
assert i is not None, "Cover doc-number paragraph not found"
set_paragraph_text(paras[i], "{{ doc_number }}")

# ---------------------------------------------------------------------------
# 3. Body paragraphs
# ---------------------------------------------------------------------------
def repl_text(needle: str, marker: str, *, must_exist=True, style: str | None = None):
    idx = find_para_by_text(doc.paragraphs, needle, style_name=style)
    if idx is None:
        if must_exist: raise RuntimeError(f"Not found: {needle!r} (style={style!r})")
        return False
    set_paragraph_text(doc.paragraphs[idx], marker)
    return True

repl_text("The purpose of this procedure is to XXXX.", "{{ purpose_text }}")
repl_text("This procedure applies to all individuals performing work for or on behalf of NextDecade",
          "{{ scope_text }}")
repl_text("Roles and responsibilities for this procedure include the following.",
          "{{ roles_intro }}")

# 4.1 PPE — two paragraphs. docxtpl `{%p ... %}` removes the WHOLE paragraph
# it lives in, so the loop directive and the content paragraph must be in
# separate paragraphs. Pattern:
#   Para 1: {%p for p in ppe_paragraphs %}    <- removed
#   Para 2: {{ p }}                            <- repeats per iteration
#   Para 3: {%p endfor %}                      <- removed
# We have two source paragraphs to work with; clone the first to make a third.
ppe_idx_1 = find_para_by_text(doc.paragraphs,
    "In all areas except administrative offices")
ppe_idx_2 = find_para_by_text(doc.paragraphs,
    "Refer to ORG-NDT-000010-SAF-PRC-00012")
assert ppe_idx_1 is not None and ppe_idx_2 is not None
# Clone the first PPE paragraph (BodyText style) and insert it AFTER ppe_idx_2
# so we have three paragraphs in a row to host the for / body / endfor pattern.
src_p_el = doc.paragraphs[ppe_idx_1]._element
new_p_el = deepcopy(src_p_el)
doc.paragraphs[ppe_idx_2]._element.addnext(new_p_el)
# Now refresh paragraph indices
ppe_idx_1 = find_para_by_text(doc.paragraphs,
    "In all areas except administrative offices")
ppe_idx_for = ppe_idx_1
ppe_idx_body = ppe_idx_1 + 1
ppe_idx_end = ppe_idx_1 + 2
set_paragraph_text(doc.paragraphs[ppe_idx_for], "{%p for p in ppe_paragraphs %}")
set_paragraph_text(doc.paragraphs[ppe_idx_body], "{{ p }}")
set_paragraph_text(doc.paragraphs[ppe_idx_end], "{%p endfor %}")

# Section 5 - the procedure itself. Keep it simple: title + intro + steps.
# IMPORTANT: target the body H1 specifically (style "RGLNG 1 (Hdg1)") so the
# replacement does NOT accidentally hit the cached TOC entry that contains the
# same text.
repl_text("Procedure Title (Enter procedure here.)",
          "{{ procedure_section_title }}",
          style="RGLNG 1 (Hdg1)")
repl_text("Procedure body goes here.", "{{ procedure_intro }}")
repl_text("The XXX completes the following:", "{{ steps_intro }}")

# Section 6 (combined "Record Keeping Requirements and Training")
repl_text("Record keeping and training requirements", "{{ recordkeeping_text }}")

# 9.1 Terms intro
repl_text("The following terms are specific to this document.", "{{ terms_intro }}")
# 9.2 Abbreviations intro
repl_text("The following abbreviations and acronyms are specific to this document.",
          "{{ abbreviations_intro }}")

# Delete the "Sample Styles" section (H1 "Sample Styles" through the last
# paragraph of the "Figures" subsection, plus the sample table). This section
# is template-author documentation, not procedure content; including it in
# every rendered procedure is noise.
def _iter_body_top_level():
    """Yield top-level body children (paragraphs and tables) in document order."""
    body = doc.element.body
    return list(body)

W_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
body_children = _iter_body_top_level()
# Find the index of the "Sample Styles" H1 element
def _para_text(el):
    return "".join(t.text or "" for t in el.iter(W_NS + "t"))

def _para_style(el):
    pStyle = el.find(W_NS + "pPr/" + W_NS + "pStyle")
    return pStyle.get(W_NS + "val") if pStyle is not None else None

start_idx = None
end_idx = None  # exclusive
for i, el in enumerate(body_children):
    if el.tag != W_NS + "p":
        continue
    if _para_style(el) == "RGLNG1Hdg1" and _para_text(el).strip() == "Sample Styles":
        start_idx = i
    elif start_idx is not None and _para_style(el) == "RGLNG1Hdg1" \
            and _para_text(el).strip() == "Definitions":
        end_idx = i
        break

assert start_idx is not None and end_idx is not None, \
    f"Could not bracket Sample Styles section: start={start_idx}, end={end_idx}"
# Remove children body_children[start_idx : end_idx]
to_remove = body_children[start_idx:end_idx]
parent = doc.element.body
for el in to_remove:
    parent.remove(el)


# Appendices: rename "Example 1" -> {{ a.title }} via paragraph loop
# We'll mark the first appendix heading with {%p for a in appendices %}{{ a.title }},
# its body paragraph with {{ a.body }}, then mark a closing paragraph with {%p endfor %}
# Find the two RGLNGAppendixHdg1 paragraphs ("Example 1" and "Example 2")
appendix_idxs = [i for i, p in enumerate(doc.paragraphs)
                 if p.style and p.style.name == "RGLNG Appendix Hdg 1"]
assert len(appendix_idxs) >= 2, f"Expected 2 appendix headings, got {len(appendix_idxs)}"

# Strategy: collapse the two-appendix block into a paragraph-for loop so any
# number of appendices can be rendered.
#   Para A: "Example 1"      -> "{%p for a in appendices %}{{ a.title }}"
#   Para A+1: "" (BodyText)  -> "{{ a.body }}"
#   Para A+2: "" (BodyText)  -> DELETE
#   Para B (Example 2)       -> DELETE
#   Para B+1, B+2            -> "{%p endfor %}"  (one of them)
first_app = appendix_idxs[0]
second_app = appendix_idxs[1]
# Pattern (4 paragraphs):
#   {%p for a in appendices %}      <- removed
#   {{ a.title }}  (Appendix Hdg 1) <- repeats; gets the appendix-heading style
#   {{ a.body }}   (BodyText)       <- repeats; body of the appendix
#   {%p endfor %}                   <- removed
#
# The source has paragraphs in this order at the tail:
#   first_app:        "Example 1"     (RGLNG Appendix Hdg 1)
#   first_app+1:      ""              (BodyText)
#   first_app+2:      ""              (BodyText)
#   second_app:       "Example 2"     (RGLNG Appendix Hdg 1)
#   second_app+1:     ""              (BodyText)
#
# We need to:
#   - Insert a new paragraph BEFORE first_app for the {%p for%} directive
#     (use BodyText style so it doesn't change the visual flow).
#   - Keep first_app, replace its text with {{ a.title }} (preserves the
#     appendix-heading style).
#   - Keep first_app+1, replace its text with {{ a.body }} (preserves BodyText).
#   - Delete first_app+2, second_app, and second_app+1.
#   - Append a new paragraph at the end for {%p endfor %}.

# Insert a new "for" directive paragraph BEFORE first_app, using BodyText style.
from docx.oxml.ns import qn as _qn
new_for_p = deepcopy(doc.paragraphs[first_app + 1]._element)  # body BodyText style
doc.paragraphs[first_app]._element.addprevious(new_for_p)
# Now the appendix indices have all shifted by +1
appendix_idxs = [i for i, p in enumerate(doc.paragraphs)
                 if p.style and p.style.name == "RGLNG Appendix Hdg 1"]
first_app = appendix_idxs[0]
second_app = appendix_idxs[1]
# Set the inserted paragraph to be the loop start
set_paragraph_text(doc.paragraphs[first_app - 1], "{%p for a in appendices %}")
# Set first appendix heading and body
set_paragraph_text(doc.paragraphs[first_app], "{{ a.title }}")
set_paragraph_text(doc.paragraphs[first_app + 1], "{{ a.body }}")
# Append a new endfor paragraph at the END of the document body, using
# BodyText style so it doesn't disturb anything
last_p = doc.paragraphs[-1]
new_end_p = deepcopy(doc.paragraphs[first_app + 1]._element)  # BodyText
last_p._element.addnext(new_end_p)
set_paragraph_text(doc.paragraphs[-1], "{%p endfor %}")
# Delete everything between first_app+2 (inclusive) and the new endfor (exclusive).
last_para_idx = len(doc.paragraphs) - 1
to_delete = list(range(first_app + 2, last_para_idx))
for idx in reversed(to_delete):
    el = doc.paragraphs[idx]._element
    el.getparent().remove(el)


# ---------------------------------------------------------------------------
# 4. Tables
# ---------------------------------------------------------------------------
tables = doc.tables
print(f"Total tables: {len(tables)}")
for i, t in enumerate(tables):
    headers = [c.text.strip() for c in t.rows[0].cells]
    print(f"Table {i}: {len(t.rows)} rows  headers={headers}")

def find_table_by_first_row(predicate):
    for t in doc.tables:
        if predicate([c.text.strip() for c in t.rows[0].cells]):
            return t
    return None


# --- Revision History (the "Revision History" merged cell as row 0) ---
rev_table = find_table_by_first_row(lambda h: h and h[0] == "Revision History")
assert rev_table is not None
# Row 0: merged "Revision History" header
# Row 1: column headers (Rev, Date, Revision Description, Originator, Reviewer/Endorser, Approver)
# Row 2: "A | 04-09-12 | Issued for Review | xxx | xxx | xxx" — the first DATA row
# Rows 3+: empty (delete first, then wrap data row with directive rows)
for row in list(rev_table.rows)[3:]:
    delete_row(row)
data_row = rev_table.rows[2]
cells = data_row.cells
set_paragraph_text(cells[0].paragraphs[0], "{{ r.rev }}")
set_paragraph_text(cells[1].paragraphs[0], "{{ r.date }}")
set_paragraph_text(cells[2].paragraphs[0], "{{ r.description }}")
set_paragraph_text(cells[3].paragraphs[0], "{{ r.originator }}")
set_paragraph_text(cells[4].paragraphs[0], "{{ r.reviewer }}")
set_paragraph_text(cells[5].paragraphs[0], "{{ r.approver }}")
wrap_row_with_tr_loop(data_row, "{%tr for r in revision_history %}")


# --- Change Log (header: Revision | Description of Changes and Notes) ---
clog_table = find_table_by_first_row(
    lambda h: tuple(h) == ("Revision", "Description of Changes and Notes"))
assert clog_table is not None
# Row 0: headers; rows 1+: empty cells (24 of them)
for row in list(clog_table.rows)[2:]:
    delete_row(row)
body_row = clog_table.rows[1]
cells = body_row.cells
set_paragraph_text(cells[0].paragraphs[0], "{{ c.revision }}")
set_paragraph_text(cells[1].paragraphs[0], "{{ c.description }}")
wrap_row_with_tr_loop(body_row, "{%tr for c in change_log %}")


# --- Roles & Responsibilities (header: Role | Responsibilities) ---
roles_table = find_table_by_first_row(
    lambda h: tuple(h) == ("Role", "Responsibilities"))
assert roles_table is not None
# Row 0: headers; rows 1..5: prefilled examples. Replace row 1 as loop body
# Use a paragraph-loop in the responsibilities cell so callers can pass a list.
# Delete extra prefilled rows first
for row in list(roles_table.rows)[2:]:
    delete_row(row)
data_row = roles_table.rows[1]
cells = data_row.cells
set_paragraph_text(cells[0].paragraphs[0], "{{ r.role }}")
# Cell 1 (Responsibilities) needs a paragraph-loop so each responsibility
# string in the list becomes its own paragraph. Pattern (3 paragraphs in the
# cell):
#   {%p for line in r.responsibilities %}    <- removed
#   {{ line }}                                <- repeats per item
#   {%p endfor %}                             <- removed
respons_cell = cells[1]
first_p = respons_cell.paragraphs[0]
orig_style = first_p.style
# Wipe all existing paragraphs in the cell except the first
for extra in list(respons_cell.paragraphs[1:]):
    extra._element.getparent().remove(extra._element)
set_paragraph_text(first_p, "{%p for line in r.responsibilities %}")
p2 = respons_cell.add_paragraph("{{ line }}")
if orig_style is not None:
    p2.style = orig_style
p3 = respons_cell.add_paragraph("{%p endfor %}")
if orig_style is not None:
    p3.style = orig_style
# Wrap the data row with {%tr for / endfor %} directive rows
wrap_row_with_tr_loop(data_row, "{%tr for r in roles %}")


# --- Steps (header: Step | Description) ---
steps_table = find_table_by_first_row(
    lambda h: tuple(h) == ("Step", "Description"))
assert steps_table is not None
for row in list(steps_table.rows)[2:]:
    delete_row(row)
data_row = steps_table.rows[1]
cells = data_row.cells
set_paragraph_text(cells[0].paragraphs[0], "{{ s.step }}")
set_paragraph_text(cells[1].paragraphs[0], "{{ s.description }}")
wrap_row_with_tr_loop(data_row, "{%tr for s in steps %}")


# --- Notes/Caution/Warning table (3 rows, leave AS-IS — pure boilerplate) ---


# --- Definitions / Terms (header: Term | Definition) ---
terms_table = find_table_by_first_row(
    lambda h: tuple(h) == ("Term", "Definition"))
assert terms_table is not None
for row in list(terms_table.rows)[2:]:
    delete_row(row)
data_row = terms_table.rows[1]
cells = data_row.cells
set_paragraph_text(cells[0].paragraphs[0], "{{ d.term }}")
set_paragraph_text(cells[1].paragraphs[0], "{{ d.definition }}")
wrap_row_with_tr_loop(data_row, "{%tr for d in definitions %}")


# --- Abbreviations (header: Abbreviation/Acronym | Definition) ---
abbr_table = find_table_by_first_row(
    lambda h: tuple(h) == ("Abbreviation/Acronym", "Definition"))
assert abbr_table is not None
for row in list(abbr_table.rows)[2:]:
    delete_row(row)
data_row = abbr_table.rows[1]
cells = data_row.cells
set_paragraph_text(cells[0].paragraphs[0], "{{ a.abbreviation }}")
set_paragraph_text(cells[1].paragraphs[0], "{{ a.definition }}")
wrap_row_with_tr_loop(data_row, "{%tr for a in abbreviations %}")


# --- References (header: Document Number | Document Title) ---
refs_table = find_table_by_first_row(
    lambda h: tuple(h) == ("Document Number", "Document Title"))
assert refs_table is not None
for row in list(refs_table.rows)[2:]:
    delete_row(row)
data_row = refs_table.rows[1]
cells = data_row.cells
set_paragraph_text(cells[0].paragraphs[0], "{{ ref.number }}")
set_paragraph_text(cells[1].paragraphs[0], "{{ ref.title }}")
wrap_row_with_tr_loop(data_row, "{%tr for ref in references %}")


# ---------------------------------------------------------------------------
# 5. Save the python-docx side, then patch header2.xml in the zip
# ---------------------------------------------------------------------------
INTERIM = Path(_tmp) / "interim.docx"
doc.save(str(INTERIM))


# Patch header2.xml: replace static text with Jinja markers.
# The header has these run sequences (from earlier inspection):
#   PARA: ['Date:', ' ', '4/9/2026']
#   PARA: ['Blank Procedure Template']
#   PARA: ['']
#   PARA: ['Rev.: ', 'A']
#   PARA: ['000-NTD-000-xxx-xxx-000xx']
#
# Replace by editing header2.xml as XML.
import xml.etree.ElementTree as ET

def patch_header_xml(zin: zipfile.ZipFile, name: str) -> bytes:
    raw = zin.read(name).decode("utf-8")
    # Use lxml so we get .getparent() on elements.
    from lxml import etree
    W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    root = etree.fromstring(raw.encode("utf-8"))
    for p in root.iter(W + "p"):
        runs = list(p.iter(W + "r"))
        full = "".join(
            "".join((t.text or "") for t in r.iter(W + "t")) for r in runs
        )
        target = None
        if full.strip().startswith("Date:"):
            target = ("Date: ", "{{ header_date }}")
        elif full.strip() == "Blank Procedure Template":
            target = (None, "{{ procedure_title }}")
        elif full.strip().startswith("Rev.:"):
            target = ("Rev.: ", "{{ revision }}")
        elif "000-NTD-000-xxx-xxx-000xx" in full:
            target = (None, "{{ doc_number }}")

        if target is None:
            continue

        prefix, marker = target
        if not runs:
            continue
        first_run = runs[0]
        # Remove all <w:t> children from the first run, then add a single one
        # carrying the marker text (so we don't accidentally split the marker).
        for t in first_run.findall(W + "t"):
            first_run.remove(t)
        t_el = etree.SubElement(first_run, W + "t")
        t_el.text = (prefix or "") + marker
        t_el.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        # Drop subsequent runs (these may live inside the paragraph, or inside
        # a <w:hyperlink>, etc. — find the actual parent each time).
        for r in runs[1:]:
            parent = r.getparent()
            if parent is not None:
                parent.remove(r)
    return etree.tostring(root, xml_declaration=True, encoding="UTF-8",
                          standalone=True)


with zipfile.ZipFile(INTERIM, "r") as zin:
    with zipfile.ZipFile(DST, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "word/header2.xml":
                data = patch_header_xml(zin, item.filename)
            zout.writestr(item, data)

print(f"\nWrote: {DST}  ({DST.stat().st_size} bytes)")
