#! /bin/sh

# Activate local workers
#redis-server
celery -A app.celery worker -B --loglevel=info

#celery -A app.celery worker --beat --max-interval 10 -l info

