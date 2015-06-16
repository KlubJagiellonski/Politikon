#!/usr/bin/env bash

python manage.py schemamigration accounts --initial
python manage.py schemamigration events --initial

python manage.py migrate accounts
python manage.py migrate events
