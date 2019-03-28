#!/bin/sh

# Waiting for Postgres
while ! nc -z db 5432; do
  sleep 0.1
done

python manage.py migrate --settings=project.settings.production
python manage.py collectstatic --no-input --settings=project.settings.production

exec "$@"
