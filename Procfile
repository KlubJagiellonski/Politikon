web: newrelic-admin run-program gunicorn politikon.wsgi -b "0.0.0.0:$PORT" -w 2 --preload --log-level=INFO --settings=politikon.settings.production
worker: celery -A politikon worker -B -l info
# worker: python manage.py celery worker --loglevel=INFO --concurrency=1 --without-mingle --without-gossip & sleep 30 && python manage.py celery beat --loglevel=INFO
