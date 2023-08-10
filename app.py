import os
from datetime import datetime, timedelta

from authlib.integrations.flask_client import OAuth
from celery.schedules import crontab
from flask import Flask, render_template
from flask_cors import CORS
from flask_mailman import Mail, EmailMessage
from flask_restful import Api
from flask_security import Security, hash_password, SQLAlchemySessionUserDatastore
from sqlalchemy import or_

import application.stats
from api.booking_api import BookingsAPI
from api.bulk_api import BulkShowsApi, BulkRunningApi, BulkTheatreApi, ExportCSV
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
from application.models import User, Role, Booking

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
api.add_resource(ExportCSV, '/api/export')


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour='24'), send_reminders.s())
    sender.add_periodic_task(crontab(day_of_month='1'), monthly_er.s())


@celery.task()
def take_stats(*args):
    now = datetime.utcnow()
    prev = now - timedelta(days=1)
    nex = now + timedelta(days=1)
    data = db_session.query(Booking.total_price, Booking.show_name, Booking.th).filter(
        or_(nex > Booking.timestamp, Booking.timestamp > prev))
    data = [x.as_dict() for x in data]
    print(data)
    return data


@celery.task()
def send_reminders(*args, **kwargs):
    emails = db_session.query(User.email).where(User.last_login_at < datetime.utcnow() - timedelta(minutes=1)).all()
    emails = [x[0] for x in emails]
    with mail.get_connection() as c:
        email1 = EmailMessage("We missed you today", render_template('daily_reminder.html'), 'from@example.com', emails,
                              connection=c, )
        email1.content_subtype = "html"  # Main content is now text/html
        email1.send()


@celery.task()
def monthly_er(*args, **kwargs):
    emails = [x[0] for x in db_session.query(User.email).all()]
    with mail.get_connection() as c:
        for em in emails:
            email1 = EmailMessage("Monthly Revenue",
                                  render_template("monthly_er.html", feed=application.stats.monthly_er(em)),
                                  'no-reply@ticket-show.com', to=em, connection=c, )
            email1.content_subtype = "html"  # Main content is now text/html
            email1.send()


@app.route("/")
def home():
    return render_template("swagger.html")


@app.route("/test")
def test():
    return "Hello World"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4433)
