import os


# class DevConfig:
#     SECRET_KEY = os.environ.get('SECRETKEY')
#     MAIL_SERVER = 'smtp.googlemail.com'
#     MAIL_PORT = 587
#     MAIL_USE_TLS = True
#     MAIL_USERNAME = os.environ.get('EMAIL')
#     MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
#     SQLALCHEMY_DATABASE_URI = os.environ.get('POSTGRESQL')
#     SQLALCHEMY_TRACK_MODIFICATIONS = False


class Config:
    SECRET_KEY = os.environ.get('SECRETKEY')
    MAIL_SERVER = ""
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = "postgres://rmeucwxwmsazxu:4b4c60b835702b91f9a77f1cf7f324279d 0b0ae58846052fbffdf9db106e" \
                              "e213@ec2-3-231-16-122.compute-1.amazonaws.com:5432/d3994g9lcuuvtr"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
