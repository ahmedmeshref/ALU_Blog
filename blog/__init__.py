from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
# set the login route when the app tries to access login_required
login_manager.login_view = 'login'
# set a category info to give the login message style
login_manager.login_message_category = 'info'
app.config['SECRET_KEY'] = '472267410d1672db337b9e9ca710ee1b'
ENV = 'dev'

# create a database layer for development
if ENV == "dev":
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:250787388219@localhost/ALU_blog'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

# make the application an instance from SQLAlchamy
db = SQLAlchemy(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# call all the routes to run after initializing db and app
from blog import routes
