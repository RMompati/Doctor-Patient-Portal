import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = '_secret_'
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, './database/dpp.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = '*******'
    MAIL_PASSWORD = '*******'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True