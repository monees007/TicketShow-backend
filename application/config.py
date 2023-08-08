import os

basedir = os.path.abspath(os.path.dirname(__file__))

cacheConfig = {
    # REDIS Caching
    'CACHE_TYPE': "redis",
    'CACHE_REDIS_HOST': "localhost",
    'CACHE_REDIS_PORT': 6379,
    'CACHE_REDIS_DB': 0,
    'CACHE_REDIS_URL': "redis://localhost:6379/0",
    'CACHE_DEFAULT_TIMEOUT': 500,
}


# celeryConfig = {
#     "broker_url": "redis://redis",
#     "result_backend": "redis://redis",
#     "beat_schedule": {
#         "reminder_email": {
#             "task": "app.send_flask_mail",
#             "schedule": 10,
#         }
#     }
# }


class Config():
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"
    GOOGLE_CLIENT_ID = '519706053397-1739mh8juqvrs4tv89mer3dvdjoshl01.apps.googleusercontent.com'
    GOOGLE_CLIENT_SECRET = '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'
    GITHUB_CLIENT_ID = 'Iv1.e8d9d28168ffef59'
    GITHUB_CLIENT_SECRET = '7535a4842dd80137d6c6601275b8b55f3d27ab65'
    # Celery Configs
    # CELERY_CONFIG = celeryConfig
    CELERY_BROKER_URL = 'redis://localhost:6379/1'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/2'
    SQLITE_DB_DIR = os.path.join(basedir, "../database")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "db.sqlite3")

    # Flask-Security configuration
    SECURITY_PASSWORD_HASH = "bcrypt"
    SECURITY_REGISTERABLE = True  # do not correct spelling
    SECURITY_CONFIRMABLE = False
    SECURITY_OAUTH_ENABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_UNAUTHORIZED_VIEW = None
    SECURITY_TRACKABLE = True
    SECURITY_USERNAME_ENABLE = True

    # Flask-Mail configuration
    MAIL_SERVER = 'sandbox.smtp.mailtrap.io'
    MAIL_PORT = 2525
    MAIL_USERNAME = 'f3cc19503b3edc'
    MAIL_PASSWORD = '8763655e4bc55d'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

    # SPA
    SECURITY_REDIRECT_BEHAVIOR = "spa"
    SECURITY_FLASH_MESSAGES = False
    SECURITY_CSRF_PROTECT_MECHANISMS = ["session", "basic"]
    SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS = True

    # Send Cookie with csrf-token. This is the default for Axios and Angular.
    SECURITY_CSRF_COOKIE_NAME = "XSRF-TOKEN"
    WTF_CSRF_CHECK_DEFAULT = False
    WTF_CSRF_TIME_LIMIT = None
    SECURITY_REDIRECT_HOST = 'localhost:8080'


class LocalDevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = os.environ.get("SECRET_KEY", 'pf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-wyJILbq_dFw')
    SECURITY_PASSWORD_SALT = 'secrets.SystemRandom().getrandbits(128)'
