#!/usr/bin/env python3
"""Render NextDecade PowerPoint decks from JSON + the master .potx.

Unlike docx, there isn't a mature Jinja-style templater for pptx, so this uses
the clone-and-fill pattern:

  1. Binary-clone the master template (preserves brand theme, 50 layouts,
     embedded logos/photos, forward-looking statements slide).
  2. Convert .potx → .pptx content-type in-place.
  3. Drop the template's two pre-populated slides.
  4. For each slide in the input JSON, add a slide using the requested layout
     and fill the placeholders.
  5. Optionally export to PDF via LibreOffice.

Supported layouts by brand family (from the color-corrected Oct 2025 master):
  ND (NextDecade Corporate): ND Blank, ND Single Narrative 18 Font,
    ND Duel Narrative, ND Tri Right Narrative, ND Tri Left Narrative,
    ND Quad Narrative
  RG (Rio Grande LNG): RG Blank, RG Single Narrative 18 Font, RG Dual Narrative,
    RG Tri Left Narrative, RG Tri Right Narrative, RG Quad Narrative
  NCS (NEXT Carbon Solutions): NCS Blank, NCS Single Narrative 18 Font,
    NCS Dual Narrative, NCS Tri Right Narrative, NCS Tri Left Narrative,
    NCS Quad Narrative
  Shared: Custom Layout (cover), 1_Custom Layout (cover variant),
    23_Custom Layout (back cover with URL), Public Disclaimer (FLS legal page)

CLI:
  python render_pptx.py <input.json> <output.pptx> [--pdf]

Input JSON shape:
  {
    "brand": "NextDecade" | "RioGrandeLNG" | "NCS",   # REQUIRED — brand-family gate
    "title": "deck title",
    "slides": [
      {"layout": "Custom Layout", "title": "Hot Work Permits", "subtitle": "..."},
      {"layout": "Public Disclaimer"},
      {"layout": "ND Single Narrative 18 Font", "title": "...", "bullets": [...]},
      {"layout": "ND Dual Narrative", "title": "...", "left_bullets": [...], "right_bullets": [...]},
      {"layout": "23_Custom Layout"}
    ]
  }

"brand" determines the allowed layout prefix for non-shared slides:
  "NextDecade"   -> layouts starting with "ND "
  "RioGrandeLNG" -> layouts starting with "RG "
  "NCS"          -> layouts starting with "NCS "
Shared layouts allowed for every brand: "Custom Layout", "1_Custom Layout",
"Public Disclaimer", "23_Custom Layout". Any other layout that does not match
the declared brand prefix raises ValueError before rendering.
"""
from __future__ import annotations
import sys, json, shutil, zipfile, subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
_REPO_ROOT = HERE.parents[2]
MASTER = (
    _REPO_ROOT / "NextDecade-Claude-Project" / "02-templates"
    / "NextDecade PowerPoint Master (Oct 2025, brand-corrected).potx"
)

# Brand-family gate. The PPTX master carries parallel ND / RG / NCS layout
# families. Single-brand decks commit to one family; corporate decks
# (investor updates, board decks, town halls) may span all three.
SHARED_LAYOUTS = {
    "Custom Layout",
    "1_Custom Layout",
    "Public Disclaimer",
    "23_Custom Layout",
}
BRAND_PREFIXES = {
    "NextDecade": ("ND",),
    "RioGrandeLNG": ("RG",),
    "NCS": ("NCS",),
    "Corporate": ("ND", "RG", "NCS"),  # multi-brand: investor/board/town-hall
}


def _validate_brand_and_layouts(data: dict) -> tuple[str, ...]:
    """Enforce the brand-family gate.

    Requires data["brand"] to be one of BRAND_PREFIXES and every slide layout
    to be either a shared cover/disclaimer/back-cover layout or to start with
    one of the declared brand's allowed prefixes + " ".

    Returns the tuple of allowed prefixes on success; raises ValueError on
    any violation so the pipeline fails loudly.
    """
    brand = data.get("brand")
    if brand not in BRAND_PREFIXES:
        raise ValueError(
            f"Input JSON must declare 'brand' as one of {sorted(BRAND_PREFIXES)}; "
            f"got {brand!r}. Ask the user which NextDecade brand the deck is for "
            f"(NextDecade Corporate / Rio Grande LNG / NEXT Carbon Solutions / "
            f"Corporate for multi-brand decks) before rendering."
        )
    prefixes = BRAND_PREFIXES[brand]
    for si, slide in enumerate(data.get("slides", []), start=1):
        layout = slide.get("layout", "")
        if layout in SHARED_LAYOUTS:
            continue
        if not any(layout.startswith(p + " ") for p in prefixes):
            raise ValueError(
                f"Slide {si}: layout {layout!r} does not match declared brand "
                f"{brand!r} (expected a layout prefixed with one of {prefixes!r} "
                f"or a shared layout: {sorted(SHARED_LAYOUTS)})."
            )
    return prefixes


