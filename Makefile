rs:
	python manage.py runserver

mg:
	python manage.py migrate

mmg:
	python manage.py makemigrations

sh:
	python manage.py shell_plus

init_dev:
	git config core.hooksPath .githooks
	poetry install --dev
