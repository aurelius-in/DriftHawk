#!/usr/bin/env bash
set -euo pipefail

echo "Expect OPA to block :latest images..."
conftest test redteam/rollout/bad_overlay.yaml -p policy/opa && { echo "ERROR: policy allowed bad overlay"; exit 1; } || echo "OK: policy blocked"

echo "Unsigned image list (manual check in CI step):"
cat redteam/supply_chain/unsigned_images.txt

mkdir -p redteam/reports/$(date +%F)
echo "# Red-Team Report $(date +%F)" > redteam/reports/$(date +%F)/infra-chaos.md


