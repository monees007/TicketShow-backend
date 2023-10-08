from flask import request, jsonify
from flask_security import login_user, current_user
from google.auth.transport import requests
from google.oauth2 import id_token

from application.config import Config
from application.database import db_session
from application.models import User


def login_with_google():
    # Get the token from the request
    token = request.json.get('token')
    # Verify the token with Google One Tap (You'll need to implement this part)
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), Config.GOOGLE_CLIENT_ID)
        # ID token is valid. Get the user's Google Account ID from the decoded token.
        userid = idinfo['sub']
        email = idinfo['email']
        print(userid, email)
        # Check if the user exists
        user = User.query.filter_by(email=email).first()
        if user:
            # Log in the user
            login_user(user)
            # Generate a Flask-Security token
            auth_token = current_user.get_auth_token()
            print(auth_token)
            return jsonify({'message': 'Login successful', 'token': auth_token}), 200
        else:
            # Create a new user if they don't exist
            new_user = User()
            db_session.add(new_user)
            db_session.commit()
            login_user(new_user)
            # Generate a Flask-Security token for the new user
            login_user(user)
            # Generate a Flask-Security token
            auth_token = current_user.get_auth_token()
            print(auth_token)
            return jsonify({'message': 'User created and logged in', 'token': auth_token}), 200
    except ValueError:
        return jsonify({'message': 'Invalid Google token'}), 401
