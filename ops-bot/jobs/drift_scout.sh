#!/usr/bin/env bash
set -euo pipefail

cd terraform/envs/prod
terraform init -input=false
terraform refresh -no-color | tee /tmp/refresh.txt
if grep -Eqi "will be (replaced|updated|destroyed)" /tmp/refresh.txt; then
  branch="fix/drift-$(date +%F)"
  git checkout -b "$branch"
  git commit --allow-empty -m "Drift: $(date +%F)"
  gh pr create --title "Drift remediation $(date +%F)" --body "Auto-PR from Drift Scout"
fi


