
.PHONY: dev
dev: docker-up backend frontend


.PHONY: docker-up
docker-up:
	docker-compose -f docker-compose.dev.yml up -d


.PHONY: backend
backend:
	cd backend && source .venv/Scripts/activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000


.PHONY: frontend
frontend:
	cd frontend && npm run dev


.PHONY: docker-down
docker-down:
	docker compose -f docker-compose.dev.yml down
