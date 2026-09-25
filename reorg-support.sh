#!/usr/bin/env bash
set -euo pipefail

mkdir -p schedules/childcare
mkdir -p puzzles/sudoku
mkdir -p puzzles/word-search
mkdir -p puzzles/polyomino
mkdir -p privacy

git mv user-manual.html schedules/childcare/
git mv user-manual.md schedules/childcare/

git mv testflight-quickstart.html schedules/childcare/
git mv testflight-quickstart.md schedules/childcare/

git mv technical-integration-brief.html schedules/childcare/
git mv technical-integration-brief.md schedules/childcare/

git mv support.html schedules/childcare/support.html

# Keep privacy at top level for now.
# We'll replace/rework it into a generic policy next.
git mv privacy.html privacy/index.html

echo
echo "New structure:"
find schedules puzzles privacy -maxdepth 3 -type f | sort
