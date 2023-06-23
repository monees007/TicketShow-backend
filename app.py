import os

from flask import Flask, render_template
from flask_cors import CORS
from flask_restful import Api
from flask_security import Security, auth_required, hash_password, \
    SQLAlchemySessionUserDatastore

from api.booking_api import BookingsAPI
from api.review_api import ReviewsAPI
from api.running_api import RunningAPI
from api.show_api import ShowsAPI
from api.theater_api import TheatresAPI
from application import swagger_render
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

# Setup Flask-Security
user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
app.security = Security(app, user_datastore)
api = Api(app)
CORS(app)
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
api.add_resource(ReviewsAPI, "/api/reviews")
api.add_resource(BookingsAPI, "/api/bookings")
api.add_resource(RunningAPI, "/api/running")


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
@auth_required()
def home():
    return render_template("swagger.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4433)
