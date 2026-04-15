#!/usr/bin/env python3
"""docxtpl render pipeline with pre-render lint and walk-and-replace fallback.

Pipeline:
  1. Lint the template (lint_docx_template.py).
  2. If lint passes (exit 0):  render with docxtpl + StrictUndefined.
  3. If lint reports recoverable issues only (exit 2): render with docxtpl,
     warn caller.
  4. If lint reports errors (exit 3): fall back to walk-and-replace using
     the original (pre-Jinja) template and a content-mapping function.

Usage as module:
  from render_docx import render_procedure
  render_procedure(input_dict, "/path/to/output.docx")

Usage as CLI:
  python render_docx.py <input.json> <output.docx> [--no-fallback]
"""
from __future__ import annotations
import sys, json, subprocess, shutil
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
TEMPLATES = HERE.parent / "templates"
LINTER = HERE / "lint_docx_template.py"

# Original (un-Jinja'd) template for the walk-and-replace fallback path
ORIGINAL_TEMPLATE = Path(
    "/home/user/Skills-fork/uploads/04-document-templates/Procedure Template.docx"
)
JINJA_TEMPLATE = TEMPLATES / "Procedure Template (Jinja).docx"
SCHEMA = TEMPLATES / "procedure_schema.json"


# ---------------------------------------------------------------------------
# Primary path: docxtpl render
# ---------------------------------------------------------------------------
def render_via_docxtpl(data: dict, template: Path, output: Path) -> None:
    from docxtpl import DocxTemplate
    from jinja2 import StrictUndefined
    tpl = DocxTemplate(str(template))
    tpl.render(data, jinja_env=_strict_env())
    tpl.save(str(output))

def _strict_env():
    from jinja2 import Environment, StrictUndefined
    return Environment(undefined=StrictUndefined, autoescape=False)


