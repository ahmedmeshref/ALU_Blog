from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from blog.config import Config

app = Flask(__name__)
app.config.from_object(Config)
# make the application an instance from SQLAlchamy
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
# set the login route when the app tries to access login_required
login_manager.login_view = 'users.login'
# set a category info to give the login message style
login_manager.login_message_category = 'info'
# initialize the mail extension
mail = Mail(app)
app.debug = True


# call all the routes to run after initializing db and app
from blog.users.routes import users
from blog.posts.routes import posts
from blog.main.routes import main
from blog.errors.handel_errors import errors
from blog.admin.routes import admin


app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)
app.register_blueprint(errors)
app.register_blueprint(admin)
