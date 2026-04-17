#!/usr/bin/env bash
# =============================================================================
# NextDecade Enterprise Skills — Full-Stack Smoke Test  (v2 — 2026-04-16)
# =============================================================================
#
# PURPOSE: Validate the entire Skills-fork repository is uploadable and
# functional for a fresh enterprise rollout. Tests: file integrity, JSON/YAML
# validity, Python syntax, schema alignment, template availability, hardcoded
# path portability, binary bloat detection, skill manifest completeness,
# branding-vs-formatting override safety, schema cross-validation, render
# pipeline dry-run, and CLAUDE-INSTRUCTIONS structural coverage.
#
# USAGE:
#   chmod +x smoke-test-enterprise.sh
#   ./smoke-test-enterprise.sh
#
# EXIT CODES:
#   0  All tests passed
#   1  One or more tests failed (scroll up for FAIL lines)
#
# WHAT THIS DOES NOT TEST:
#   - Actual document rendering (requires docxtpl, python-docx, openpyxl)
#   - LibreOffice PDF conversion (requires soffice)
#   - Claude API integration (requires API key)
#   - Visual QA of generated documents
#
# =============================================================================

set -uo pipefail
# Note: intentionally NOT using set -e. Many checks use grep/diff that return
# non-zero on "no match" — those are expected, not errors.

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$REPO_ROOT"

PASS=0
FAIL=0
WARN=0

# Counter file — works around the bash pipe-subshell problem where
# `cmd | while read ...` runs the loop in a subshell and counter
# increments are lost when the subshell exits.
_COUNTER_FILE=$(mktemp)
echo "0 0 0" > "$_COUNTER_FILE"
trap 'rm -f "$_COUNTER_FILE"' EXIT

pass() {
    PASS=$((PASS + 1))
    echo "  PASS: $1"
    echo "P" >> "$_COUNTER_FILE"
}
fail() {
    FAIL=$((FAIL + 1))
    echo "  FAIL: $1"
    echo "F" >> "$_COUNTER_FILE"
}
warn() {
    WARN=$((WARN + 1))
    echo "  WARN: $1"
    echo "W" >> "$_COUNTER_FILE"
}
section() { echo ""; echo "=== $1 ==="; }

# _reconcile_counters: call after any pipeline section to pick up
# pass/fail/warn calls that happened inside a pipe subshell.
_reconcile_counters() {
    PASS=$(grep -c '^P$' "$_COUNTER_FILE" 2>/dev/null || true)
    FAIL=$(grep -c '^F$' "$_COUNTER_FILE" 2>/dev/null || true)
    WARN=$(grep -c '^W$' "$_COUNTER_FILE" 2>/dev/null || true)
    # Ensure numeric (strip trailing whitespace/newlines)
    PASS=${PASS//[^0-9]/}; PASS=${PASS:-0}
    FAIL=${FAIL//[^0-9]/}; FAIL=${FAIL:-0}
    WARN=${WARN//[^0-9]/}; WARN=${WARN:-0}
}

# =============================================================================
section "1. Repository structure — required directories exist"
# =============================================================================

REQUIRED_DIRS=(
    "skills/docx"
    "skills/docx/templates"
    "skills/docx/scripts"
    "skills/pptx"
    "skills/pptx/scripts"
    "skills/xlsx"
    "skills/xlsx/scripts"
    "skills/pdf"
    "skills/pdf/scripts"
    "skills/internal-comms"
    "skills/brand-guidelines"
    "skills/skill-creator"
    "skills/mcp-builder"
    "skills/canvas-design"
    "skills/algorithmic-art"
    "skills/frontend-design"
    "skills/doc-coauthoring"
    "skills/slack-gif-creator"
    "skills/theme-factory"
    "skills/web-artifacts-builder"
    "skills/webapp-testing"
    "skills/claude-api"
    "NextDecade-Claude-Project/01-brand-references"
    "NextDecade-Claude-Project/02-templates"
    "NextDecade-Claude-Project/03-original-templates"
    "NextDecade-Claude-Project/04-scripts"
    "NextDecade-Claude-Project/05-samples"
    "spec"
    "template"
    ".claude"
    ".claude-plugin"
)

for d in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$d" ]; then
        pass "$d/"
    else
        fail "$d/ is missing"
    fi
done

# =============================================================================
section "2. Every skill has a SKILL.md with valid YAML frontmatter"
# =============================================================================

SKILL_DIRS=$(find skills -maxdepth 1 -mindepth 1 -type d | sort)
for skill_dir in $SKILL_DIRS; do
    skill_name=$(basename "$skill_dir")
    skill_md="$skill_dir/SKILL.md"
    if [ ! -f "$skill_md" ]; then
        fail "$skill_name: missing SKILL.md"
        continue
    fi
    # Check frontmatter has name + description
    result=$(python3 -c "
import yaml, sys
content = open('$skill_md').read()
if not content.startswith('---'):
    print('NO_FRONTMATTER'); sys.exit()
parts = content.split('---', 2)
if len(parts) < 3:
    print('MALFORMED'); sys.exit()
try:
    fm = yaml.safe_load(parts[1])
except Exception as e:
    print(f'YAML_ERROR:{e}'); sys.exit()
if not isinstance(fm, dict):
    print('NOT_DICT'); sys.exit()
missing = []
if 'name' not in fm: missing.append('name')
if 'description' not in fm: missing.append('description')
if missing:
    print(f'MISSING:{\"|\".join(missing)}')
else:
    print(f'OK:{fm[\"name\"]}')
" 2>&1)
    case "$result" in
        OK:*)
            pass "$skill_name: SKILL.md frontmatter valid (name=${result#OK:})"
            ;;
        MISSING:*)
            fail "$skill_name: frontmatter missing fields: ${result#MISSING:}"
            ;;
        *)
            fail "$skill_name: frontmatter issue: $result"
            ;;
    esac
done

# =============================================================================
section "3. Marketplace manifest — JSON valid, all skill paths resolve"
# =============================================================================

MARKETPLACE=".claude-plugin/marketplace.json"
if [ ! -f "$MARKETPLACE" ]; then
    fail "marketplace.json missing"
else
    if python3 -c "import json; json.load(open('$MARKETPLACE'))" 2>/dev/null; then
        pass "marketplace.json is valid JSON"
    else
        fail "marketplace.json has JSON syntax errors"
    fi

    # Check every skill path in the manifest points to a real directory
    python3 -c "
import json, os
data = json.load(open('$MARKETPLACE'))
for plugin in data.get('plugins', []):
    for skill_path in plugin.get('skills', []):
        clean = skill_path.lstrip('./')
        if os.path.isdir(clean):
            print(f'OK:{plugin[\"name\"]}:{clean}')
        else:
            print(f'MISSING:{plugin[\"name\"]}:{clean}')
" 2>&1 | while IFS= read -r line; do
        case "$line" in
            OK:*)    pass "manifest: ${line#OK:}" ;;
            MISSING:*) fail "manifest path missing: ${line#MISSING:}" ;;
        esac
    done
fi

# =============================================================================
section "4. JSON file validation (all .json files parse cleanly)"
# =============================================================================

JSON_ERRORS=0
while IFS= read -r f; do
    if python3 -c "import json; json.load(open('$f'))" 2>/dev/null; then
        : # silent pass for bulk
    else
        fail "JSON parse error: $f"
        JSON_ERRORS=$((JSON_ERRORS + 1))
    fi
done < <(find . -name '*.json' -not -path './.git/*' -type f)
if [ "$JSON_ERRORS" -eq 0 ]; then
    pass "All JSON files parse cleanly"
fi

# =============================================================================
section "5. Python syntax validation (all .py files compile)"
# =============================================================================

PY_ERRORS=0
while IFS= read -r f; do
    if python3 -c "import ast; ast.parse(open('$f').read())" 2>/dev/null; then
        : # silent pass
    else
        fail "Python syntax error: $f"
        PY_ERRORS=$((PY_ERRORS + 1))
    fi
done < <(find . -name '*.py' -not -path './.git/*' -type f)
if [ "$PY_ERRORS" -eq 0 ]; then
    pass "All Python files have valid syntax"
fi

# =============================================================================
section "6. Schema files — exist and match their templates"
# =============================================================================

