SHELL := /bin/bash
ENV ?= dev

init:
	python -V >/dev/null || true

policy.test:
	conftest test gitops/rollouts/ops-bot.yaml -p policy/opa

tf.plan:
	cd terraform/envs/$(ENV) && terraform init -input=false && terraform plan -out=tfplan && terraform show -json tfplan > ../../artifacts/plan.json

brief:
	curl -s -X POST localhost:8080/chatops/plan-brief -H 'Content-Type: application/json' -d '{"env":"$(ENV)"}' | jq

argo.sync:
	kubectl apply -f gitops/apps/drifthawk.yaml

graph:
	bash tools/graph/graph.sh $(ENV)

redteam.run:
	bash redteam/run_redteam.sh

drift.run:
	bash ops-bot/jobs/drift_scout.sh

run.bot:
	bash ops-bot/run.sh


