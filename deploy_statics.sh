#!/bin/sh
DATABASE_URL='postgres://bb:bb@localhost/bb' ENV_FLAVOUR=PRODUCTION python manage.py collectstatic