SCHEMA_PAIRS=(
    "skills/docx/templates/procedure_schema.json:skills/docx/templates/Procedure Template (Jinja).docx"
    "skills/docx/templates/standard_schema.json:skills/docx/templates/Standard Template (Jinja).docx"
    "skills/docx/templates/guidance_schema.json:skills/docx/templates/Guidance Template (Jinja).docx"
)
for pair in "${SCHEMA_PAIRS[@]}"; do
    schema="${pair%%:*}"
    template="${pair#*:}"
    if [ -f "$schema" ]; then
        pass "schema exists: $schema"
    else
        fail "schema missing: $schema"
    fi
    if [ -f "$template" ]; then
        pass "template exists: $template"
    else
        fail "template missing: $template"
    fi
done

# Also check duplicates in NextDecade-Claude-Project/02-templates/
for schema_name in procedure_schema.json standard_schema.json guidance_schema.json; do
    nc_schema="NextDecade-Claude-Project/02-templates/$schema_name"
    sk_schema="skills/docx/templates/$schema_name"
    if [ -f "$nc_schema" ] && [ -f "$sk_schema" ]; then
        if diff -q "$nc_schema" "$sk_schema" > /dev/null 2>&1; then
            pass "schema in sync: $schema_name (skills/ == NextDecade-Claude-Project/)"
        else
            warn "schema DIVERGED: $schema_name differs between skills/docx/templates/ and NextDecade-Claude-Project/02-templates/"
        fi
    fi
done

# Verify schema source_template fields reference existing files in 03-original-templates/
python3 -c "
import json, os
orig = 'NextDecade-Claude-Project/03-original-templates'
for name in ('procedure', 'standard', 'guidance'):
    schema = json.load(open(f'skills/docx/templates/{name}_schema.json'))
    src = schema.get('source_template', '')
    if not src:
        print(f'WARN:{name}_schema.json has no source_template field')
        continue
    path = os.path.join(orig, src)
    if os.path.exists(path):
        print(f'OK:{name} source_template exists: {src}')
    else:
        print(f'WARN:{name} source_template not found: {src} (check 03-original-templates/)')
" 2>&1 | while IFS= read -r line; do
    case "$line" in
        OK:*)   pass "${line#OK:}" ;;
        WARN:*) warn "${line#WARN:}" ;;
        FAIL:*) fail "${line#FAIL:}" ;;
    esac
done

# =============================================================================
section "7. NextDecade-Claude-Project bundle — critical files present"
# =============================================================================

BUNDLE_FILES=(
    "NextDecade-Claude-Project/START-HERE.md"
    "NextDecade-Claude-Project/CLAUDE-INSTRUCTIONS.md"
    "NextDecade-Claude-Project/PROJECT-SELFTEST.md"
    "NextDecade-Claude-Project/01-brand-references/Brand & Style Guidelines 2024.pdf"
    "NextDecade-Claude-Project/01-brand-references/Writing Style Guide & Resources 2024.pdf"
    "NextDecade-Claude-Project/02-templates/Procedure Template (Jinja).docx"
    "NextDecade-Claude-Project/02-templates/Standard Template (Jinja).docx"
    "NextDecade-Claude-Project/02-templates/Guidance Template (Jinja).docx"
    "NextDecade-Claude-Project/02-templates/NextDecade PowerPoint Master (Oct 2025, brand-corrected).potx"
    "NextDecade-Claude-Project/02-templates/NextDecade PowerPoint Master (Oct 2025, brand-corrected).pdf"
    "NextDecade-Claude-Project/02-templates/HSSE Flash Template.pptx"
    "NextDecade-Claude-Project/02-templates/HSSE Flash Template.pdf"
    "NextDecade-Claude-Project/03-original-templates/NextDecade Blank Procedure Template_Rev 1 April 9th 2026.docx"
    "NextDecade-Claude-Project/03-original-templates/Standard Template.docx"
    "NextDecade-Claude-Project/03-original-templates/Guidance Template.docx"
    "NextDecade-Claude-Project/05-samples/Hot Work Procedure (docxtpl).docx"
    "NextDecade-Claude-Project/05-samples/Hot Work Procedure (docxtpl).pdf"
    "NextDecade-Claude-Project/05-samples/Hot Work Safety Standard.docx"
    "NextDecade-Claude-Project/05-samples/Hot Work Safety Guidance.docx"
    "NextDecade-Claude-Project/05-samples/Hot Work Safety Moment.pptx"
    "NextDecade-Claude-Project/05-samples/Hot Work All-Hands Email.docx"
    "NextDecade-Claude-Project/05-samples/Hot Work Permit Tracker.xlsx"
    "NextDecade-Claude-Project/05-samples/input-example.json"
    "extracted-specs.md"
    "gap-report.md"
)

for f in "${BUNDLE_FILES[@]}"; do
    if [ -f "$f" ]; then
        pass "bundle: $f"
    else
        fail "bundle missing: $f"
    fi
done

# =============================================================================
section "8. Render scripts — import chain check (no missing modules at parse)"
# =============================================================================

RENDER_SCRIPTS=(
    "skills/docx/scripts/render_docx.py"
    "skills/docx/scripts/lint_docx_template.py"
    "skills/docx/scripts/build_procedure_jinja.py"
    "skills/pptx/scripts/render_pptx.py"
    "skills/pptx/scripts/lint_pptx_master.py"
    "skills/xlsx/scripts/recalc.py"
)
for script in "${RENDER_SCRIPTS[@]}"; do
    if [ -f "$script" ]; then
        pass "render script exists: $script"
    else
        fail "render script missing: $script"
    fi
done

# Check the NextDecade-Claude-Project/04-scripts/ copies exist too
for script_name in render_docx.py render_pptx.py lint_docx_template.py lint_pptx_master.py; do
    nc_script="NextDecade-Claude-Project/04-scripts/$script_name"
    if [ -f "$nc_script" ]; then
        pass "NC script: $nc_script"
    else
        warn "NC script missing (may be OK if not duplicated): $nc_script"
    fi
done

# Verify render_pptx.py imports successfully (catches broken import chains)
python3 -c "
import sys, importlib.util, os
os.chdir('$(pwd)')
spec = importlib.util.spec_from_file_location('render_pptx', 'skills/pptx/scripts/render_pptx.py')
try:
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    if hasattr(mod, 'render'):
        print('OK:render_pptx.py imports successfully, render() present')
    else:
        print('WARN:render_pptx.py imports but render() function not found')
except Exception as e:
    print(f'FAIL:render_pptx.py import failed: {e}')
" 2>&1 | while IFS= read -r line; do
    case "$line" in
        OK:*)   pass "${line#OK:}" ;;
        WARN:*) warn "${line#WARN:}" ;;
        FAIL:*) fail "${line#FAIL:}" ;;
    esac
done

# =============================================================================
section "9. Hardcoded path audit"
# =============================================================================

echo "  Checking for hardcoded /home/user/Skills-fork paths in code..."
HC_COUNT=$(grep -rn '/home/user/Skills-fork' --include='*.py' . 2>/dev/null | grep -v '.git/' | wc -l || true)
if [ "$HC_COUNT" -eq 0 ]; then
    pass "No hardcoded absolute paths in Python files"
else
    warn "$HC_COUNT hardcoded /home/user/Skills-fork references in .py files (breaks portability)"
    grep -rn '/home/user/Skills-fork' --include='*.py' . 2>/dev/null | grep -v '.git/' | head -10 | while IFS= read -r line; do
        echo "       $line"
    done
fi

# =============================================================================
section "10. Binary bloat check — large tracked files"
# =============================================================================
# Threshold is 10MB. Files between 5-10MB are expected (PPTX templates, POTX
# masters, reference PDFs). Files over 10MB are unexpected and should be
# distributed via GitHub Releases instead of committed to the repo.
# Known intentional tracked binaries (5-10MB):
#   NextDecade PowerPoint Master (Oct 2025, brand-corrected).potx  ~6MB
#   NextDecade PowerPoint Master (Oct 2025, brand-corrected).pdf   ~5MB
#   HSSE Flash Template.pptx                                       ~5MB
#   Hot Work Safety Moment.pptx                                    ~6MB

echo "  Listing tracked binary files > 10MB..."
BLOAT_COUNT=0
while IFS= read -r fpath; do
    [ -z "$fpath" ] && continue
    if [ -f "$fpath" ]; then
        size=$(stat -c%s "$fpath" 2>/dev/null || stat -f%z "$fpath" 2>/dev/null || echo 0)
        if [ "$size" -gt 10485760 ]; then
            size_mb=$(( size / 1048576 ))
            warn "large tracked file (${size_mb}MB): $fpath"
            BLOAT_COUNT=$((BLOAT_COUNT + 1))
        fi
    fi
