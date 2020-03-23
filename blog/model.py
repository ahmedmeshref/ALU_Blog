from datetime import datetime
from blog import app, db, login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as ts

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# create a table
class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    profile_image = db.Column(db.String(20), nullable=False, default='my_profile.png')
    email = db.Column(db.String(50), unique=True, nullable=False)
    # we hash the user password to a 60 string long
    password = db.Column(db.String(60), nullable=False)
    # activation state
    active = db.Column(db.String(10), nullable=False, default=True)
    # one to many relationship between the user (author) and the posts
    # give a ref to Post class
    posts = db.relationship('Post', backref='author', lazy=True)

    def reset_password_token(self, active_sec=3600):
        """
        create token creates in a random token for resting the users password
        """
        # create an instance of the ts model and set an expiration time
        s = ts(app.config['SECRET_KEY'], active_sec)
        # create a token with a user id with a payload
        return s.dumps({'user_id': self.id}).decode('utf-8')

    # verify_reset_password_token is a static function that doesn't accept
    # self variable
    @staticmethod
    def verify_reset_password_token(token):
        """
        verify if it is the same user, using his id
        """
        s = ts(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.profile_image}')"


class Post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    content = db.Column(db.Text, nullable=False)
    # connect used_id to id col from user table
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post({self.title}, {self.date})"
