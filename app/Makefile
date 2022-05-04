all: migrate static run

.PHONY: migrate
migrate:
	python manage.py migrate --no-input

.PHONY: static
static:
	python manage.py collectstatic --no-input

.PHONY: run
run:
	python manage.py runserver 0.0.0.0:8000

.PHONY: createsuperuser
createsuperuser:
	python manage.py createsuperuser