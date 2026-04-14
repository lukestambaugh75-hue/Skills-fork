# 03 — Photography, Icons & Imagery

**Priority:** Recommended. Without this, Claude will use placeholder imagery.

## What to upload here

### Photography
- [ ] Approved site photos (Rio Grande LNG Facility, CP2 site, construction)
- [ ] Aerial / drone imagery
- [ ] Executive / leadership headshots (official versions)
- [ ] Employee / workforce photos (cleared for use)
- [ ] Partnership / community photos
- [ ] Stock photography approved for use

### Icons & illustrations
- [ ] Icon library (SVG preferred) — safety, operations, commercial, financial
- [ ] Infographic element templates (process flows, maps)
- [ ] Illustration style samples if a house illustration style exists

### Usage documentation
- [ ] Photography rules (color treatment, cropping, captions)
- [ ] Imagery do/don't examples
- [ ] Prohibited imagery (e.g., "never use stock photos of competitors' facilities")
- [ ] Model release status — which people can appear in external comms

## File types expected

`.jpg`, `.png`, `.svg`, `.ai`, `.eps`, plus `.pdf`/`.docx` with usage rules

## What Claude will extract

- Indexed library of available assets with descriptive names + suggested uses
- Photography treatment rules (grading, cropping, duotone, overlays)
- Icon style specification (stroke width, corner radius, fill vs. outline)
- Captioning format (caption position, font, credit line conventions)
- Which images are approved for: external web / investor / internal / community / media
- Restrictions (e.g., "no aerial shots of CP2 until FERC approval")

## Feeds these skills

- `skills/brand-guidelines/` (imagery section)
- `skills/pptx/` (default image library for decks)
- `skills/docx/` (report cover imagery, inline figures)
- NEW: `skills/data-visualization/` (chart iconography)

## Notes

- Organize into subfolders by category if uploading many: `03-imagery/photos/site/`, `03-imagery/photos/headshots/`, `03-imagery/icons/`, etc.
- Include EXIF metadata intact where possible (Claude will use it to catalog)
- For restricted imagery, add a plain `.txt` file next to the image explaining the restriction
