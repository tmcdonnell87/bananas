web: gunicorn config.wsgi:application
worker: celery worker --app=bananas.taskapp --loglevel=info