# ---------------------------------------------------------------------------
# Fallback path: walk-and-replace on the ORIGINAL template
# ---------------------------------------------------------------------------
def render_via_walk_and_replace(data: dict, output: Path) -> None:
    """Walk-and-replace on the original (pre-Jinja) Procedure Template.

    This path is the safety net: if the Jinja template gets corrupted by a
    Word edit, we still produce a brand-correct procedure from the original.
    """
    from docx import Document
    from copy import deepcopy
    from docx.text.paragraph import Paragraph

    shutil.copy2(ORIGINAL_TEMPLATE, output)
    doc = Document(str(output))

    def _set_text(p, text):
        runs = p.runs
        if not runs:
            p.add_run(text); return
        runs[0].text = text
        for r in runs[1:]:
            r._element.getparent().remove(r._element)

    def _h1(token):
        for i, p in enumerate(doc.paragraphs):
            if p.style and p.style.name == "Heading 1" and \
               token.lower() in p.text.strip().lower():
                return i
        return None

    def _fill_after(idx, text):
        if idx is None: return
        for k in range(idx + 1, len(doc.paragraphs)):
            p = doc.paragraphs[k]
            if p.style and p.style.name == "Heading 1": return
            if p.text.strip():
                _set_text(p, text); return

    _fill_after(_h1("PURPOSE"),                  data["purpose_text"])
    _fill_after(_h1("SCOPE"),                    data["scope_text"])
    _fill_after(_h1("INTEGRATED GOVERNANCE"),    data["governance_text"])
    _fill_after(_h1("EXCEPTION REQUEST"),        data["exception_text"])
    _fill_after(_h1("CONTINUOUS IMPROVEMENT"),   data["continuous_text"])

    # Content sections
    sections = data["content_sections"]
    slots = [i for i, p in enumerate(doc.paragraphs)
             if p.style and p.style.name == "Heading 1" and "[CONTENT TITLE]" in p.text]

    def _fill_content_section(heading_idx, section):
        h = doc.paragraphs[heading_idx]
        _set_text(h, section["title"])
        intro_set = False
        bullet_paragraphs = []
        for k in range(heading_idx + 1, len(doc.paragraphs)):
            p = doc.paragraphs[k]
            if p.style and p.style.name == "Heading 1": break
            if not p.text.strip(): continue
            if not intro_set:
                _set_text(p, section["intro"]); intro_set = True
            else:
                bullet_paragraphs.append(p)
        bullets = section["bullets"]
        if len(bullets) <= len(bullet_paragraphs):
            for i, b in enumerate(bullets):
                _set_text(bullet_paragraphs[i], b)
            for extra in bullet_paragraphs[len(bullets):]:
                extra._element.getparent().remove(extra._element)
        else:
            for i, p in enumerate(bullet_paragraphs):
                _set_text(p, bullets[i])
            last = bullet_paragraphs[-1]
            for b in bullets[len(bullet_paragraphs):]:
                new_el = deepcopy(last._element)
                last._element.addnext(new_el)
                last = Paragraph(new_el, last._parent)
                _set_text(last, b)

    n_slots = len(slots)
    n_sections = len(sections)
    if n_sections <= n_slots:
        for i in range(n_sections):
            slot_idx = [j for j, p in enumerate(doc.paragraphs)
                        if p.style and p.style.name == "Heading 1"
                        and "[CONTENT TITLE]" in p.text][0]
            _fill_content_section(slot_idx, sections[i])
        # Remove unused slots
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
        # Fill all slots, then clone-from-last for remaining sections
        for i in range(n_slots):
            slot_idx = [j for j, p in enumerate(doc.paragraphs)
                        if p.style and p.style.name == "Heading 1"
                        and "[CONTENT TITLE]" in p.text][0]
            _fill_content_section(slot_idx, sections[i])
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
            _fill_content_section(new_h_idx, sec)

    # Tables
    for t in doc.tables:
        headers = [c.text.strip() for c in t.rows[0].cells]
        if headers[:3] == ["No.", "Term", "Definition"]:
            data_rows = list(t.rows)[1:]
            for i, d in enumerate(data["definitions"]):
                if i < len(data_rows):
                    r = data_rows[i]
                    _set_text(r.cells[0].paragraphs[0], d["no"])
                    _set_text(r.cells[1].paragraphs[0], d["term"])
                    _set_text(r.cells[2].paragraphs[0], d["definition"])
                else:
                    new_row = t.add_row()
                    new_row.cells[0].text = d["no"]
                    new_row.cells[1].text = d["term"]
                    new_row.cells[2].text = d["definition"]
            for r in data_rows[len(data["definitions"]):]:
                r._element.getparent().remove(r._element)
        elif headers[:2] == ["Title", "Document Number"]:
            data_rows = list(t.rows)[1:]
            for i, ref in enumerate(data["references"]):
                if i < len(data_rows):
                    r = data_rows[i]
                    _set_text(r.cells[0].paragraphs[0], ref["title"])
                    _set_text(r.cells[1].paragraphs[0], ref["number"])
                else:
                    new_row = t.add_row()
                    new_row.cells[0].text = ref["title"]
                    new_row.cells[1].text = ref["number"]
            for r in data_rows[len(data["references"]):]:
                r._element.getparent().remove(r._element)
        elif headers[:4] == ["Responsible", "Accountable", "Consulted", "Informed"]:
            if len(t.rows) > 1:
                r = t.rows[1]
                raci = data["raci"]
                _set_text(r.cells[0].paragraphs[0], raci["responsible"])
                _set_text(r.cells[1].paragraphs[0], raci["accountable"])
                _set_text(r.cells[2].paragraphs[0], raci["consulted"])
                _set_text(r.cells[3].paragraphs[0], raci["informed"])
        elif headers[:3] == ["Issuer / Title", "Adopted By", "Effective / Amended Date"]:
            if len(t.rows) > 1:
                r = t.rows[1]
                ap = data["approval"]
                _set_text(r.cells[0].paragraphs[0], ap["issuer"])
                _set_text(r.cells[1].paragraphs[0], ap["adopted_by"])
                _set_text(r.cells[2].paragraphs[0], ap["effective_date"])
        elif headers[:2] == ["Revision", "Description of Changes and Notes"]:
            data_rows = list(t.rows)[1:]
            for i, rev in enumerate(data["revision_history"]):
                if i < len(data_rows):
                    r = data_rows[i]
                    _set_text(r.cells[0].paragraphs[0], rev["number"])
                    _set_text(r.cells[1].paragraphs[0], rev["description"])
                else:
                    new_row = t.add_row()
                    new_row.cells[0].text = rev["number"]
                    new_row.cells[1].text = rev["description"]
            for r in data_rows[len(data["revision_history"]):]:
                r._element.getparent().remove(r._element)

    doc.save(str(output))


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------
def render_procedure(data: dict, output: str | Path,
                     allow_fallback: bool = True) -> dict:
    """Render a NextDecade Procedure document.

    Returns a small report describing which path was taken and any warnings.
    """
    output = Path(output)
    report = {"output": str(output), "path": None, "warnings": []}

    # Step 1: lint
    proc = subprocess.run(
        [sys.executable, str(LINTER), str(JINJA_TEMPLATE), str(SCHEMA)],
        capture_output=True, text=True,
    )
    lint_report = json.loads(proc.stdout) if proc.stdout else {}
    lint_exit = proc.returncode
    report["lint"] = {
        "exit": lint_exit,
        "issue_count": len(lint_report.get("issues", [])),
        "warning_count": len(lint_report.get("warnings", [])),
    }

    # Step 2: choose path
    if lint_exit == 0:
        render_via_docxtpl(data, JINJA_TEMPLATE, output)
        report["path"] = "docxtpl"
    elif lint_exit == 2:
        # Recoverable: try docxtpl, surface warnings
        try:
            render_via_docxtpl(data, JINJA_TEMPLATE, output)
            report["path"] = "docxtpl"
            report["warnings"] = [w["message"] for w in lint_report.get("warnings", [])]
        except Exception as e:
            if allow_fallback:
                render_via_walk_and_replace(data, output)
                report["path"] = "walk_and_replace_fallback"
                report["warnings"].append(f"docxtpl raised: {e}; used fallback")
            else:
                raise
    else:
        # Unrecoverable Jinja template issues — go straight to fallback
        if allow_fallback:
            render_via_walk_and_replace(data, output)
            report["path"] = "walk_and_replace_fallback"
            report["warnings"].append(
                "Jinja template has unrecoverable issues; rendered via "
                "walk-and-replace on the original template. "
                "Fix the Jinja template to restore the fast path."
            )
            report["lint_issues"] = lint_report.get("issues", [])
        else:
            raise RuntimeError(
                f"Template lint failed with exit {lint_exit}; "
                f"fallback disabled. Issues: {lint_report.get('issues')}"
            )
    return report


def main():
    if len(sys.argv) < 3:
        print("Usage: render_docx.py <input.json> <output.docx> [--no-fallback]",
              file=sys.stderr)
        sys.exit(64)
    data = json.loads(Path(sys.argv[1]).read_text())
    output = sys.argv[2]
    allow_fallback = "--no-fallback" not in sys.argv
    report = render_procedure(data, output, allow_fallback=allow_fallback)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
