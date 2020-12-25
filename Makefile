rs:
	python manage.py runserver --nostatic

mg:
	python manage.py migrate

mmg:
	python manage.py makemigrations

sh:
	python manage.py shell_plus

test:
	python manage.py test

init_dev:
	poetry install
	rm -f db.sqlite3 || true
	poetry run python manage.py migrate
	poetry run python manage.py createsuperuser
	poetry run python manage.py seed_data
	$(MAKE) rs

export_poetry_lockfile:
	poetry export -f requirements.txt --output requirements.txt
	poetry export --dev -f requirements.txt --output requirements-dev.txt
