#!/usr/bin/env bash
set -euo pipefail

ENV="${1:-dev}"
pushd "terraform/envs/${ENV}" >/dev/null
terraform init -input=false -upgrade
terraform graph | dot -Tpng > "../../../artifacts/${ENV}-graph.png"
echo "wrote artifacts/${ENV}-graph.png"
popd >/dev/null


