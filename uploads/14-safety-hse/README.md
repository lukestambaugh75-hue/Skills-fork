# 14 — Safety, Health, Environment (HSE)

**Priority:** Recommended. LNG is a safety-first industry; HSE messaging has its own voice and protocols.

## What to upload here

### Safety moments / meeting openers
- [ ] Safety moment templates
- [ ] Examples of previously-delivered safety moments
- [ ] Topical safety moments (seasonal, incident-driven, recurring themes)

### HSE messaging
- [ ] Corporate HSE policy
- [ ] Safety vision / mission statements
- [ ] Life-saving rules / cardinal rules (NDLNG's specific set)
- [ ] Stop-work authority language
- [ ] Behavior-based safety program materials

### Incident communication
- [ ] Incident classification rubric (near miss / first aid / recordable / lost time / major)
- [ ] Incident communication templates by severity
- [ ] Internal incident bulletins
- [ ] External incident notifications (regulatory, media if applicable)
- [ ] Holding statement templates
- [ ] Lessons-learned memo format

### Metrics & reporting
- [ ] Safety metrics conventions (TRIR, LTIR, DART, fatality rate)
- [ ] HSE dashboard examples
- [ ] Monthly / quarterly HSE reports

### Training / awareness
- [ ] Safety bulletin templates
- [ ] Safety training presentations (for the pptx skill)
- [ ] Toolbox talk templates
- [ ] Pre-task hazard analysis / JSA templates (if documented)

### Environmental
- [ ] Environmental compliance reports
- [ ] Emissions reporting format
- [ ] Environmental incident reporting

## File types expected

`.docx`, `.pdf`, `.pptx`, `.xlsx`

## What Claude will extract

- HSE voice (usually more direct, more urgent than corporate voice)
- Cardinal / life-saving rules exact wording
- Incident severity language (e.g., "recordable injury" vs. "serious injury")
- Root cause language conventions (5 Whys? TapRoot? specific methodology?)
- Holding statement structure for different severity incidents
- Approved metrics terminology and formatting (TRIR to 2 decimal places, etc.)
- Who speaks for HSE matters (CEO? COO? HSE VP? site manager?)
- Escalation thresholds (when does it go external / to regulators / to public)
- Pre-approved "good catch" / recognition language

## Feeds these skills

- NEW: `skills/safety-hse/` (dedicated skill)
- `skills/pptx/` (safety moment slide template)
- `skills/internal-comms/` (HSE bulletin format)
- NEW: `skills/crisis-communications/` (incident comms, tied here)

## Notes

- Safety messaging must never be slopped or generic. If no real NDLNG safety messaging is uploaded, the skill won't produce anything — better to refuse than sound generic.
- Include "what NOT to say" examples — especially around incidents, blame language, premature causation claims
- If incident language is tightly controlled by legal, note that — Claude will draft but flag for HSE + legal review by default
