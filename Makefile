install:
	poetry install
	npm ci

run_frontend:
	npm run watch

run_backend:
	poetry run python ./manage.py migrate
	poetry run python ./manage.py runserver 0.0.0.0:8000

migrate:
	poetry run python ./manage.py migrate

makemigrations:
	poetry run python ./manage.py makemigrations

collectstatic:
	# poetry run python ./manage.py compilescss
	poetry run python ./manage.py collectstatic --noinput
