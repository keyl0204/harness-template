#!/usr/bin/env bash
set -euo pipefail

test -f AGENTS.md
test -d .harness
test -d docs
test -f .harness/rules/doc-boundary-rules.md

echo "Harness 预检查通过"
