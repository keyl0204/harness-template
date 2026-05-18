#!/usr/bin/env bash
set -euo pipefail

test -f AGENTS.md
test -d .harness
test -d docs
test -f .harness/rules/doc-boundary-rules.md
if test -f .harness/scripts/harness-check.py; then
  python -B .harness/scripts/harness-check.py
fi

echo "Harness 预检查通过"
