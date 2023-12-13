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
    'task_track_started': True
}


class Config:
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"

    # Celery Configs
    # CELERY_CONFIG = celeryConfig
    CELERY = dict(
        broker_url='redis://localhost:6379/1',
        result_backend='redis://localhost:6379/2'
    ),
    SQLITE_DB_DIR = os.path.join(basedir, "../database")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "db.sqlite3")

    # Flask-Security configuration
    SECURITY_PASSWORD_HASH = "bcrypt"
    SECURITY_REGISTERABLE = True  # do not correct spelling
    SECURITY_CONFIRMABLE = False
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_UNAUTHORIZED_VIEW = None
    SECURITY_TRACKABLE = True
    SECURITY_USERNAME_ENABLE = True

    # Flask-Social configuration
    SECURITY_OAUTH_ENABLE = True
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID', '')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET', '')
    GITHUB_CLIENT_ID = os.getenv('GITHUB_CLIENT_ID', '')
    GITHUB_CLIENT_SECRET = os.getenv('GITHUB_CLIENT_SECRET', '')

    # Flask-Mail configuration
    MAIL_SERVER = 'sandbox.smtp.mailtrap.io'
    MAIL_PORT = 2525
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

    # SPA
    SECURITY_REDIRECT_BEHAVIOR = "spa"
    SECURITY_FLASH_MESSAGES = False
    SECURITY_CSRF_PROTECT_MECHANISMS = ["session", "token"]
    SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS = True

    # Send Cookie with csrf-token. This is the default for Axios and Angular.
    SECURITY_CSRF_COOKIE_NAME = "XSRF-TOKEN"
    WTF_CSRF_CHECK_DEFAULT = False
    WTF_CSRF_TIME_LIMIT = None
    SECURITY_REDIRECT_HOST = 'https://localhost:8080/'
    SECURITY_POST_LOGIN_VIEW = 'https://localhost:8080/'


class LocalDevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = os.environ.get("SECRET_KEY", '')
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT", '')