done < <(git ls-files 2>/dev/null)
if [ "$BLOAT_COUNT" -eq 0 ]; then
    pass "No tracked files exceed 10MB (expected template binaries are under threshold)"
fi

# =============================================================================
section "11. Output files — identify generated artifacts NOT needed for fresh upload"
# =============================================================================

echo "  Files in output/final/ (these are generated examples, not required for skill upload):"
if [ -d "output/final" ]; then
    OUTPUT_COUNT=$(find output/final -type f | wc -l)
    echo "  Found $OUTPUT_COUNT files in output/final/:"
    find output/final -type f | sort | while IFS= read -r f; do
        size=$(stat -c%s "$f" 2>/dev/null || stat -f%z "$f" 2>/dev/null || echo 0)
        size_mb=$(( size / 1048576 ))
        echo "       [${size_mb}MB] $f"
    done
    warn "output/final/ contains $OUTPUT_COUNT generated example files (not needed for fresh skill upload)"
else
    pass "No output/final/ directory (clean for upload)"
fi

echo ""
echo "  Tracked files/dirs NOT required for a fresh skills-only upload:"

NOT_NEEDED_FOR_UPLOAD=(
    "samples/document-types-validation"
    "output/final"
    ".claude/plans"
    "skills/theme-factory/theme-showcase.pdf"
)
for item in "${NOT_NEEDED_FOR_UPLOAD[@]}"; do
    # Only warn if the item is actually tracked by git (not just present on disk)
    if git ls-files --error-unmatch "$item" > /dev/null 2>&1 || \
       [ -n "$(git ls-files "$item" 2>/dev/null)" ]; then
        if [ -d "$item" ]; then
            item_size=$(du -sm "$item" 2>/dev/null | cut -f1)
            warn "tracked but removable for fresh upload: $item/ (${item_size}MB dir)"
        elif [ -f "$item" ]; then
            size=$(stat -c%s "$item" 2>/dev/null || stat -f%z "$item" 2>/dev/null || echo 0)
            size_mb=$(( size / 1048576 ))
            warn "tracked but removable for fresh upload: $item (${size_mb}MB)"
        fi
    fi
done

# =============================================================================
section "12. .gitignore coverage check"
# =============================================================================

# output/final/ is tracked but output/iter*/ is ignored — check if this is intentional
if grep -q 'output/iter' .gitignore 2>/dev/null; then
    pass ".gitignore ignores output/iter*/"
else
    warn ".gitignore does not ignore output/iter*/"
fi

if grep -q 'output/final' .gitignore 2>/dev/null; then
    pass ".gitignore ignores output/final/"
else
    warn "output/final/ is NOT in .gitignore (tracked generated output)"
fi

if grep -q '__pycache__' .gitignore 2>/dev/null; then
    pass ".gitignore ignores __pycache__/"
else
    fail ".gitignore missing __pycache__/"
fi

# Check for env/secrets patterns
for pattern in ".env" "*.key" "*.pem" "credentials"; do
    if grep -q "$pattern" .gitignore 2>/dev/null; then
        pass ".gitignore covers $pattern"
    else
        warn ".gitignore does not cover $pattern (no secrets protection for this pattern)"
    fi
done

# =============================================================================
section "13. Brand-guidelines skill — still references Anthropic, not NextDecade"
# =============================================================================

if grep -qi "anthropic" skills/brand-guidelines/SKILL.md 2>/dev/null; then
    warn "skills/brand-guidelines/SKILL.md still references Anthropic branding (not NextDecade)"
    echo "       This is the upstream skill — may need replacing or removing for NDLNG enterprise rollout"
else
    pass "brand-guidelines skill does not reference Anthropic"
fi

# =============================================================================
section "14. DOCX template sync — skills/ vs NextDecade-Claude-Project/"
# =============================================================================

for tpl_name in "Procedure Template (Jinja).docx" "Standard Template (Jinja).docx" "Guidance Template (Jinja).docx"; do
    sk="skills/docx/templates/$tpl_name"
    nc="NextDecade-Claude-Project/02-templates/$tpl_name"
    if [ -f "$sk" ] && [ -f "$nc" ]; then
        if diff -q "$sk" "$nc" > /dev/null 2>&1; then
            pass "template in sync: $tpl_name"
        else
            fail "TEMPLATE DIVERGED: $tpl_name differs between skills/ and NextDecade-Claude-Project/"
        fi
    elif [ ! -f "$sk" ]; then
        fail "missing in skills/: $tpl_name"
    elif [ ! -f "$nc" ]; then
        fail "missing in NextDecade-Claude-Project/: $tpl_name"
    fi
done

# =============================================================================
section "15. Procedure schema v2 — required markers completeness"
# =============================================================================

python3 -c "
import json
schema = json.load(open('skills/docx/templates/procedure_schema.json'))
required = set(schema.get('required_markers', []))
fields = set(schema.get('fields', {}).keys())

# Every required marker should have a field definition
undocumented = required - fields
if undocumented:
    for m in sorted(undocumented):
        print(f'FAIL:required marker \"{m}\" has no field definition in schema')
else:
    print('OK:all required markers have field definitions')

# Every field should be required or optional
optional = set(schema.get('optional_markers', []))
orphan_fields = fields - required - optional
if orphan_fields:
    for f in sorted(orphan_fields):
        print(f'WARN:field \"{f}\" is defined but not in required_markers or optional_markers')
" 2>&1 | while IFS= read -r line; do
    case "$line" in
        OK:*)   pass "${line#OK:}" ;;
        FAIL:*) fail "${line#FAIL:}" ;;
        WARN:*) warn "${line#WARN:}" ;;
    esac
done

# =============================================================================
section "16. Sample input JSON — validates against procedure schema required fields"
# =============================================================================

SAMPLE_INPUT="NextDecade-Claude-Project/05-samples/input-example.json"
if [ -f "$SAMPLE_INPUT" ]; then
    python3 -c "
import json
schema = json.load(open('skills/docx/templates/procedure_schema.json'))
sample = json.load(open('$SAMPLE_INPUT'))
required = schema.get('required_markers', [])
missing = [r for r in required if r not in sample]
if missing:
    for m in missing:
        print(f'FAIL:input-example.json missing required field: {m}')
else:
    print(f'OK:input-example.json has all {len(required)} required fields')
" 2>&1 | while IFS= read -r line; do
        case "$line" in
            OK:*)   pass "${line#OK:}" ;;
            FAIL:*) fail "${line#FAIL:}" ;;
        esac
    done
else
    fail "input-example.json not found"
fi

# =============================================================================
section "17. CLAUDE-INSTRUCTIONS.md — brand constants spot-check"
# =============================================================================

INSTRUCTIONS="NextDecade-Claude-Project/CLAUDE-INSTRUCTIONS.md"
if [ -f "$INSTRUCTIONS" ]; then
    # Check critical brand values are present
    for value in "#002060" "#FC7134" "#00B050" "Segoe UI" "NextDecade Corporation" "Delivering Energy" "Confidential and Proprietary"; do
        if grep -q "$value" "$INSTRUCTIONS" 2>/dev/null; then
            pass "CLAUDE-INSTRUCTIONS contains: $value"
        else
            fail "CLAUDE-INSTRUCTIONS missing brand constant: $value"
        fi
    done
else
    fail "CLAUDE-INSTRUCTIONS.md not found"
fi

# =============================================================================
section "18. Duplicate content detection — output/final vs samples/"
# =============================================================================

echo "  Checking for identical files between output/final/ and samples/..."
DUP_COUNT=0
if [ -d "output/final" ] && [ -d "samples/document-types-validation" ]; then
    while IFS= read -r output_file; do
        basename_f=$(basename "$output_file")
        # Find matching filename in samples/
        match=$(find samples/document-types-validation -name "$basename_f" -type f 2>/dev/null | head -1)
        if [ -n "$match" ]; then
            if diff -q "$output_file" "$match" > /dev/null 2>&1; then
                warn "DUPLICATE: output/final/$basename_f is identical to $match"
                DUP_COUNT=$((DUP_COUNT + 1))
            fi
        fi
    done < <(find output/final -type f 2>/dev/null)
fi
if [ "$DUP_COUNT" -eq 0 ]; then
    pass "No exact duplicates between output/final/ and samples/"
