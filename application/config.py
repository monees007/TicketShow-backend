import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"
    GOOGLE_CLIENT_ID = '519706053397-1739mh8juqvrs4tv89mer3dvdjoshl01.apps.googleusercontent.com'
    GOOGLE_CLIENT_SECRET = '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'
    GITHUB_CLIENT_ID = 'Iv1.e8d9d28168ffef59'
    GITHUB_CLIENT_SECRET = '7535a4842dd80137d6c6601275b8b55f3d27ab65'
    CELERY_BROKER_URL = 'redis://localhost:6379/1'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/2'
    SQLITE_DB_DIR = os.path.join(basedir, "../database")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "db.sqlite3")
    SECURITY_PASSWORD_HASH = "bcrypt"
    SECURITY_REGISTERABLE = True  # do not correct spelling
    SECURITY_CONFIRMABLE = True
    SECURITY_OAUTH_ENABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_UNAUTHORIZED_VIEW = None
    MAIL_SERVER = 'smtp.mailgun.org'
    MAIL_PORT = 587
    MAIL_USERNAME = "postmaster@sandbox1c10f67a4d8d48368d6045147034f119.mailgun.org"
    MAIL_PASSWORD = "fa4311bd80bf60953e0170ed11df5203-c30053db-68919d7e"
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    # MAIL_DEFAULT_SENDER = 'noreply@localhost'

    # SECURITY_USERNAME_ENABLE = True

class LocalDevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = os.environ.get("SECRET_KEY", 'pf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-wyJILbq_dFw')
    SECURITY_PASSWORD_SALT = 'secrets.SystemRandom().getrandbits(128)'
