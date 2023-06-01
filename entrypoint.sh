#!/bin/sh

# Copy static files
echo "Copy static files"
find /static -mindepth 1 -delete
cp -a /website/static/. /static


echo "Migrating DB"
poetry run python ./manage.py migrate

echo "Starting ASGI Server..."
poetry run daphne website.asgi:application -b 0.0.0.0
