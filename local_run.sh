#! /bin/sh
echo "======================================================================"
echo "Welcome to to the application. This will setup the local virtual env." 
echo "And then it will install all the required python libraries."
echo "You can rerun this without any issues."
echo "----------------------------------------------------------------------"


# Activate local workers
#redis-server
#celery -A app.celery worker --loglevel=info

# Activate virtual env
#. venv/bin/activate
export ENV=development
python app.py
#deactivate
