#!/usr/bin/env python3
"""docxtpl render pipeline for NextDecade governance documents.

Supports: procedure, standard, guidance. Each has a Jinja-tagged template and
a JSON schema under ../templates/. Pipeline:
  1. Lint the Jinja template (scripts/lint_docx_template.py).
  2. Render with docxtpl + StrictUndefined (raises on any missing key).
  3. Optional: convert the rendered .docx to .pdf via LibreOffice.

CLI:
  python render_docx.py <doc_type> <input.json> <output.docx> [--pdf]
    doc_type: procedure | standard | guidance

Module:
  from render_docx import render
  report = render("procedure", data_dict, "/path/to/output.docx", pdf=True)
"""
from __future__ import annotations
import sys, json, subprocess, shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
# NOTE: TEMPLATES path constant below differs between the two render_docx.py
# copies (skills/docx/scripts/ vs NextDecade-Claude-Project/04-scripts/)
# because each copy resolves templates relative to its own directory. The
# smoke test strips path-constant lines before diffing so only functional
# drift is reported.
TEMPLATES = HERE.parent / "02-templates"
LINTER = HERE / "lint_docx_template.py"

DOC_TYPES = {
    "procedure": {
        "jinja_template": TEMPLATES / "Procedure Template (Jinja).docx",
        "schema": TEMPLATES / "procedure_schema.json",
    },
    "standard": {
        "jinja_template": TEMPLATES / "Standard Template (Jinja).docx",
        "schema": TEMPLATES / "standard_schema.json",
    },
    "guidance": {
        "jinja_template": TEMPLATES / "Guidance Template (Jinja).docx",
        "schema": TEMPLATES / "guidance_schema.json",
    },
}


def _strict_env():
    from jinja2 import Environment, StrictUndefined
    return Environment(undefined=StrictUndefined, autoescape=False)


def _xml_escape_data(obj):
    """Recursively escape XML-special characters (&, <, >) in string values.

    docxtpl injects rendered text directly into Word XML. If the data contains
    raw '&', '<', or '>' the XML parser fails with 'xmlParseEntityRef'. This
    pre-escaping makes the docxtpl path safe for arbitrary user content
    including ampersands, angle brackets, and em-dashes.
    """
    from xml.sax.saxutils import escape
    if isinstance(obj, str):
        return escape(obj)
    if isinstance(obj, dict):
        return {k: _xml_escape_data(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_xml_escape_data(v) for v in obj]
    return obj


def render_via_docxtpl(data: dict, template: Path, output: Path) -> None:
    from docxtpl import DocxTemplate
    tpl = DocxTemplate(str(template))
    tpl.render(_xml_escape_data(data), jinja_env=_strict_env())
    tpl.save(str(output))


def _post_render_cover_fixup(output: Path, data: dict, doc_type: str) -> list[str]:
    """Patch cover-page text boxes and headers in the rendered .docx.

    The Standard and Guidance Jinja templates have plain-text placeholders
    ("NAME", "xxx-xxx-xxx-xxx-xxx-#####") inside text boxes and headers that
    docxtpl cannot reach because they're not Jinja markers. This function
    does a targeted XML search-and-replace inside the .docx zip.

    Returns a list of patches applied (for logging).
    """
    import zipfile

    doc_name = data.get("document_name", "")
    doc_num = data.get("doc_number", "")
    if not doc_name and not doc_num:
        return []

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


def _remove_template_scaffolding(output: Path, doc_type: str) -> None:
    """Remove known template scaffolding from the rendered .docx.

    Procedure: removes "Use the following for notes, cautions, and warnings."
    paragraph and the Note/Caution/Warning demo table that follows.
    Standard/Guidance: removes placeholder boilerplate paragraphs
    (e.g., "[CONTENT TITLE]", "Enter text here") if any survive rendering.
    """
    from docx import Document

    doc = Document(str(output))
    changed = False

    if doc_type == "procedure":
        for p in list(doc.paragraphs):
            if "Use the following for notes, cautions, and warnings" in p.text:
                p._element.getparent().remove(p._element)
                changed = True

        for t in list(doc.tables):
            cell_texts = []
            for row in t.rows:
                for cell in row.cells:
                    cell_texts.append(cell.text.strip())
            all_text = " ".join(cell_texts)
            if ("Note:" in all_text and "Caution:" in all_text
                    and "Warning:" in all_text
                    and "alerts users" in all_text):
                t._element.getparent().remove(t._element)
                changed = True

    elif doc_type in ("standard", "guidance"):
        scaffolding_markers = [
            "[CONTENT TITLE]",
            "Enter text here",
            "Click here to enter text",
        ]
        for p in list(doc.paragraphs):
            for marker in scaffolding_markers:
                if marker in p.text:
                    p._element.getparent().remove(p._element)
                    changed = True
                    break

    if changed:
        doc.save(str(output))


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
def render(doc_type: str, data: dict, output: str | Path, pdf: bool = False) -> dict:
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

    if lint_exit not in (0, 2):
        raise RuntimeError(
            f"Template lint failed with exit {lint_exit}. "
            f"Fix the Jinja template before rendering. "
            f"Issues: {lint_report.get('issues')}"
        )

    # Step 2: render strict
    render_via_docxtpl(data, cfg["jinja_template"], output)
    report["path"] = "docxtpl"
    if lint_exit == 2:
        report["warnings"] = [w["message"] for w in lint_report.get("warnings", [])]

    # Step 2.5a: post-render cover-page fixup (Standard/Guidance text boxes + headers)
    cover_patches = _post_render_cover_fixup(output, data, doc_type)
    if cover_patches:
        report["cover_patches"] = cover_patches

    # Step 2.5b: remove template scaffolding (applies to all doc types)
    _remove_template_scaffolding(output, doc_type)

    # Step 3: optional PDF
    if pdf:
        pdf_path = convert_to_pdf(output)
        report["pdf"] = str(pdf_path)

    return report


def main():
    if len(sys.argv) < 4:
        print("Usage: render_docx.py <doc_type> <input.json> <output.docx> [--pdf]",
              file=sys.stderr)
        print(f"  doc_type one of: {sorted(DOC_TYPES)}", file=sys.stderr)
        sys.exit(64)
    doc_type = sys.argv[1]
    data = json.loads(Path(sys.argv[2]).read_text())
    output = sys.argv[3]
    pdf = "--pdf" in sys.argv
    report = render(doc_type, data, output, pdf=pdf)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
