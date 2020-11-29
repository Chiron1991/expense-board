rs:
	python manage.py runserver --nostatic

mg:
	python manage.py migrate

mmg:
	python manage.py makemigrations

sh:
	python manage.py shell_plus

init_dev:
	git config core.hooksPath githooks
	poetry install

export_poetry_lockfile:
	poetry export -f requirements.txt --output requirements.txt
	poetry export --dev -f requirements.txt --output requirements-dev.txt
