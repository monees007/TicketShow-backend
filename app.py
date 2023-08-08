import os
from datetime import datetime, timedelta

from authlib.integrations.flask_client import OAuth
from celery.schedules import crontab
from flask import Flask, render_template
from flask_cors import CORS
from flask_mailman import Mail, EmailMessage
from flask_restful import Api
from flask_security import Security, hash_password, SQLAlchemySessionUserDatastore

from api.booking_api import BookingsAPI
from api.bulk_api import BulkShowsApi, BulkRunningApi, BulkTheatreApi
from api.review_api import ReviewsAPI
from api.running_api import RunningAPI
from api.show_api import ShowsAPI
from api.theater_api import TheatresAPI
from api.user_api import UserAPI
from api.views_api import HomePageAPI, SearchAPI
from application import cache
from application import swagger_render
# from application import tasks
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
user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
app.security = Security(app, user_datastore)  # , mail_util_cls=MyMailUtil)

cache.init_app(app)
CORS(app)
api = Api(app)
celery = workers.celery
celery.conf.update(broker_url=app.config['CELERY_BROKER_URL'], result_backend=app.config['CELERY_RESULT_BACKEND'])

# celery.config_from_object(celery_config)
celery.Task = workers.ContextTask

oauthapp = OAuth(app)
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
api.add_resource(BulkShowsApi, "/api/bulk/shows")
api.add_resource(BulkTheatreApi, "/api/bulk/theatre")
api.add_resource(BulkRunningApi, "/api/bulk/running")
api.add_resource(HomePageAPI, "/api/homepage")
api.add_resource(SearchAPI, "/api/search")
api.add_resource(UserAPI, "/api/user")


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour='24'), send_reminders.s())
    sender.add_periodic_task(hello_there('man').s(), name="hello t")


@celery.task()
def hello_there(name):
    print("Hello there, {}".format(name))
    return "Hello there, {}".format(name)


@celery.task()
def send_reminders(*args, **kwargs):
    emails = db_session.query(User.email).where(User.last_login_at < datetime.utcnow() - timedelta(minutes=1)).all()
    emails = [x[0] for x in emails]
    with mail.get_connection() as c:
        email1 = EmailMessage("We missed you today", """<h1> We missed you today. </h1>
                            <p> We noticed that you did not login today. We hope to see you soon. </p>
                            <p> Regards, </p>
                            <p> Team TicketShow </p>""", 'from@example.com', emails, connection=c, )
        email1.content_subtype = "html"  # Main content is now text/html
        email1.send()


# Error handlers
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4433)
