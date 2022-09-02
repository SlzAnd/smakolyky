web: gunicorn cookbook/cookbook.wsgi
release: python cookbook/manage.py makemigrations --noinput
release: python cookbook/manage.py collectstatic --noinput
release: python cookbook/manage.py migrate --noinput