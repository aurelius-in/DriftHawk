SHELL := /bin/bash
ENV ?= dev

init:
	python -V >/dev/null || true

policy.test:
	conftest test gitops/rollouts/ops-bot.yaml -p policy/opa

tf.plan:
	cd terraform/envs/$(ENV) && terraform init -input=false && terraform plan -out=tfplan && terraform show -json tfplan > ../../artifacts/plan.json

tf.plan.dev:
	$(MAKE) tf.plan ENV=dev

tf.plan.staging:
	$(MAKE) tf.plan ENV=staging

tf.plan.prod:
	$(MAKE) tf.plan ENV=prod

api.openapi:
	curl -s http://localhost:8080/openapi.json > artifacts/openapi.json

brief:
	curl -s -X POST localhost:8080/chatops/plan-brief -H 'Content-Type: application/json' -d '{"env":"$(ENV)"}' | jq

argo.sync:
	kubectl apply -f gitops/apps/drifthawk.yaml

graph:
	bash tools/graph/graph.sh $(ENV)

graph.win:
	powershell -ExecutionPolicy Bypass -File tools/graph/graph.ps1 -Env $(ENV)

redteam.run:
	bash redteam/run_redteam.sh

drift.run:
	bash ops_bot/jobs/drift_scout.sh

run.bot:
	bash ops_bot/run.sh

compose.up:
	docker compose up -d

compose.down:
	docker compose down


