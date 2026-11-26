#!/usr/bin/env bash
# Rebuild the published book after a push, for .github/workflows/build-book.yml.
#
# Usage: tools/markdown/ci-build.sh [BEFORE_SHA]
#   BEFORE_SHA: the commit before the push (empty or all zeros for a manual run).
#
# 1. If book/book.json does not name Markdown as the source of truth, do nothing.
# 2. If the committed pages already match a fresh build, do nothing.
# 3. If the push itself changed a fully built page (search-textbook.html,
#    read-this-first.html, vendor-questionnaire.html) and that page does not
#    match a fresh build, stop with an error rather than overwrite what looks
#    like a hand edit: the change belongs in book/.
# 4. Otherwise rebuild in place, check the result, and make sure only the pages
#    a build may write have changed. Committing is left to the workflow.
#
# Writes changed=true|false to $GITHUB_OUTPUT when it is set.
set -euo pipefail

PY="${PYTHON:-python}"
BUILT=(search-textbook.html read-this-first.html vendor-questionnaire.html)
WRITABLE='^ M (search-textbook|read-this-first|vendor-questionnaire|teaching-notes)\.html$'
before="${1:-}"
output() { if [ -n "${GITHUB_OUTPUT:-}" ]; then echo "changed=$1" >> "$GITHUB_OUTPUT"; fi; }

truth=$("$PY" -c 'import json; print(json.load(open("book/book.json"))["source_of_truth"])')
if [ "$truth" != "markdown" ]; then
  echo "book/book.json names \"$truth\" as the source of truth; nothing to build."
  output false
  exit 0
fi

log=$(mktemp)
if "$PY" tools/build-book.py --check > "$log" 2>&1; then
  echo "The committed pages already match a fresh build of book/."
  output false
  exit 0
fi

if [[ -n "$before" && ! "$before" =~ ^0+$ ]] && ! git diff --quiet "$before" HEAD -- "${BUILT[@]}"; then
  cat "$log"
  echo "::error::This push changed a built page directly, and it no longer matches a build of book/." \
       "Make the change in the Markdown under book/ instead (a rebuild would discard it), or run" \
       "python tools/build-book.py and commit the result."
  output false
  exit 1
fi

"$PY" tools/build-book.py
"$PY" tools/build-book.py --check

unexpected=$(git status --porcelain | grep -Ev "$WRITABLE" || true)
if [ -n "$unexpected" ]; then
  echo "::error::The build changed files it should not write:"
  echo "$unexpected"
  output false
  exit 1
fi
echo "Rebuilt: $(git status --porcelain | awk '{print $2}' | tr '\n' ' ')"
output true
