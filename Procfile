web: gunicorn politikon.wsgi -b "0.0.0.0:$PORT" -w 2 --preload  --log-level=debug
#worker: python manage.py celery beat --loglevel=INFO & python manage.py celery worker --loglevel=DEBUG --concurrency=1
