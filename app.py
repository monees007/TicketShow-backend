import os

from flask import Flask, render_template_string, render_template
from flask_restful import Resource, Api

from flask_security import Security, current_user, auth_required, hash_password, \
    SQLAlchemySessionUserDatastore

from application.config import LocalDevelopmentConfig
from application.database import db_session, init_db
from application.models import User, Role

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

# one time setup
with app.app_context():
    # Create a user to test with
    init_db()
    if not app.security.datastore.find_user(email="test3@me.com"):
        app.security.datastore.create_user(email="test3@me.com", password=hash_password("password3"))
    db_session.commit()
api = Api(app)
app.app_context().push()


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
    return render_template_string('Hello {{email}} !', email=current_user.email)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4433)