def _potx_to_pptx_inplace(path: Path):
    """Rewrite [Content_Types].xml so LibreOffice/PowerPoint treat the file as a pptx."""
    with zipfile.ZipFile(path) as z:
        files = {n: z.read(n) for n in z.namelist()}
        infos = {n: z.getinfo(n) for n in z.namelist()}
    ct = files["[Content_Types].xml"].decode("utf-8")
    if "presentationml.template.main+xml" in ct:
        ct = ct.replace("presentationml.template.main+xml",
                        "presentationml.presentation.main+xml")
        files["[Content_Types].xml"] = ct.encode("utf-8")
        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
            for n, b in files.items():
                z.writestr(infos[n], b)


def _drop_existing_slides(prs):
    from pptx.oxml.ns import qn
    sldIdLst = prs.slides._sldIdLst
    for el in list(sldIdLst):
        rId = el.get(qn("r:id"))
        sldIdLst.remove(el)
        try:
            prs.part.drop_rel(rId)
        except Exception:
            pass


def _fill_placeholders(slide, layout_name: str, data: dict):
    """Fill title, subtitle, and body placeholders based on layout semantics."""
    placeholders_by_idx = {sh.placeholder_format.idx: sh for sh in slide.placeholders}

    # Title (idx 0) — "Custom Layout" cover, content layouts, etc.
    if "title" in data and 0 in placeholders_by_idx:
        placeholders_by_idx[0].text_frame.text = data["title"]

    # Subtitle / date (idx 10 on "Custom Layout") — "Click to edit date" placeholder
    if "subtitle" in data:
        for idx in (10, 11):
            if idx in placeholders_by_idx:
                placeholders_by_idx[idx].text_frame.text = data["subtitle"]
                break

    # Single-narrative bullets (idx 10 on ND/RG/NCS Single Narrative)
    if "bullets" in data:
        # Find the body placeholder — typically idx 10 on Single/Quad layouts
        for idx in (10, 12, 13):
            if idx in placeholders_by_idx:
                tf = placeholders_by_idx[idx].text_frame
                tf.clear()
                for i, b in enumerate(data["bullets"]):
                    p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
                    p.text = b
                    p.level = 0
                break

    # Dual-narrative: left_bullets + right_bullets → ph 12 & 13
    if "left_bullets" in data and 12 in placeholders_by_idx:
        tf = placeholders_by_idx[12].text_frame
        tf.clear()
        for i, b in enumerate(data["left_bullets"]):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.text = b
    if "right_bullets" in data and 13 in placeholders_by_idx:
        tf = placeholders_by_idx[13].text_frame
        tf.clear()
        for i, b in enumerate(data["right_bullets"]):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.text = b


def render(data: dict, output: str | Path, pdf: bool = False) -> dict:
    from pptx import Presentation
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)

    # Step 0: brand-family gate. Fail fast if the caller didn't ask the user
    # which brand the deck is for, or picked layouts from the wrong family.
    _validate_brand_and_layouts(data)

    # Step 1: clone and convert
    shutil.copy2(MASTER, output)
    _potx_to_pptx_inplace(output)

    # Step 2: open and clear
    prs = Presentation(str(output))
    _drop_existing_slides(prs)

    # Step 3: index layouts
    layouts_by_name = {}
    for master in prs.slide_masters:
        for layout in master.slide_layouts:
            layouts_by_name[layout.name] = layout

    # Step 4: build slides
    report = {"output": str(output), "slides": [], "warnings": []}
    for si, slide_spec in enumerate(data.get("slides", [])):
        layout_name = slide_spec.get("layout", "ND Blank")
        layout = layouts_by_name.get(layout_name)
        if layout is None:
            report["warnings"].append(
                f"Slide {si+1}: layout {layout_name!r} not found; using 'ND Blank'"
            )
            layout = layouts_by_name.get("ND Blank") or list(layouts_by_name.values())[0]
        slide = prs.slides.add_slide(layout)
        _fill_placeholders(slide, layout_name, slide_spec)
        report["slides"].append({"layout": layout_name,
                                 "title": slide_spec.get("title", "")})

    prs.save(str(output))

    # Step 5: optional PDF
    if pdf:
        try:
            pdf_path = _convert_to_pdf(output)
            report["pdf"] = str(pdf_path)
        except Exception as e:
            report["warnings"].append(f"PDF export failed: {e}")
    return report


def _convert_to_pdf(pptx_path: Path) -> Path:
    """Convert .pptx to .pdf via headless LibreOffice."""
    import tempfile
    pdf_path = pptx_path.with_suffix(".pdf")
    out_dir = pptx_path.parent
    with tempfile.TemporaryDirectory() as tmpdir:
        profile_arg = f"-env:UserInstallation=file://{tmpdir}/lo_profile"
        cmd = ["soffice", "--headless", profile_arg, "--convert-to", "pdf",
               "--outdir", str(out_dir), str(pptx_path)]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        if result.returncode != 0:
            raise RuntimeError(
                f"LibreOffice conversion failed (exit {result.returncode}): "
                f"{result.stderr}"
            )
    actual = out_dir / (pptx_path.stem + ".pdf")
    if not actual.exists():
        raise RuntimeError(f"PDF not produced at {actual}")
    return actual


def main():
    if len(sys.argv) < 3:
        print("Usage: render_pptx.py <input.json> <output.pptx> [--pdf]",
              file=sys.stderr)
        sys.exit(64)
    data = json.loads(Path(sys.argv[1]).read_text())
    output = sys.argv[2]
    pdf = "--pdf" in sys.argv
    report = render(data, output, pdf=pdf)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
