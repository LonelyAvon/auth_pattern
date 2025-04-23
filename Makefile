revision:
	poetry run alembic revision --autogenerate

upgrade:
	poetry run alembic upgrade head

install:
	poetry install

db:
	docker compose --env-file .env.develop -f docker/docker-compose-dev.yml --project-directory . up --build -d

dev: install db
	poetry run uvicorn app.api.main:app --host 0.0.0.0 --port 4001 --reload

deploy:
	docker compose --env-file .env.deploy -f docker/docker-compose.yml --project-directory . up --build -d