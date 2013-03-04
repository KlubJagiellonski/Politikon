#!/bin/sh
DATABASE_URL='postgres://localhost/' ENV_FLAVOUR=PRODUCTION python manage.py assets build
DATABASE_URL='postgres://localhost/' ENV_FLAVOUR=PRODUCTION python manage.py collectstatic
