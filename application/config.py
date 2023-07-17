import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    DEBUG = False
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"

class LocalDevelopmentConfig(Config):
    SQLITE_DB_DIR = os.path.join(basedir, "../database")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "db.sqlite3")
    DEBUG = True
    SECRET_KEY = os.environ.get("SECRET_KEY", 'pf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-wyJILbq_dFw')
    SECURITY_PASSWORD_HASH = "bcrypt"
    SECURITY_PASSWORD_SALT = 'secrets.SystemRandom().getrandbits(128)'
    SECURITY_REGISTERABLE = True  # do not correct spelling
    SECURITY_CONFIRMABLE = True
    SECURITY_OAUTH_ENABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_UNAUTHORIZED_VIEW = None
    WTF_CSRF_ENABLED = False
    # SECURITY_USERNAME_ENABLE = True

    GOOGLE_CLIENT_ID = '519706053397-1739mh8juqvrs4tv89mer3dvdjoshl01.apps.googleusercontent.com'
    GOOGLE_CLIENT_SECRET = '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'
    GITHUB_CLIENT_ID = 'Iv1.e8d9d28168ffef59'
    GITHUB_CLIENT_SECRET = '7535a4842dd80137d6c6601275b8b55f3d27ab65'
