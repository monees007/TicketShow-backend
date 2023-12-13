from flask import current_app

from app import celery


class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with current_app.app_context():
            return self.run(self, *args, **kwargs)

