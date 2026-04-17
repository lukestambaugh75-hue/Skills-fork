#!/usr/bin/env python3
"""Pre-render linter for docxtpl templates.

Catches the failure modes that production document automation actually hits:
  1. Mismatched {{ / }} or {% / %} counts
  2. Smart-quote contamination of markers (Word autocorrect)
  3. Markers split across multiple text runs (Word edit causing run-split)
  4. Required markers from the schema missing from the template
  5. Markers in the template that aren't in the schema (typos)

Exit codes:
  0  template is clean
  2  recoverable issues (caller may choose to fall back to walk-and-replace)
  3  unrecoverable issues (template needs human fix in Word)

Usage:
  python lint_docx_template.py <template.docx> [<schema.json>]

Output: JSON report on stdout.
"""
from __future__ import annotations
import sys, re, json, zipfile
from pathlib import Path

W_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

# Smart-quote / ligature characters Word sometimes inserts inside markers
SMART_QUOTE_CHARS = {
    "\u2018": "'",   # left single
    "\u2019": "'",   # right single
    "\u201C": '"',   # left double
    "\u201D": '"',   # right double
    "\u00AB": '"',   # «
    "\u00BB": '"',   # »
    "\u2013": "-",   # en-dash
    "\u2014": "-",   # em-dash
    "\u00A0": " ",   # non-breaking space
}

JINJA_PATTERN = re.compile(r"(\{\{[^{}]*\}\}|\{%[^{}]*%\})")
SUSPECT_FRAGMENT = re.compile(r"\{\{|\}\}|\{%|%\}")

def collect_xml(template_path: str) -> dict:
    """Return {part_name: xml_string} for document, header*, footer* parts."""
    parts = {}
    with zipfile.ZipFile(template_path) as z:
        for name in z.namelist():
            if name.endswith("document.xml") or \
               re.match(r"word/header\d+\.xml$", name) or \
               re.match(r"word/footer\d+\.xml$", name):
                parts[name] = z.read(name).decode("utf-8", "ignore")
    return parts

def extract_paragraph_runs(xml: str) -> list[list[str]]:
    """Return a list of paragraphs; each paragraph is a list of run-text strings.

    We use a simple regex parser rather than full XML parsing because we want to
    look at the raw text inside <w:t> elements grouped by <w:p>.
    """
    paragraphs: list[list[str]] = []
    for p_match in re.finditer(r"<w:p[ >].*?</w:p>", xml, re.DOTALL):
        p_xml = p_match.group(0)
        runs = []
        for t_match in re.finditer(r"<w:t[^>]*>(.*?)</w:t>", p_xml, re.DOTALL):
            txt = (t_match.group(1)
                   .replace("&amp;", "&")
                   .replace("&lt;", "<")
                   .replace("&gt;", ">")
                   .replace("&quot;", '"')
                   .replace("&apos;", "'"))
            runs.append(txt)
        if runs:
            paragraphs.append(runs)
    return paragraphs