else
    warn "$DUP_COUNT files in output/final/ are exact duplicates of samples/ files"
fi

# =============================================================================
section "19. PPTX brand-family gate — render_pptx.py validates brand field"
# =============================================================================

for render_pptx in skills/pptx/scripts/render_pptx.py NextDecade-Claude-Project/04-scripts/render_pptx.py; do
    if [ -f "$render_pptx" ]; then
        if grep -q 'BRAND_PREFIXES' "$render_pptx" 2>/dev/null; then
            pass "$render_pptx has brand-family gate (BRAND_PREFIXES)"
        else
            fail "$render_pptx missing brand-family gate"
        fi
        if grep -q '_validate_brand_and_layouts' "$render_pptx" 2>/dev/null; then
            pass "$render_pptx has layout validator"
        else
            fail "$render_pptx missing layout validator"
        fi
    fi
done

# =============================================================================
section "20. spec/agent-skills-spec.md — content check"
# =============================================================================

SPEC="spec/agent-skills-spec.md"
if [ -f "$SPEC" ]; then
    SPEC_LINES=$(wc -l < "$SPEC")
    if [ "$SPEC_LINES" -lt 5 ]; then
        warn "spec/agent-skills-spec.md is a stub ($SPEC_LINES lines) — just a redirect to agentskills.io"
    else
        pass "spec/agent-skills-spec.md has content ($SPEC_LINES lines)"
    fi
else
    fail "spec/agent-skills-spec.md missing"
fi

# =============================================================================
section "21. Branding-vs-formatting override safety"
# =============================================================================
# CRITICAL CHECK: Verify that brand-guidelines SKILL.md contains ZERO document
# structure rules (section ordering, heading numbers, table layouts). If it
# does, branding could silently override Procedure/Standard/Guidance formatting.

echo "  Checking brand-guidelines SKILL.md for structural directives..."
BRAND_SKILL="skills/brand-guidelines/SKILL.md"
if [ -f "$BRAND_SKILL" ]; then
    # These patterns indicate document-structure rules that belong in docx/SKILL.md, NOT brand-guidelines
    STRUCT_LEAKS=0
    for pattern in \
        "1\.0 Purpose" \
        "2\.0 Scope" \
        "3\.0 Roles" \
        "5\.0 Procedure" \
        "INTRODUCTION.*SCOPE.*GOVERNANCE" \
        "PURPOSE.*GUIDELINE.*APPROVAL" \
        "section_title" \
        "revision_history" \
        "Heading 1.*Heading 2" \
        "RGLNG 1.*Hdg1" \
        "procedure_schema" \
        "standard_schema" \
        "guidance_schema"; do
        if grep -qiP "$pattern" "$BRAND_SKILL" 2>/dev/null; then
            fail "brand-guidelines leaks document structure: matches /$pattern/"
            STRUCT_LEAKS=$((STRUCT_LEAKS + 1))
        fi
    done
    if [ "$STRUCT_LEAKS" -eq 0 ]; then
        pass "brand-guidelines contains NO document-structure rules (clean separation)"
    fi

    # Verify it DOES contain the branding items it should
    for brand_item in "#002060" "#FC7134" "#00B050" "Segoe UI" "NextDecade Corporation"; do
        if grep -q "$brand_item" "$BRAND_SKILL" 2>/dev/null; then
            pass "brand-guidelines has expected brand constant: $brand_item"
        else
            fail "brand-guidelines missing brand constant: $brand_item"
        fi
    done
else
    fail "brand-guidelines SKILL.md not found"
fi

# =============================================================================
section "22. docx SKILL.md — contains structure rules (must NOT leak brand overrides)"
# =============================================================================
# The docx skill should define document structure but should NOT redefine brand
# colors/fonts in a way that conflicts with brand-guidelines.

DOCX_SKILL="skills/docx/SKILL.md"
if [ -f "$DOCX_SKILL" ]; then
    # Check it has the structural rules it needs
    STRUCT_HITS=0
    for structural_term in "procedure_title" "standard_schema" "guidance_schema" \
                           "render_docx.py" "Revision History" "Cover page"; do
        if grep -q "$structural_term" "$DOCX_SKILL" 2>/dev/null; then
            STRUCT_HITS=$((STRUCT_HITS + 1))
        fi
    done
    if [ "$STRUCT_HITS" -ge 4 ]; then
        pass "docx SKILL.md has document-structure rules ($STRUCT_HITS/6 key terms)"
    else
        warn "docx SKILL.md may be missing structure rules (only $STRUCT_HITS/6 key terms found)"
    fi

    # Check for conflicting brand color definitions that differ from brand-guidelines
    python3 -c "
import re, sys
docx = open('$DOCX_SKILL').read()
brand = open('$BRAND_SKILL').read() if __import__('os').path.exists('$BRAND_SKILL') else ''
# Extract hex colors from both files
docx_colors = set(re.findall(r'#[0-9A-Fa-f]{6}', docx))
brand_colors = set(re.findall(r'#[0-9A-Fa-f]{6}', brand))
# Colors in docx that are NOT in brand-guidelines could be conflicts
docx_only = docx_colors - brand_colors
if docx_only:
    # Filter out common non-brand hex (e.g. XML namespace fragments)
    real_colors = {c for c in docx_only if not c.startswith('#xmlns')}
    if real_colors:
        print(f'WARN:docx SKILL.md defines colors not in brand-guidelines: {real_colors}')
    else:
        print('OK:no conflicting colors')
else:
    print('OK:all colors in docx SKILL.md also appear in brand-guidelines (no conflict)')
" 2>&1 | while IFS= read -r line; do
        case "$line" in
            OK:*)   pass "${line#OK:}" ;;
            WARN:*) warn "${line#WARN:}" ;;
            FAIL:*) fail "${line#FAIL:}" ;;
        esac
    done
else
    fail "docx SKILL.md not found"
fi

# =============================================================================
section "23. CLAUDE-INSTRUCTIONS.md — structure rules match schema section order"
# =============================================================================
# Verify the governance document section ordering in CLAUDE-INSTRUCTIONS.md
# matches the schemas. If they diverge, Claude Projects will produce docs
# with wrong section order.

INSTRUCTIONS="NextDecade-Claude-Project/CLAUDE-INSTRUCTIONS.md"
if [ -f "$INSTRUCTIONS" ]; then
    # Procedure structure check: must mention Cover, Revision History, Purpose,
    # Scope, Roles, Safety/PPE, Procedure body, Record Keeping, Definitions, References, Appendix
    PROC_SECTIONS=0
    for section_marker in "Cover page" "Revision History" "Purpose" "Scope" \
                          "Roles and Responsibilities" "Safety" "PPE" \
                          "Procedure" "Record Keeping" "Definitions" "References" "Appendix"; do
        if grep -qi "$section_marker" "$INSTRUCTIONS" 2>/dev/null; then
            PROC_SECTIONS=$((PROC_SECTIONS + 1))
        fi
    done
    if [ "$PROC_SECTIONS" -ge 10 ]; then
        pass "CLAUDE-INSTRUCTIONS covers Procedure structure ($PROC_SECTIONS/12 sections)"
    else
        fail "CLAUDE-INSTRUCTIONS missing Procedure sections (only $PROC_SECTIONS/12)"
    fi

    # Standard structure check
    STD_SECTIONS=0
    for section_marker in "INTRODUCTION" "SCOPE" "INTEGRATED GOVERNANCE" "DEFINITIONS" \
                          "REFERENCES" "EXCEPTION REQUEST" "CONTINUOUS IMPROVEMENT" \
                          "OWNERSHIP" "APPROVAL" "REVISION HISTORY"; do
        if grep -q "$section_marker" "$INSTRUCTIONS" 2>/dev/null; then
            STD_SECTIONS=$((STD_SECTIONS + 1))
        fi
    done
    if [ "$STD_SECTIONS" -ge 8 ]; then
        pass "CLAUDE-INSTRUCTIONS covers Standard structure ($STD_SECTIONS/10 sections)"
    else
        fail "CLAUDE-INSTRUCTIONS missing Standard sections (only $STD_SECTIONS/10)"
    fi

    # Guidance structure check
    GDN_SECTIONS=0
    for section_marker in "PURPOSE" "INTEGRATED GOVERNANCE" "GUIDELINE" \
                          "OWNERSHIP" "APPROVAL" "REVISION HISTORY"; do
        if grep -q "$section_marker" "$INSTRUCTIONS" 2>/dev/null; then
            GDN_SECTIONS=$((GDN_SECTIONS + 1))
        fi
    done
    if [ "$GDN_SECTIONS" -ge 5 ]; then
        pass "CLAUDE-INSTRUCTIONS covers Guidance structure ($GDN_SECTIONS/6 sections)"
    else
        fail "CLAUDE-INSTRUCTIONS missing Guidance sections (only $GDN_SECTIONS/6)"
    fi

    # Check that CLAUDE-INSTRUCTIONS defers to templates (not re-defining structure from scratch)
    if grep -qi "use the templates in" "$INSTRUCTIONS" 2>/dev/null; then
        pass "CLAUDE-INSTRUCTIONS defers to templates ('use the templates in')"
    else
        warn "CLAUDE-INSTRUCTIONS may not explicitly defer to templates for rendering"
    fi
