release: python manage.py migrate
web: gunicorn educa.wsgi
worker: celery -A educa worker -l info