build:
	docker build -f deploy/local/Dockerfile -t fruits/service .

build.base:
	docker build -f deploy/base/Dockerfile -t fruits/service-base .

push.base:
	docker tag fruits/service-base registry.yandex-academy.ru/school/2022-06/backend/python/homeworks/hw3-search/fruits/service-base:latest
	docker push registry.yandex-academy.ru/school/2022-06/backend/python/homeworks/hw3-search/fruits/service-base:latest

build.ci:
	docker build -f deploy/ci/Dockerfile -t fruits/service-ci .

build.postgres:
	docker build --no-cache -f deploy/postgres/Dockerfile -t fruits/store .

push.postgres:
	docker tag fruits/store registry.yandex-academy.ru/school/2022-06/backend/python/homeworks/hw3-search/fruits/store:latest
	docker push registry.yandex-academy.ru/school/2022-06/backend/python/homeworks/hw3-search/fruits/store:latest

run.postgres:
	docker run --name store -e POSTGRES_USER=user -e POSTGRES_PASSWORD=random -e POSTGRES_DB=homework -p 5432:5432 registry.yandex-academy.ru/school/2022-06/backend/python/homeworks/hw3-search/fruits/store

up:
	docker-compose up -d  

down:
	docker-compose down

migrate:
	docker-compose exec service python manage.py migrate

fill:
	docker-compose exec service python manage.py fill

create_db:
	docker-compose exec store psql "user=user password=random" -c "create database homework WITH ENCODING 'UTF8' LC_COLLATE = 'en_US.utf8' LC_CTYPE = 'en_US.utf8';"

restore_db:
	docker-compose exec -t store psql "dbname=homework user=user password=random" <dump.sql

dump_db:
	docker-compose exec -T store pg_dump "dbname=homework user=user password=random" >dump.sql

drop_db:
	docker-compose exec store psql "user=user password=random" -c "drop database homework;"

psql:
	docker-compose exec store psql "dbname=homework user=user password=random"

shell:
	docker-compose exec service python manage.py shell

logs:
	docker-compose logs -f

test:
	docker-compose exec service pytest --durations=0
