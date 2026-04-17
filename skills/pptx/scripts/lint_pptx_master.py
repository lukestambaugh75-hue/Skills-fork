#!/usr/bin/env python3
"""Linter for the NextDecade PowerPoint master .potx.

Checks:
  1. All expected brand layouts are present (ND/RG/NCS × 6 content families,
     plus Custom Layout cover, Public Disclaimer, 23_Custom Layout back cover).
  2. Theme1 has the correct Segoe UI font and brand navy #002060.
  3. Brand orange #FC7134 is in accent2 (not the Office default #ED7D31).
  4. Public Disclaimer layout still contains the required legal boilerplate
     phrases (so a human edit hasn't accidentally gutted the FLS).

Exit 0 = clean. Exit 3 = errors. Exit 2 = warnings only.

Usage:
  python lint_pptx_master.py [<master.potx>]
"""
from __future__ import annotations
import sys, json, zipfile, re
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_MASTER = (
    _REPO_ROOT / "NextDecade-Claude-Project" / "02-templates"
    / "NextDecade PowerPoint Master (Oct 2025, brand-corrected).potx"
)

REQUIRED_LAYOUTS = [
    "Custom Layout",               # cover
    "Public Disclaimer",           # forward-looking statements
    "23_Custom Layout",            # back cover with URL
    "ND Blank", "ND Single Narrative 18 Font", "ND Duel Narrative",
    "ND Tri Right Narrative", "ND Tri Left Narrative", "ND Quad Narrative",
    "RG Blank", "RG Single Narrative 18 Font", "RG Dual Narrative",
    "RG Tri Left Narrative", "RG Tri Right Narrative", "RG Quad Narrative",
    "NCS Blank", "NCS Single Narrative 18 Font", "NCS Dual Narrative",
    "NCS Tri Right Narrative", "NCS Tri Left Narrative", "NCS Quad Narrative",
]

REQUIRED_FLS_PHRASES = [
    "forward-looking statements",
    "Section 27A of the Securities Act of 1933",
    "Section 21E of the Securities Exchange Act of 1934",
    "anticipate",
    "does not undertake any obligation",
    "NASDAQ: NEXT",
]

def lint(master_path: Path) -> dict:
    issues, warnings, found_layouts = [], [], []
    ok = True

    with zipfile.ZipFile(master_path) as z:
        # ---- layouts ----
        for n in z.namelist():
            m = re.match(r"ppt/slideLayouts/slideLayout\d+\.xml$", n)
            if m:
                xml = z.read(n).decode("utf-8", "ignore")
                name_m = re.search(r'<p:cSld name="([^"]+)"', xml)
                if name_m:
                    found_layouts.append(name_m.group(1))

        for req in REQUIRED_LAYOUTS:
            if req not in found_layouts:
                issues.append({
                    "severity": "error",
                    "kind": "missing_layout",
                    "layout": req,
                    "message": f"Required layout {req!r} missing from master.",
                })
                ok = False

        # ---- theme colors + font ----
        theme1 = z.read("ppt/theme/theme1.xml").decode("utf-8", "ignore")
        # accent1 should be navy 002060
        m = re.search(r'<a:accent1>\s*<a:srgbClr val="([0-9A-Fa-f]{6})"', theme1)
        if m and m.group(1).upper() != "002060":
            issues.append({
                "severity": "error",
                "kind": "wrong_accent1",
                "value": f"#{m.group(1).upper()}",
                "expected": "#002060",
                "message": f"accent1 should be brand navy #002060; found #{m.group(1).upper()}",
            })
            ok = False

        # accent2 should be brand orange FC7134 (corrected from Office default ED7D31)
        m = re.search(r'<a:accent2>\s*<a:srgbClr val="([0-9A-Fa-f]{6})"', theme1)
        if m:
            val = m.group(1).upper()
            if val == "ED7D31":
                issues.append({
                    "severity": "error",
                    "kind": "office_default_orange",
                    "message": "accent2 is Office default #ED7D31; should be brand #FC7134",
                })
                ok = False
            elif val != "FC7134":
                warnings.append({
                    "severity": "warning",
                    "kind": "unexpected_accent2",
                    "value": f"#{val}",
                    "message": f"accent2 is #{val}; expected brand orange #FC7134",
                })

        # Font should be Segoe UI
        font_m = re.search(r'<a:majorFont>\s*<a:latin typeface="([^"]+)"', theme1)
        if font_m and font_m.group(1) != "Segoe UI":
            warnings.append({
                "severity": "warning",
                "kind": "unexpected_major_font",
                "value": font_m.group(1),
                "message": f"Major font is {font_m.group(1)!r}; expected 'Segoe UI'",
            })

        # ---- FLS legal text presence ----
        fls_layout_xml = None
        for n in z.namelist():
            if not re.match(r"ppt/slideLayouts/slideLayout\d+\.xml$", n):
                continue
            xml = z.read(n).decode("utf-8", "ignore")
            if '<p:cSld name="Public Disclaimer"' in xml:
                fls_layout_xml = xml
                break
        if fls_layout_xml:
            fls_text = re.sub(r"<[^>]+>", " ", fls_layout_xml)
            fls_text = re.sub(r"\s+", " ", fls_text)
            for phrase in REQUIRED_FLS_PHRASES:
                if phrase.lower() not in fls_text.lower():
                    issues.append({
                        "severity": "error",
                        "kind": "fls_phrase_missing",
                        "phrase": phrase,
                        "message": (
                            f"Public Disclaimer layout is missing required FLS "
                            f"phrase: {phrase!r}. Do not ship this master until "
                            f"Legal restores the language."
                        ),
                    })
                    ok = False
        else:
            issues.append({
                "severity": "error",
                "kind": "fls_layout_missing",
                "message": "Public Disclaimer layout not found.",
            })
            ok = False

    return {
        "master": str(master_path),
        "ok": ok,
        "found_layouts": found_layouts,
        "issues": issues,
        "warnings": warnings,
    }


def main():
    master = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_MASTER
    report = lint(master)
    print(json.dumps(report, indent=2))
    if not report["ok"]:
        sys.exit(3 if any(i["severity"] == "error" for i in report["issues"]) else 2)
    sys.exit(0)


if __name__ == "__main__":
    main()
