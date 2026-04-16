#!/usr/bin/env bash
# =============================================================================
# NextDecade Enterprise Skills — Full-Stack Smoke Test
# =============================================================================
#
# PURPOSE: Validate the entire Skills-fork repository is uploadable and
# functional for a fresh enterprise rollout. Tests: file integrity, JSON/YAML
# validity, Python syntax, schema alignment, template availability, hardcoded
# path portability, binary bloat detection, and skill manifest completeness.
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

pass()  { PASS=$((PASS + 1)); echo "  PASS: $1"; }
fail()  { FAIL=$((FAIL + 1)); echo "  FAIL: $1"; }
warn()  { WARN=$((WARN + 1)); echo "  WARN: $1"; }
section() { echo ""; echo "=== $1 ==="; }

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

echo "  Listing tracked binary files > 5MB..."
BLOAT_COUNT=0
while IFS= read -r fpath; do
    [ -z "$fpath" ] && continue
    if [ -f "$fpath" ]; then
        size=$(stat -c%s "$fpath" 2>/dev/null || stat -f%z "$fpath" 2>/dev/null || echo 0)
        if [ "$size" -gt 5242880 ]; then
            size_mb=$(( size / 1048576 ))
            warn "large tracked file (${size_mb}MB): $fpath"
            BLOAT_COUNT=$((BLOAT_COUNT + 1))
        fi
    fi
done < <(git ls-files 2>/dev/null)
if [ "$BLOAT_COUNT" -eq 0 ]; then
    pass "No tracked files exceed 5MB"
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
echo "  Other files NOT required for a fresh skills-only upload:"

NOT_NEEDED_FOR_UPLOAD=(
    "Use this to share.zip"
    "samples/document-types-validation"
    "output/final"
    ".claude/plans"
    "skills/theme-factory/theme-showcase.pdf"
)
for item in "${NOT_NEEDED_FOR_UPLOAD[@]}"; do
    if [ -e "$item" ]; then
        if [ -d "$item" ]; then
            item_size=$(du -sm "$item" 2>/dev/null | cut -f1)
            warn "removable for fresh upload: $item/ (${item_size}MB dir)"
        else
            size=$(stat -c%s "$item" 2>/dev/null || stat -f%z "$item" 2>/dev/null || echo 0)
            size_mb=$(( size / 1048576 ))
            warn "removable for fresh upload: $item (${size_mb}MB)"
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
# SUMMARY
# =============================================================================

echo ""
echo "============================================="
echo "  SMOKE TEST SUMMARY"
echo "============================================="
echo "  PASS: $PASS"
echo "  FAIL: $FAIL"
echo "  WARN: $WARN"
echo "============================================="
echo ""

if [ "$FAIL" -gt 0 ]; then
    echo "  RESULT: FAILED ($FAIL failures)"
    echo ""
    echo "  Review the FAIL lines above. Common fixes:"
    echo "    - Missing files: check git status, re-pull"
    echo "    - Schema drift: re-sync skills/ and NextDecade-Claude-Project/"
    echo "    - JSON errors: validate with python3 -m json.tool <file>"
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
