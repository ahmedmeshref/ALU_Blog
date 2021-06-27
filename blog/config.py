import os


class Config:
    SECRET_KEY = os.urandom(32)
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('IBM_POSTGRESQL') + 'alu_social'
    SQLALCHEMY_TRACK_MODIFICATIONS = False