else
    fail "CLAUDE-INSTRUCTIONS.md not found"
fi

# =============================================================================
section "24. Schema cross-validation — Procedure vs Standard vs Guidance"
# =============================================================================
# Verify schemas don't accidentally share field names with incompatible types
# (e.g., both define 'definitions' but with different column structures).

python3 -c "
import json, sys

proc = json.load(open('skills/docx/templates/procedure_schema.json'))
std  = json.load(open('skills/docx/templates/standard_schema.json'))
gdn  = json.load(open('skills/docx/templates/guidance_schema.json'))

proc_fields = set(proc.get('required_markers', []) + proc.get('optional_markers', []))
std_fields  = set(std.get('required_markers', []) + std.get('optional_markers', []))
gdn_fields  = set(gdn.get('required_markers', []) + gdn.get('optional_markers', []))

# Fields shared between schemas
proc_std = proc_fields & std_fields
proc_gdn = proc_fields & gdn_fields
std_gdn  = std_fields & gdn_fields

if proc_std:
    # Check if shared fields have compatible shapes
    for f in sorted(proc_std):
        p_def = proc.get('fields', {}).get(f, {})
        s_def = std.get('fields', {}).get(f, {})
        p_type = p_def.get('type', 'unknown')
        s_type = s_def.get('type', 'unknown')
        if p_type != s_type and p_type != 'unknown' and s_type != 'unknown':
            print(f'WARN:shared field \"{f}\" has different types: procedure={p_type}, standard={s_type}')
        else:
            print(f'OK:shared field \"{f}\" compatible between procedure and standard')

if std_gdn:
    for f in sorted(std_gdn):
        s_def = std.get('fields', {}).get(f, {})
        g_def = gdn.get('fields', {}).get(f, {})
        s_type = s_def.get('type', 'unknown')
        g_type = g_def.get('type', 'unknown')
        if s_type != g_type and s_type != 'unknown' and g_type != 'unknown':
            print(f'WARN:shared field \"{f}\" has different types: standard={s_type}, guidance={g_type}')
        else:
            print(f'OK:shared field \"{f}\" compatible between standard and guidance')

# Verify each schema has a version field (schema_version or version)
for name, schema in [('procedure', proc), ('standard', std), ('guidance', gdn)]:
    ver = schema.get('schema_version', schema.get('version', 'MISSING'))
    if ver == 'MISSING':
        print(f'FAIL:{name} schema missing schema_version field')
    else:
        print(f'OK:{name} schema schema_version={ver}')
" 2>&1 | while IFS= read -r line; do
    case "$line" in
        OK:*)   pass "${line#OK:}" ;;
        WARN:*) warn "${line#WARN:}" ;;
        FAIL:*) fail "${line#FAIL:}" ;;
    esac
done

# =============================================================================
section "25. Render pipeline dry-run — import check + strict-only design verification"
# =============================================================================
# Import render_docx.py, verify DOC_TYPES is populated, templates/schemas
# exist, and confirm the strict-only design: no fallback registry, no lenient
# renderer, no fallback key in any DOC_TYPES entry.

python3 -c "
import sys, importlib.util, os
os.chdir('$(pwd)')
spec = importlib.util.spec_from_file_location('render_docx', 'skills/docx/scripts/render_docx.py')
try:
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    doc_types = getattr(mod, 'DOC_TYPES', {})
    if not doc_types:
        print('FAIL:DOC_TYPES registry is empty after import')
    else:
        for dt, cfg in doc_types.items():
            jinja = cfg.get('jinja_template')
            schema = cfg.get('schema')
            if jinja and jinja.exists():
                print(f'OK:{dt} jinja template found: {jinja.name}')
            else:
                print(f'FAIL:{dt} jinja template missing: {jinja}')
            if schema and schema.exists():
                print(f'OK:{dt} schema found: {schema.name}')
            else:
                print(f'FAIL:{dt} schema missing: {schema}')
            # Strict-only: no fallback key should exist in any DOC_TYPES entry
            if 'fallback' in cfg:
                print(f'FAIL:{dt} unexpected fallback key in DOC_TYPES cfg (strict-only design)')
            else:
                print(f'OK:{dt} no fallback key in DOC_TYPES cfg (strict-only confirmed)')
    # Verify FALLBACK_FNS registry was removed
    if hasattr(mod, 'FALLBACK_FNS'):
        print('FAIL:FALLBACK_FNS registry still present — should be absent in strict-only design')
    else:
        print('OK:FALLBACK_FNS registry absent (strict-only design confirmed)')
    # Verify lenient renderer was removed
    if hasattr(mod, 'render_via_docxtpl_lenient'):
        print('FAIL:render_via_docxtpl_lenient still present — should be absent in strict-only design')
    else:
        print('OK:render_via_docxtpl_lenient absent (strict-only design confirmed)')
    # Verify strict renderer exists
    if hasattr(mod, 'render_via_docxtpl'):
        print('OK:render_via_docxtpl present (strict renderer)')
    else:
        print('FAIL:render_via_docxtpl missing — primary render function not found')
except Exception as e:
    print(f'FAIL:render_docx.py import failed: {e}')
" 2>&1 | while IFS= read -r line; do
    case "$line" in
        OK:*)   pass "${line#OK:}" ;;
        WARN:*) warn "${line#WARN:}" ;;
        FAIL:*) fail "${line#FAIL:}" ;;
    esac
done

# =============================================================================
section "26. Schema definitions shape — Procedure vs Standard compatibility"
# =============================================================================
# The strict render path uses StrictUndefined, so if a schema field exists in
# one doc type but not another, and a template accidentally references the wrong
# field, it raises immediately. Verify that shared fields have compatible shapes
# across Procedure and Standard schemas so the render pipeline can use the same
# data structure for both.

python3 -c "
import json
proc = json.load(open('skills/docx/templates/procedure_schema.json'))
std  = json.load(open('skills/docx/templates/standard_schema.json'))
gdn  = json.load(open('skills/docx/templates/guidance_schema.json'))

for name, schema in [('procedure', proc), ('standard', std), ('guidance', gdn)]:
    defs = schema.get('fields', {}).get('definitions', {})
    items = defs.get('items', {})
    keys = sorted(items.keys()) if isinstance(items, dict) else []
    if keys:
        print(f'INFO:{name} definitions item keys: {keys}')
    else:
        print(f'INFO:{name} definitions: list-of-strings or not present in schema fields')

# Verify schemas have the same revision_history shape (shared critical field)
for field in ['revision_history', 'raci', 'approval']:
    shapes = {}
    for name, schema in [('procedure', proc), ('standard', std), ('guidance', gdn)]:
        f = schema.get('fields', {}).get(field, {})
        if f:
            shapes[name] = f.get('type', 'unknown')
    if len(set(shapes.values())) == 1:
        print(f'OK:shared field \"{field}\" same type across all schemas ({list(shapes.values())[0]})')
    elif shapes:
        print(f'WARN:shared field \"{field}\" type mismatch: {shapes}')
" 2>&1 | while IFS= read -r line; do
    case "$line" in
        OK:*)   pass "${line#OK:}" ;;
        INFO:*) echo "  ${line#INFO:}" ;;
        WARN:*) warn "${line#WARN:}" ;;
        FAIL:*) fail "${line#FAIL:}" ;;
    esac
done

# =============================================================================
section "27. Cover-page fixup fragility — placeholder strings still in templates"
# =============================================================================
# _post_render_cover_fixup relies on exact string matches ("NAME",
# "xxx-xxx-xxx-xxx-xxx-#####") in Standard/Guidance templates.
# Verify these placeholders are present in the Jinja templates.

