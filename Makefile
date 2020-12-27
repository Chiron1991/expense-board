rs:
	python manage.py runserver --nostatic

mg:
	python manage.py migrate

mmg:
	python manage.py makemigrations

sh:
	python manage.py shell_plus

lint:
	sh -c "flake8 ."
	sh -c "isort --check-only ."

test:
	python manage.py test

test_cov:
	coverage run
	coverage html

dbuild:
	docker build . --pull -t chiron1991/expense-board:latest

init_dev:
	poetry install
	rm -f db.sqlite3 || true
	poetry run python manage.py migrate
	poetry run python manage.py createsuperuser
	poetry run python manage.py seed_data

requirements:
	poetry export -f requirements.txt --output requirements.txt
	poetry export --dev -f requirements.txt --output requirements-dev.txt
