from celery import Celery
from flask import current_app

celery = Celery(__name__)


# celery.conf.update(app.config)
class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with current_app.app_context():
            return self.run(self, *args, **kwargs)