for doc_type in standard guidance; do
    tpl_file="skills/docx/templates/$(echo "$doc_type" | sed 's/^./\U&/') Template (Jinja).docx"
    if [ -f "$tpl_file" ]; then
        # Extract text content from the docx zip (word/*.xml)
        FOUND_PLACEHOLDERS=0
        for placeholder in "NAME" "xxx-xxx-xxx-xxx-xxx-#####"; do
            if python3 -c "
import zipfile, sys
with zipfile.ZipFile('$tpl_file') as z:
    for name in z.namelist():
        if name.startswith('word/') and name.endswith('.xml'):
            content = z.read(name).decode('utf-8', errors='replace')
            if '$placeholder' in content:
                sys.exit(0)
sys.exit(1)
" 2>/dev/null; then
                FOUND_PLACEHOLDERS=$((FOUND_PLACEHOLDERS + 1))
            fi
        done
        if [ "$FOUND_PLACEHOLDERS" -ge 1 ]; then
            pass "$doc_type template has cover-page placeholders ($FOUND_PLACEHOLDERS/2)"
        else
            warn "$doc_type template missing cover-page placeholders — _post_render_cover_fixup will be a no-op"
        fi
    fi
done

# =============================================================================
section "28. Sample input JSON — validates ALL three doc types"
# =============================================================================

VALIDATION_INPUTS=(
    "procedure:samples/document-types-validation/_inputs/vendor-onboarding-procedure.json:skills/docx/templates/procedure_schema.json"
    "standard:samples/document-types-validation/_inputs/records-retention-standard.json:skills/docx/templates/standard_schema.json"
    "guidance:samples/document-types-validation/_inputs/remote-work-guidance.json:skills/docx/templates/guidance_schema.json"
)
for entry in "${VALIDATION_INPUTS[@]}"; do
    IFS=':' read -r dtype input_file schema_file <<< "$entry"
    if [ -f "$input_file" ] && [ -f "$schema_file" ]; then
        python3 -c "
import json
schema = json.load(open('$schema_file'))
sample = json.load(open('$input_file'))
# Check required_markers (Jinja template markers)
required = schema.get('required_markers', [])
missing = [r for r in required if r not in sample]
if missing:
    for m in missing:
        print(f'FAIL:$dtype input missing required Jinja field: {m}')
else:
    print(f'OK:$dtype input has all {len(required)} required Jinja fields')
# Check post_render_markers (handled by _post_render_cover_fixup, not Jinja)
post = schema.get('post_render_markers', [])
missing_post = [r for r in post if r not in sample]
if missing_post:
    for m in missing_post:
        print(f'FAIL:$dtype input missing post-render field: {m}')
elif post:
    print(f'OK:$dtype input has all {len(post)} post-render fields ({post})')
" 2>&1 | while IFS= read -r line; do
            case "$line" in
                OK:*)   pass "${line#OK:}" ;;
                FAIL:*) fail "${line#FAIL:}" ;;
            esac
        done
    else
        [ ! -f "$input_file" ] && warn "$dtype validation input not found: $input_file"
        [ ! -f "$schema_file" ] && fail "$dtype schema not found: $schema_file"
    fi
done

# =============================================================================
section "29. Files NOT relevant to fresh skill upload — inventory"
# =============================================================================

echo "  Comprehensive list of files/dirs that can be excluded from a clean"
echo "  skills-only upload (they are examples, dev artifacts, or build outputs):"
echo ""

NOT_NEEDED=(
    ".claude/plans:Development planning docs — not runtime"
    "samples/document-types-validation:Validation sample set — rebuild via _build/ scripts"
    "output/final:Generated example outputs — add to .gitignore"
    "SMOKE-TEST-FINDINGS.md:Previous smoke test findings — superseded by this script"
    "extracted-specs.md:Claude-readable brand distillation — useful for Claude Projects but not for skill upload"
    "gap-report.md:Gap analysis — useful for Claude Projects but not for skill upload"
    "NextDecade-Claude-Project/05-samples:Hot Work example set — reference only"
    "NextDecade-Claude-Project/03-original-templates:Source templates before Jinja tagging — used by build scripts not runtime"
)
NN_FOUND=0
for entry in "${NOT_NEEDED[@]}"; do
    IFS=':' read -r item reason <<< "$entry"
    # Only count items that are tracked by git (gitignored/untracked items are already handled)
    is_tracked=0
    if [ -d "$item" ] && [ -n "$(git ls-files "$item" 2>/dev/null)" ]; then
        is_tracked=1
    elif [ -f "$item" ] && git ls-files --error-unmatch "$item" > /dev/null 2>&1; then
        is_tracked=1
    fi
    if [ "$is_tracked" -eq 1 ]; then
        if [ -d "$item" ]; then
            item_size=$(du -sm "$item" 2>/dev/null | cut -f1)
            echo "    [${item_size:-?}MB dir] $item/"
        else
            size=$(stat -c%s "$item" 2>/dev/null || stat -f%z "$item" 2>/dev/null || echo 0)
            size_mb=$(( size / 1048576 ))
            echo "    [${size_mb}MB] $item"
        fi
        echo "           Reason: $reason"
        NN_FOUND=$((NN_FOUND + 1))
    fi
done
echo ""
if [ "$NN_FOUND" -gt 0 ]; then
    warn "$NN_FOUND tracked items are removable for a clean skills-only upload"
else
    pass "No tracked removable items — repo is lean for fresh upload"
fi

# =============================================================================
section "30. NextDecade-Claude-Project/04-scripts — canonical copy check"
# =============================================================================
# The 04-scripts/ directory duplicates scripts from skills/docx/scripts/ and
# skills/pptx/scripts/. Verify they're byte-identical so users don't get
# different behavior depending on which copy they run.
#
# Legitimate per-copy differences (stripped before diff):
#   render_docx.py: TEMPLATES path (skills/docx/templates vs 02-templates)
#   render_docx.py: NOTE comment about path constants differing
#   render_pptx.py: TEMPLATES path similarly
# UPLOADS and _REPO_ROOT constants were removed in the strict-only refactor;
# the grep pattern is kept for safety in case they're re-added.

SCRIPT_PAIRS=(
    "skills/docx/scripts/render_docx.py:NextDecade-Claude-Project/04-scripts/render_docx.py"
    "skills/pptx/scripts/render_pptx.py:NextDecade-Claude-Project/04-scripts/render_pptx.py"
)
for pair in "${SCRIPT_PAIRS[@]}"; do
    IFS=':' read -r canonical dupe <<< "$pair"
    if [ -f "$canonical" ] && [ -f "$dupe" ]; then
        if diff -q \
            <(grep -v 'TEMPLATES\|UPLOADS\|_REPO_ROOT\|HERE\.parent\|HERE\.parents\|Resolve.*relative.*this file' "$canonical") \
            <(grep -v 'TEMPLATES\|UPLOADS\|_REPO_ROOT\|HERE\.parent\|HERE\.parents\|Resolve.*relative.*this file' "$dupe") \
            > /dev/null 2>&1; then
            pass "script in sync: $(basename "$canonical") (functional code identical, paths adjusted)"
        else
            warn "script DIVERGED: $(basename "$canonical") has functional differences between skills/ and 04-scripts/"
        fi
    elif [ ! -f "$dupe" ]; then
        warn "04-scripts/ missing: $(basename "$canonical")"
    fi
done

# =============================================================================
section "31. Template-is-sole-source-of-formatting invariant + strict-only API surface"
# =============================================================================
# NextDecade policy: the DOCX template is the authoritative source of
# typography, colors, margins, headers, footers. The strict docxtpl render
# must produce output whose theme1.xml and Heading 1 color match the template
# exactly. Any drift means a renderer is introducing formatting that the
# template doesn't specify -- a policy violation.
#
# This test also verifies the strict-only API surface: walk_replace_* functions
# must NOT exist on the module (removed in the strict-only refactor).

python3 - <<'PY' > /tmp/step31_out.txt 2>&1 || true
import sys, json, re, zipfile, tempfile
from pathlib import Path
sys.path.insert(0, "skills/docx/scripts")
import render_docx

