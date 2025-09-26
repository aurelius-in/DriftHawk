#!/usr/bin/env bash
set -euo pipefail

cd terraform/envs/prod
terraform init -input=false
terraform plan -refresh-only -no-color -out=tfplan | tee /tmp/refresh.txt || true
terraform show -no-color tfplan >> /tmp/refresh.txt || true
if grep -Eqi "(replace|update|destroy)" /tmp/refresh.txt; then
  gh issue create --title "Drift detected $(date +%F)" --body "See drift output in /tmp/refresh.txt. Please address on develop branch." || true
fi


