.DEFAULT_GOAL := help

BRAIN_DIR := brain
WEB_DIR   := web
DEPLOY_DIR := deploy
UV        := $(shell command -v uv 2>/dev/null || echo uv)
BUN       := $(shell command -v bun 2>/dev/null || echo bun)

.PHONY: help init check test dev-brain dev-web deploy push push-tags status log

help: ## Show targets
	@grep -E '^[a-zA-Z_-]+:.*?##' $(MAKEFILE_LIST) | \
	  awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

init: ## Copy .env.example and deploy override example
	@test -f .env || cp .env.example .env
	@test -f $(DEPLOY_DIR)/docker-compose.override.yml || \
	  cp $(DEPLOY_DIR)/docker-compose.override.example.yml $(DEPLOY_DIR)/docker-compose.override.yml
	@echo "Edit .env (bw-env) then: make dev-brain / make dev-web"

check: test ## Brain tests + web typecheck
	@cd $(WEB_DIR) && $(BUN) run typecheck

test: ## Run brain pytest
	@cd $(BRAIN_DIR) && $(UV) sync --group dev
	@cd $(BRAIN_DIR) && $(UV) run pytest -q

dev-brain: ## Run brain API on :8000
	@cd $(BRAIN_DIR) && $(UV) sync --group dev
	@cd $(BRAIN_DIR) && $(UV) run uvicorn live_brain.main:app --reload --host 0.0.0.0 --port 8000

dev-web: ## Run Vite dev server on :5173
	@cd $(WEB_DIR) && $(BUN) install
	@cd $(WEB_DIR) && $(BUN) run dev

deploy: ## Build and start stack locally (deploy/)
	@cd $(DEPLOY_DIR) && docker compose -p live up -d --build

down: ## Stop local deploy stack
	@cd $(DEPLOY_DIR) && docker compose -p live down

log: ## Follow deploy logs
	@cd $(DEPLOY_DIR) && docker compose -p live logs -f

push: ## Push current branch to all remotes (github + gitlab)
	@branch="$$(git branch --show-current)"; \
	git remote | xargs -I{} sh -c 'echo "==> pushing '"$$branch"' to {}"; git push {} '"$$branch"'"

push-tags: ## Push tags to all remotes
	@git remote | xargs -I{} git push {} --tags

status: ## git status --short
	@git status --short

log-git: ## Last 10 commits
	@git log --oneline -10
