#! /bin/sh
. venv/bin/activate



# Activate local workers
#redis-server
#celery -A app.celery beat --loglevel=info

#celery -A app.celery worker -l debug
#celery -A app.celery worker beat  --max-interval 10 -l debug

celery -A app.celery worker -l info -B