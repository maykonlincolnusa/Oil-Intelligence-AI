SHELL := /bin/bash

.PHONY: setup dev up backend frontend down logs test lint backend-test backend-lint frontend-lint frontend-typecheck seed

setup:
	cp .env.example .env || true

dev: up

up:
	docker compose up --build

backend:
	cd apps/api && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

frontend:
	cd apps/web && npm run dev

down:
	docker compose down

logs:
	docker compose logs -f

test: backend-test

lint: backend-lint frontend-lint frontend-typecheck

backend-test:
	cd apps/api && pytest -q

backend-lint:
	cd apps/api && ruff check .

frontend-lint:
	cd apps/web && npm run lint

frontend-typecheck:
	cd apps/web && npx tsc --noEmit

seed:
	cd apps/api && python -m app.seed
