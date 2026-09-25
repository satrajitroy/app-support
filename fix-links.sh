#!/usr/bin/env bash
set -euo pipefail

DIR="schedules/childcare"

echo "Before:"
grep -Rni 'href="privacy.html"' "$DIR" || true

grep -rl 'href="privacy.html"' "$DIR" \
  | while IFS= read -r f; do
      sed -i '' 's#href="privacy.html"#href="../../privacy/"#g' "$f"
      echo "fixed: $f"
    done

echo
echo "After:"
grep -Rni 'href="privacy.html"' "$DIR" || true

echo
echo "Current privacy links:"
grep -Rni 'privacy/' "$DIR" || true
