TEST = poetry run python -m pytest --verbosity=2 --showlocals --log-level=DEBUG
CODE = shortener tests

all:
	@echo "make lint		- Check code with pylint"
	@echo "make format		- Reformat code with isort and black"
	@echo "make migrate		- Do all migrations in database"
	@echo "make revision	- Create new revision automatically"
	@echo "make test		- Test application with pytest"
	@echo "make test-cov	- Test application with pytest and create coverage report"
	@exit 0

clean:
	rm -fr *.egg-info dist

db:
	docker-compose -f docker-compose.yml up -d --remove-orphans

lint:
	pylint $(CODE)

format:
	isort $(CODE)
	black $(CODE)

migrate:
	cd shortener/db && alembic upgrade head

run:
	uvicorn shortener.__main__:app --reload --port=8080

revision:
	cd shortener/db && alembic revision --autogenerate

open_db:
	docker exec -it ya-url-shortener-for-viplink_db_1 psql -U user -W shortener

test:
	make db && $(TEST)

test-cov:
	make db && $(TEST) --cov=shortener
