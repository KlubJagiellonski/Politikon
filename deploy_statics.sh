#!/bin/sh
rm -rf ./static_build
python manage.py collectstatic --noinput -v 0
DATABASE_URL='postgres://localhost/' ENV_FLAVOUR=PRODUCTION python manage.py assets build
DATABASE_URL='postgres://localhost/' ENV_FLAVOUR=PRODUCTION python manage.py collectstatic --noinput
