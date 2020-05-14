import os


# class Config:
#     SECRET_KEY = os.environ.get('SECRETKEY')
#     MAIL_SERVER = 'smtp.googlemail.com'
#     MAIL_PORT = 587
#     MAIL_USE_TLS = True
#     MAIL_USERNAME = os.environ.get('EMAIL')
#     MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
#     SQLALCHEMY_DATABASE_URI = os.environ.get('POSTGRESQL')
#     SQLALCHEMY_TRACK_MODIFICATIONS = False


class Config:
    SECRET_KEY = "472267410d1672db337b9e9ca710ee1b"
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "a.meshref@alustudent.com"
    MAIL_PASSWORD = "250787388219@Meshref"
    SQLALCHEMY_DATABASE_URI = "postgres://xqfgovndpbsmpy:7d6bf2bd54345aceeeeb5886e8f741e6fe073d7abef1a27dd3d3ea8d7a32d50b@ec2-34-230-149-169.compute-1.amazonaws.com:5432/d22uqnfgc1h4tr"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
