revision:
	poetry run alembic revision --autogenerate

upgrade:
	poetry run alembic upgrade head

install:
	poetry install

dev: install
	docker-compose -f docker/docker-compose-dev.yml --project-directory . up --build -d;
	poetry run uvicorn app.api.main:app --host 0.0.0.0 --port 10000 --reload

deploy:
	docker-compose -f docker/docker-compose.yml --project-directory . up --build -d