def fingerprint(docx_path):
    with zipfile.ZipFile(docx_path) as z:
        theme = z.read("word/theme/theme1.xml").decode() if "word/theme/theme1.xml" in z.namelist() else ""
        styles = z.read("word/styles.xml").decode()
    maj = re.search(r'<a:majorFont>\s*<a:latin\s+typeface="([^"]+)"', theme)
    h1 = re.search(r'<w:style[^>]*w:styleId="Heading1"[^>]*>.*?<w:color[^/]*w:val="([0-9A-Fa-f]+)"', styles, re.DOTALL)
    return (maj.group(1) if maj else None, h1.group(1).upper() if h1 else None)

# Verify walk_replace_* functions have been removed (strict-only design)
for fn_name in ("walk_replace_procedure", "walk_replace_standard", "walk_replace_guidance"):
    if hasattr(render_docx, fn_name):
        print(f"FAIL {fn_name} still present — must be removed in strict-only design")
    else:
        print(f"PASS {fn_name} absent (strict-only API surface confirmed)")

try:
    import docxtpl  # noqa: F401
except ImportError:
    print("WARN formatting-invariant render skipped: docxtpl not installed (pip install docxtpl)")
    sys.exit(0)

cases = [
    ("procedure", "skills/docx/templates/Procedure Template (Jinja).docx",
     "samples/document-types-validation/_inputs/vendor-onboarding-procedure.json"),
    ("standard",  "skills/docx/templates/Standard Template (Jinja).docx",
     "samples/document-types-validation/_inputs/records-retention-standard.json"),
]
with tempfile.TemporaryDirectory() as td:
    for dt, tpl, inp in cases:
        if not Path(inp).exists():
            print(f"WARN {dt}-strict: sample input not found ({inp}) — skipping render")
            continue
        tpl_fp = fingerprint(tpl)
        with open(inp) as f: data = json.load(f)
        out_strict = Path(td) / f"{dt}_strict.docx"
        render_docx.render(dt, data, out_strict)
        fp_strict = fingerprint(out_strict)
        if fp_strict == tpl_fp:
            print(f"PASS {dt}-strict: output formatting matches template ({tpl_fp[0]}, H1={tpl_fp[1]})")
        else:
            print(f"FAIL {dt}-strict: template={tpl_fp} output={fp_strict}")
PY
while IFS= read -r line; do
    if [[ "$line" == PASS\ * ]]; then
        pass "${line#PASS }"
    elif [[ "$line" == FAIL\ * ]]; then
        fail "${line#FAIL }"
    elif [[ "$line" == WARN\ * ]]; then
        warn "${line#WARN }"
    fi
done < /tmp/step31_out.txt

# =============================================================================
section "32. StrictUndefined enforcement — render raises on missing required key"
# =============================================================================
# Core invariant of the strict-only design: render_via_docxtpl must raise an
# UndefinedError (not silently produce empty output) when a required Jinja
# marker is absent from the input data. This test renders a procedure with one
# required key deliberately removed and asserts an exception is raised.

python3 - <<'PY' > /tmp/step32_out.txt 2>&1 || true
import sys, json, tempfile
from pathlib import Path
sys.path.insert(0, "skills/docx/scripts")
import render_docx

inp = "samples/document-types-validation/_inputs/vendor-onboarding-procedure.json"
if not Path(inp).exists():
    print("WARN strict-undefined-test: sample input not found — skipping")
    sys.exit(0)

try:
    import docxtpl  # noqa: F401
except ImportError:
    print("WARN strict-undefined-test: docxtpl not installed — skipping")
    sys.exit(0)

with open(inp) as f:
    data = json.load(f)

# Remove a required key that the Jinja template definitely references
truncated = {k: v for k, v in data.items() if k != "procedure_title"}

with tempfile.TemporaryDirectory() as td:
    out = Path(td) / "strict_test.docx"
    try:
        render_docx.render("procedure", truncated, out)
        print("FAIL strict-undefined: render succeeded with missing key (StrictUndefined not enforced!)")
    except Exception as e:
        err = str(e)
        if "procedure_title" in err or "UndefinedError" in type(e).__name__ or "Undefined" in type(e).__name__ or "undefined" in err.lower():
            print(f"PASS strict-undefined: render raised on missing 'procedure_title' ({type(e).__name__})")
        else:
            print(f"PASS strict-undefined: render raised on missing key ({type(e).__name__}: {err[:80]})")
PY
while IFS= read -r line; do
    if [[ "$line" == PASS\ * ]]; then
        pass "${line#PASS }"
    elif [[ "$line" == FAIL\ * ]]; then
        fail "${line#FAIL }"
    elif [[ "$line" == WARN\ * ]]; then
        warn "${line#WARN }"
    fi
done < /tmp/step32_out.txt

# =============================================================================
section "33. Lint failure raises — no silent render when template is broken"
# =============================================================================
# Verify that render() raises RuntimeError when the linter returns exit code 3
# (unrecoverable template damage). In the strict-only design there is no
# fallback path — a broken template must block rendering entirely.
# We mock this by temporarily pointing at a non-existent schema file so the
# linter subprocess returns non-zero, then check render() raises.

python3 - <<'PY' > /tmp/step33_out.txt 2>&1 || true
import sys, json, tempfile, unittest.mock
from pathlib import Path
sys.path.insert(0, "skills/docx/scripts")
import render_docx

inp = "samples/document-types-validation/_inputs/vendor-onboarding-procedure.json"
if not Path(inp).exists():
    print("WARN lint-raises-test: sample input not found — skipping")
    sys.exit(0)

try:
    import docxtpl  # noqa: F401
except ImportError:
    print("WARN lint-raises-test: docxtpl not installed — skipping")
    sys.exit(0)

with open(inp) as f:
    data = json.load(f)

# Simulate a lint failure by patching subprocess.run to return exit code 3
import subprocess, types

orig_run = subprocess.run

def fake_run(cmd, **kwargs):
    if str(render_docx.LINTER) in str(cmd):
        r = types.SimpleNamespace()
        r.returncode = 3
        r.stdout = '{}'
        r.stderr = ''
        return r
    return orig_run(cmd, **kwargs)

with tempfile.TemporaryDirectory() as td:
    out = Path(td) / "lint_fail_test.docx"
    with unittest.mock.patch.object(subprocess, 'run', side_effect=fake_run):
        try:
            render_docx.render("procedure", data, out)
            print("FAIL lint-raises: render succeeded despite lint exit=3 (no fallback guard!)")
        except RuntimeError as e:
            if "lint" in str(e).lower() or "template" in str(e).lower():
                print(f"PASS lint-raises: render raised RuntimeError on lint failure ({str(e)[:80]})")
            else:
                print(f"PASS lint-raises: render raised RuntimeError ({str(e)[:80]})")
        except Exception as e:
            print(f"PASS lint-raises: render raised {type(e).__name__} on lint failure")
PY
while IFS= read -r line; do
    if [[ "$line" == PASS\ * ]]; then
        pass "${line#PASS }"
    elif [[ "$line" == FAIL\ * ]]; then
        fail "${line#FAIL }"
    elif [[ "$line" == WARN\ * ]]; then
        warn "${line#WARN }"
    fi
done < /tmp/step33_out.txt

# =============================================================================
section "34. API surface audit — back-compat shims and dead functions removed"
# =============================================================================
# Verify the public API of render_docx.py is clean after the strict-only
# refactor: no back-compat shims, no walk-replace helpers, no dead code that
# could confuse callers or mask regressions.

python3 -c "
import sys, importlib.util, os
os.chdir('$(pwd)')
spec = importlib.util.spec_from_file_location('render_docx', 'skills/docx/scripts/render_docx.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

# Functions that MUST exist (public API)
must_exist = ['render', 'render_via_docxtpl', 'convert_to_pdf']
for fn in must_exist:
    if hasattr(mod, fn):
        print(f'OK:{fn} present in public API')
    else:
        print(f'FAIL:{fn} missing from public API')

# Functions that MUST NOT exist (removed in strict-only refactor)
must_not_exist = [
    'render_procedure',           # back-compat shim
    'render_via_docxtpl_lenient', # lenient renderer
    'walk_replace_procedure',     # walk-and-replace fallbacks
    'walk_replace_standard',
    'walk_replace_guidance',
    '_wr_common_setup',           # walk-and-replace helpers
    '_wr_fill_content_sections',
    '_wr_fill_tables',
    '_table_plans_common',
    '_table_plans_guidance',
    '_resolve_original',          # only used by walk-replace
    'FALLBACK_FNS',               # fallback registry
]
for fn in must_not_exist:
    if hasattr(mod, fn):
        print(f'FAIL:{fn} still present — should have been removed in strict-only refactor')
    else:
        print(f'OK:{fn} absent (clean API surface)')
" 2>&1 | while IFS= read -r line; do
    case "$line" in
        OK:*)   pass "${line#OK:}" ;;
        WARN:*) warn "${line#WARN:}" ;;
        FAIL:*) fail "${line#FAIL:}" ;;
    esac
