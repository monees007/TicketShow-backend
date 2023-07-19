import os

from authlib.integrations.flask_client import OAuth
from flask import Flask, render_template
from flask_cors import CORS
from flask_mailman import Mail
from flask_restful import Api
from flask_security import Security, hash_password, SQLAlchemySessionUserDatastore

from api.booking_api import BookingsAPI
from api.review_api import ReviewsAPI
from api.running_api import RunningAPI
from api.show_api import ShowsAPI
from api.theater_api import TheatresAPI
from application import swagger_render
from application import tasks
from application import workers
from application.config import LocalDevelopmentConfig
from application.database import db_session, init_db
from application.models import User, Role

# render openAPI
swagger_render.render()

app = Flask(__name__, template_folder="templates")
if os.getenv('ENV', "development") == "production":
    app.logger.info("Currently no production config is setup.")
    raise Exception("Currently no production config is setup.")
else:
    app.logger.info("Staring Local Development.")
    print("Staring Local Development")
    app.config.from_object(LocalDevelopmentConfig)
init_db()
app.app_context().push()
app.logger.info("App setup complete")

# class MyMailUtil(MailUtil):
#     def send_mail(self, template, subject, recipient, sender, body, html, **kwargs):
#         send_flask_mail.delay(
#             subject=subject,
#             from_email=sender,
#             to=[recipient],
#             body=body,
#             html=html,
#         )


# Setup Flask-Security
user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
app.security = Security(app, user_datastore)  # , mail_util_cls=MyMailUtil)

# # Setup Celery
# # backend = "redis://localhost:6379/0"
# # broker = backend.replace("0", "1")
# celery = Celery(__name__)  # , #backend=backend, broker=broker)
# celery.conf.update(app.config)
# TaskBase = celery.Task


# class ContextTask(TaskBase):
#     def __call__(self, *args, **kwargs):
#         with app.app_context():
#             return TaskBase.__call__(self, *args, **kwargs)


# celery.Task = ContextTask

CORS(app)
api = Api(app)
celery = workers.celery
celery.conf.update(
    broker_url=app.config['CELERY_BROKER_URL'],
    result_backend=app.config['CELERY_RESULT_BACKEND']
)
celery.Task = workers.ContextTask

oauthapp = OAuth(app)  # ignore Typo
mail = Mail(app)
app.app_context().push()

# one time setup
with app.app_context():
    # Create a user to test with
    init_db()
    if not app.security.datastore.find_user(email="test3@me.com"):
        app.security.datastore.create_user(email="test3@me.com", password=hash_password("password3"))
    db_session.commit()

# APIs for the application
api.add_resource(ShowsAPI, "/api/shows")
api.add_resource(TheatresAPI, "/api/theatre")
api.add_resource(ReviewsAPI, "/api/review")
api.add_resource(BookingsAPI, "/api/booking")
api.add_resource(RunningAPI, "/api/running")


# @celery.task
# def send_flask_mail(**kwargs):
#     with app.app_context():
#         with mail.get_connection() as connection:
#             html = kwargs.pop("html", None)
#             msg = EmailMultiAlternatives(**kwargs, connection=connection)
#             if html:
#                 msg.attach_alternative(html, "text/html")
#             msg.send()


# Import all the controllers, so they are loaded
# from application.controllers import *

# # Add all restful controllers
# from application.api import ArticleLikesAPI
# api.add_resource(ArticleLikesAPI, "/api/article_likes", "/api/article_likes/<int:article_id>")
#

# @app.errorhandler(404)
# def page_not_found(e):
#     # note that we set the 404 status explicitly
#     return render_template('404.html'), 404
#
#
# @app.errorhandler(403)
# def not_authorized(e):
#     # note that we set the 403 status explicitly
#     return render_template('403.html'), 403


@app.route("/")
def home():
    return render_template("swagger.html")


@app.route("/hello/<name>")
def hello(name):
    job = tasks.hello_there.delay(name)
    return str(job), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4433)
