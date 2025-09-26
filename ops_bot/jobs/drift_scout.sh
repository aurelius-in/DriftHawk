#!/usr/bin/env bash
set -euo pipefail

cd terraform/envs/prod
terraform init -input=false
terraform plan -refresh-only -no-color -out=tfplan | tee /tmp/refresh.txt || true
terraform show -no-color tfplan >> /tmp/refresh.txt || true
if grep -Eqi "(replace|update|destroy)" /tmp/refresh.txt; then
  branch="fix/drift-$(date +%F)"
  git checkout -b "$branch"
  git commit --allow-empty -m "Drift: $(date +%F)"
  gh pr create --title "Drift remediation $(date +%F)" --body "Auto-PR from Drift Scout"
fi


