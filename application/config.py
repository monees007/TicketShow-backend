import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
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
    SECURITY_CONFIRMABLE = False
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

    SECURITY_USERNAME_ENABLE = True
    # REDIS Caching
    CACHE_TYPE = "redis"
    CACHE_REDIS_HOST = "localhost"
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 0
    CACHE_REDIS_URL = "redis://localhost:6379/0"
    CACHE_DEFAULT_TIMEOUT = 500

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
