FROM registry.yandex-academy.ru/school/2022-06/backend/python/homeworks/hw3-search/fruits/service-base:latest

RUN mkdir /$app/solution

ADD src /$app
ADD solution /$app/solution

CMD python manage.py migrate
CMD python manage.py runserver 0.0.0.0:8000