def lint_template(template_path: str, schema_path: str | None = None) -> dict:
    template_path = str(template_path)
    parts = collect_xml(template_path)

    issues: list[dict] = []
    warnings: list[dict] = []
    found_markers: set[str] = set()
    ok = True

    for part_name, xml in parts.items():
        paragraphs = extract_paragraph_runs(xml)

        for p_idx, runs in enumerate(paragraphs):
            full_text = "".join(runs)

            # Find well-formed markers
            for m in JINJA_PATTERN.finditer(full_text):
                marker = m.group(0)
                # Check for smart-quote / ligature contamination INSIDE the marker
                for sc, _ in SMART_QUOTE_CHARS.items():
                    if sc in marker:
                        issues.append({
                            "severity": "error",
                            "kind": "smart_quote_in_marker",
                            "part": part_name,
                            "paragraph_index": p_idx,
                            "marker": marker,
                            "char": repr(sc),
                            "message": (
                                f"Marker {marker!r} contains a smart-quote/ligature "
                                f"character {sc!r}. Word autocorrect likely altered it. "
                                f"Re-type this marker in Word with autocorrect off."
                            ),
                        })
                        ok = False
                # Extract marker name(s) for schema check
                # {{ a.b.c }} -> 'a'; {% for x in xs %} -> 'xs'
                mname = None
                if marker.startswith("{{"):
                    inner = marker[2:-2].strip()
                    # Handle filters/dots: take the root identifier
                    root = re.match(r"([a-zA-Z_][a-zA-Z0-9_]*)", inner)
                    if root: mname = root.group(1)
                elif marker.startswith("{%"):
                    inner = marker[2:-2].strip()
                    # Loop tags: {% for x in xs %}, {% endfor %}, {% if cond %}, etc.
                    # Capture the iterable name for "for ... in NAME"
                    fm = re.search(r"\bfor\s+\w+\s+in\s+([a-zA-Z_][a-zA-Z0-9_]*)", inner)
                    if fm: mname = fm.group(1)
                if mname:
                    found_markers.add(mname)

            # Detect SUSPECT fragments: any { { } } pieces NOT inside a complete marker
            # (potential run-split or broken marker)
            stripped = JINJA_PATTERN.sub("", full_text)
            for sus in SUSPECT_FRAGMENT.finditer(stripped):
                # Could also be content that legitimately contains {{ — flag as warning
                snippet = stripped[max(0, sus.start()-20):sus.end()+20]
                issues.append({
                    "severity": "error",
                    "kind": "broken_or_split_marker",
                    "part": part_name,
                    "paragraph_index": p_idx,
                    "fragment": sus.group(0),
                    "snippet": snippet,
                    "message": (
                        f"Stray Jinja fragment {sus.group(0)!r} in paragraph — "
                        f"likely a marker split across runs by a Word edit, "
                        f"or content that contains literal {{ }} characters. "
                        f"Open in Word, find the marker, retype it as a single edit."
                    ),
                })
                ok = False

            # Run-split detection: if a {{ or {% appears in one run and the
            # closing }} or %} appears in a LATER run within the same paragraph,
            # that's a confirmed run-split — docxtpl WILL fail to render it.
            # Escalate to error so the render pipeline auto-falls-back to walk-and-replace.
            if len(runs) > 1:
                for ri, r in enumerate(runs):
                    open_in_r = "{{" in r and "}}" not in r
                    pct_open_in_r = "{%" in r and "%}" not in r
                    if open_in_r or pct_open_in_r:
                        rest = "".join(runs[ri+1:])
                        close_token = "}}" if open_in_r else "%}"
                        if close_token in rest:
                            issues.append({
                                "severity": "error",
                                "kind": "run_split_marker",
                                "part": part_name,
                                "paragraph_index": p_idx,
                                "snippet": "".join(runs)[:120],
                                "message": (
                                    f"Marker is split across runs (opening token in "
                                    f"run {ri}, closing token {close_token!r} in a later "
                                    f"run of the same paragraph). docxtpl WILL fail to "
                                    f"render this. Open in Word, delete the marker, "
                                    f"retype it in one motion, save. (The render pipeline "
                                    f"will automatically fall back to walk-and-replace "
                                    f"until this is fixed.)"
                                ),
                            })
                            ok = False

    # Top-level marker integrity: balanced braces across the whole template
    all_xml = "\n".join(parts.values())
    open_double = all_xml.count("{{")
    close_double = all_xml.count("}}")
    open_pct = all_xml.count("{%")
    close_pct = all_xml.count("%}")
    if open_double != close_double:
        issues.append({
            "severity": "error",
            "kind": "unbalanced_braces",
            "message": f"Unbalanced {{{{/}}}}: {open_double} opens, {close_double} closes.",
        })
        ok = False
    if open_pct != close_pct:
        issues.append({
            "severity": "error",
            "kind": "unbalanced_braces",
            "message": f"Unbalanced {{%/%}}: {open_pct} opens, {close_pct} closes.",
        })
        ok = False

    # Schema check
    schema_issues = []
    if schema_path and Path(schema_path).exists():
        schema = json.loads(Path(schema_path).read_text())
        required = set(schema.get("required_markers", []))
        optional = set(schema.get("optional_markers", []))
        known = required | optional

        missing_required = required - found_markers
        unknown_in_template = found_markers - known

        for m in sorted(missing_required):
            schema_issues.append({
                "severity": "error",
                "kind": "required_marker_missing",
                "marker": m,
                "message": f"Required marker {{{{ {m} }}}} not found in template.",
            })
            ok = False
        for m in sorted(unknown_in_template):
            schema_issues.append({
                "severity": "warning",
                "kind": "unknown_marker_in_template",
                "marker": m,
                "message": (
                    f"Marker {{{{ {m} }}}} is in the template but not in the schema. "
                    f"Either add it to the schema or remove from the template."
                ),
            })

    report = {
        "template": template_path,
        "schema": schema_path,
        "ok": ok,
        "found_markers": sorted(found_markers),
        "issues": issues + schema_issues,
        "warnings": warnings,
    }
    return report

def main():
    if len(sys.argv) < 2:
        print("Usage: lint_docx_template.py <template.docx> [<schema.json>]",
              file=sys.stderr)
        sys.exit(64)
    template = sys.argv[1]
    schema = sys.argv[2] if len(sys.argv) >= 3 else None
    report = lint_template(template, schema)
    print(json.dumps(report, indent=2))

    if not report["ok"]:
        # Distinguish recoverable (warnings only) vs. unrecoverable (errors)
        has_errors = any(i.get("severity") == "error" for i in report["issues"])
        sys.exit(3 if has_errors else 2)
    sys.exit(0)

if __name__ == "__main__":
    main()
