#! /bin/sh
echo "======================================================================"
echo "Welcome to to the setup. This will setup the local virtual env." 
echo "And then it will install all the required python libraries."
echo "You can rerun this without any issues."
echo "----------------------------------------------------------------------"
#if [ -d ".env" ];
#then
#    echo "Enabling virtual env"
#else
#    echo "No Virtual env. Please run setup.sh first"
#    exit
#fi

# Activate local workers
celery -A app.celery worker --loglevel=info

# Activate virtual env
#. .env/bin/activate
#export ENV=development
#python main.py
#deactivate
