import os


class DevConfig:
    SECRET_KEY = os.environ.get('SECRETKEY')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('POSTGRESQL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False



class Config:
    SECRET_KEY = os.environ.get('SECRETKEY')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('POSTGRESQL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False