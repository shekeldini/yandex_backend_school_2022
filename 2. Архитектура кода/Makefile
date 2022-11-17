TEST = poetry run python -m pytest --verbosity=2 --showlocals --log-level=DEBUG
CODE = shortener tests


db:
	cd database/postgresql-docker-image && docker-compose up -d --remove-orphans

migrate:
	cd shortener/db && alembic upgrade head

run:
	uvicorn app.__main__:app --reload --port=8080

revision:
	cd shortener/db && alembic revision --autogenerate

open_db:
	docker exec -it database psql -U student -W pharmacy

