SHELL := /bin/bash
ENV ?= dev

init:
	python -V >/dev/null || true

policy.test:
	conftest test gitops/rollouts/ops-bot.yaml -p policy/opa

policy.test.dev:
	conftest test gitops/overlays/dev -p policy/opa

policy.test.staging:
	conftest test gitops/overlays/staging -p policy/opa

policy.test.prod:
	conftest test gitops/overlays/prod -p policy/opa

tf.plan:
	cd terraform/envs/$(ENV) && terraform init -input=false && terraform plan -out=tfplan && terraform show -json tfplan > ../../artifacts/plan.json

tf.fmt:
	terraform -chdir=terraform/envs/$(ENV) fmt -recursive

tf.validate:
	terraform -chdir=terraform/envs/$(ENV) init -input=false && terraform -chdir=terraform/envs/$(ENV) validate

k8s.validate:
	kubeconform -strict -summary -ignore-missing-schemas gitops/**/*.yaml

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

lint.py:
	flake8 ops_bot

test.bot:
	pytest -q

compose.up:
	docker compose up -d

compose.down:
	docker compose down


