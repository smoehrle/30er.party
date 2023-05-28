install:
	poetry install

run:
	poetry run python ./manage.py migrate
	poetry run python ./manage.py runserver 0.0.0.0:8000

migrate:
	poetry run python ./manage.py migrate

makemigrations:
	poetry run python ./manage.py makemigrations

collectstatic:
	poetry run python ./manage.py compilescss
	poetry run python ./manage.py collectstatic --noinput -i facebook/*