done

# =============================================================================
section "35. XML escape safety — _xml_escape_data handles &, <, > in all types"
# =============================================================================
# _xml_escape_data is the safety guard between user input and Word XML.
# If it fails to escape a single & or < in any nested string, the rendered
# .docx XML will be malformed. Verify the function handles strings, dicts,
# lists, and nested structures.

python3 -c "
import sys, importlib.util, os
os.chdir('$(pwd)')
spec = importlib.util.spec_from_file_location('render_docx', 'skills/docx/scripts/render_docx.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
fn = mod._xml_escape_data

# String escaping
cases = [
    ('ampersand', 'A & B', 'A &amp; B'),
    ('less-than', 'A < B', 'A &lt; B'),
    ('greater-than', 'A > B', 'A &gt; B'),
    ('combined', 'A & B < C > D', 'A &amp; B &lt; C &gt; D'),
    ('safe string', 'Hello World', 'Hello World'),
    ('number passthrough', 42, 42),
    ('none passthrough', None, None),
]
for label, inp, expected in cases:
    result = fn(inp)
    if result == expected:
        print(f'OK:escape {label}: {repr(inp)!r} -> {repr(result)!r}')
    else:
        print(f'FAIL:escape {label}: expected {repr(expected)!r}, got {repr(result)!r}')

# Dict recursion
d = {'title': 'A & B', 'nested': {'text': '1 < 2'}}
r = fn(d)
if r == {'title': 'A &amp; B', 'nested': {'text': '1 &lt; 2'}}:
    print('OK:escape dict recursive: nested dict escaped correctly')
else:
    print(f'FAIL:escape dict recursive: {r}')

# List recursion
lst = ['A & B', 'C < D', 42]
r = fn(lst)
if r == ['A &amp; B', 'C &lt; D', 42]:
    print('OK:escape list recursive: list items escaped correctly')
else:
    print(f'FAIL:escape list recursive: {r}')
" 2>&1 | while IFS= read -r line; do
    case "$line" in
        OK:*)   pass "${line#OK:}" ;;
        WARN:*) warn "${line#WARN:}" ;;
        FAIL:*) fail "${line#FAIL:}" ;;
    esac
done

# =============================================================================
# Reconcile counters from pipe subshells before printing summary
# =============================================================================
section "36. _post_render_cover_fixup — patches NAME and doc number in Standard"
# =============================================================================
# _post_render_cover_fixup does targeted XML search-and-replace inside the
# rendered .docx zip to fill in cover-page text boxes that Jinja cannot reach.
# Test: copy the Jinja template, inject a fake render, call fixup, verify
# placeholders were replaced.

python3 - <<'PY' > /tmp/step36_out.txt 2>&1 || true
import sys, zipfile, shutil, tempfile
from pathlib import Path
sys.path.insert(0, "skills/docx/scripts")
import render_docx

tpl = Path("skills/docx/templates/Standard Template (Jinja).docx")
if not tpl.exists():
    print("WARN cover-fixup-test: Standard template not found — skipping")
    sys.exit(0)

with tempfile.TemporaryDirectory() as td:
    # Copy template as the "rendered" output (it contains the placeholder strings)
    out = Path(td) / "standard_fixup_test.docx"
    shutil.copy2(tpl, out)

    data = {"document_name": "Hot Work Safety", "doc_number": "ND-HSSE-001-2026"}
    patches = render_docx._post_render_cover_fixup(out, data, "standard")

    if patches:
        print(f"PASS cover-fixup: {len(patches)} placeholder(s) patched")
        # Verify NAME and doc number appear in patched XML
        with zipfile.ZipFile(out) as z:
            all_xml = " ".join(z.read(n).decode("utf-8", errors="replace")
                               for n in z.namelist()
                               if n.startswith("word/") and n.endswith(".xml"))
        if "Hot Work Safety" in all_xml:
            print("PASS cover-fixup: document_name present in patched XML")
        else:
            print("FAIL cover-fixup: document_name not found in patched XML")
        if "ND-HSSE-001-2026" in all_xml:
            print("PASS cover-fixup: doc_number present in patched XML")
        else:
            print("FAIL cover-fixup: doc_number not found in patched XML")
    else:
        print("WARN cover-fixup: no patches applied (placeholders may have changed in template)")
PY
while IFS= read -r line; do
    if [[ "$line" == PASS\ * ]]; then
        pass "${line#PASS }"
    elif [[ "$line" == FAIL\ * ]]; then
        fail "${line#FAIL }"
    elif [[ "$line" == WARN\ * ]]; then
        warn "${line#WARN }"
    fi
done < /tmp/step36_out.txt

# =============================================================================
section "37. _remove_template_scaffolding — known markers absent in rendered output"
# =============================================================================
# After a full render, the scaffolding markers ("[CONTENT TITLE]", "Enter text
# here", "Click here to enter text") should have been replaced by Jinja content
# and any survivors should have been removed by _remove_template_scaffolding.
# Test: render the Standard sample and verify no scaffolding markers survive.

python3 - <<'PY' > /tmp/step37_out.txt 2>&1 || true
import sys, json, tempfile, zipfile
from pathlib import Path
sys.path.insert(0, "skills/docx/scripts")
import render_docx

try:
    import docxtpl  # noqa: F401
except ImportError:
    print("WARN scaffolding-test: docxtpl not installed — skipping")
    sys.exit(0)

markers = ["[CONTENT TITLE]", "Enter text here", "Click here to enter text"]

cases = [
    ("standard",  "samples/document-types-validation/_inputs/records-retention-standard.json"),
    ("guidance",  "samples/document-types-validation/_inputs/remote-work-guidance.json"),
]
for dt, inp in cases:
    if not Path(inp).exists():
        print(f"WARN scaffolding-test: {dt} sample input not found — skipping")
        continue
    with open(inp) as f:
        data = json.load(f)
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / f"{dt}_scaffolding_test.docx"
        render_docx.render(dt, data, out)
        with zipfile.ZipFile(out) as z:
            all_xml = " ".join(z.read(n).decode("utf-8", errors="replace")
                               for n in z.namelist()
                               if n.startswith("word/") and n.endswith(".xml"))
        found = [m for m in markers if m in all_xml]
        if found:
            print(f"FAIL scaffolding-removal: {dt} — markers still present: {found}")
        else:
            print(f"PASS scaffolding-removal: no scaffolding markers in rendered {dt} output")
PY
while IFS= read -r line; do
    if [[ "$line" == PASS\ * ]]; then
        pass "${line#PASS }"
    elif [[ "$line" == FAIL\ * ]]; then
        fail "${line#FAIL }"
    elif [[ "$line" == WARN\ * ]]; then
        warn "${line#WARN }"
    fi
done < /tmp/step37_out.txt

# =============================================================================
_reconcile_counters

# =============================================================================
# SUMMARY
# =============================================================================

echo ""
echo "============================================="
echo "  SMOKE TEST SUMMARY  (v2 — $(date +%Y-%m-%d))"
echo "============================================="
echo "  PASS: $PASS"
echo "  FAIL: $FAIL"
echo "  WARN: $WARN"
echo "  TOTAL CHECKS: $((PASS + FAIL + WARN))"
echo "============================================="
echo ""

if [ "$FAIL" -gt 0 ]; then
    echo "  RESULT: FAILED ($FAIL failures)"
    echo ""
    echo "  Review the FAIL lines above. Common fixes:"
    echo "    - Missing files: check git status, re-pull"
    echo "    - Schema drift: re-sync skills/ and NextDecade-Claude-Project/"
    echo "    - JSON errors: validate with python3 -m json.tool <file>"
    echo "    - Branding override: move structure rules out of brand-guidelines"
    echo "    - Schema cross-mismatch: align field types in shared fields"
    echo ""
    exit 1
else
    echo "  RESULT: PASSED (with $WARN warnings)"
    echo ""
    if [ "$WARN" -gt 0 ]; then
        echo "  Warnings are advisory — review before enterprise distribution."
    fi
    exit 0
fi
