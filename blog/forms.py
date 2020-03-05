from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from blog.model import User
from flask_login import current_user


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=5, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    # check if the email already exist
    def validate_email(self, email):
        email_exist = User.query.filter_by(email=email.data).first()
        if email_exist:
            raise ValidationError('This email is already registered! Please login')

    # check if the username already exist
    def validate_username(self, username):
        username_exist = User.query.filter_by(username=username.data).first()
        if username_exist:
            raise ValidationError('username is already taken!')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateProfileForm(FlaskForm):
    """
    form for updating the username and picture fields
    """
    new_username = StringField('New Username', validators=[DataRequired(), Length(min=2, max=20)])
    new_picture = FileField("Update Profile Picture", validators=[FileAllowed(['jpg', 'jpeg ', 'png'])])
    submit = SubmitField('Save Changes')

    def validate_new_username(self, new_username):
        # check if the new username is different from the current
        if new_username.data != current_user.username:
            # check that the new username is unique
            username_exist = User.query.filter_by(username=new_username.data).first()
            if username_exist:
                raise ValidationError('username is already taken!')


class AddPostForm(FlaskForm):
    """
    form for adding new posts
    """
    title = StringField("Title", validators=[DataRequired(), Length(min=2, max=30)])
    content = TextAreaField("Content", validators=[DataRequired(), Length(min=10, max=500)],
                            render_kw={"placeholder": "What new at ALU?"})
    submit = SubmitField("Post")

