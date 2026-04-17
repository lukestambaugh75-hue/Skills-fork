#!/usr/bin/env bash
# Build "Claude Project knowledge bundle.zip" from the ClaudeProjectBundle/ folder.
# Output is in .gitignore'd by the repo's global *.zip rule, so it stays local.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"
OUT="Claude Project knowledge bundle.zip"
rm -f "$OUT"
cd ClaudeProjectBundle
zip -rq "../$OUT" .
cd ..
ls -lh "$OUT"
