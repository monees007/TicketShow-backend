from application.workers import celery


@celery.task()
def hello_there(name):
    print("Hello there, {}".format(name))
    return "Hello there, {}".format(name)
