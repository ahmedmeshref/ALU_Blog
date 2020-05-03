from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from blog.model import User
from flask_login import current_user


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=5, max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=50)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('SIGN UP')

    # check if the email already exist
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user and not user.active:
            raise ValidationError('Your email is already registered but deactivated! Please login to activate it.')
        elif user:
            raise ValidationError('Your email is already registered! Please login')

    # check if the username already exist
    def validate_username(self, username):
        username_exist = User.query.filter_by(username=username.data).first()
        if username_exist:
            raise ValidationError('username is already taken!')
        unvalid_chars = ["@", "&", "'", "(", ")", "<", ">", '"']
        for char in unvalid_chars:
            if char in username.data:
                raise ValidationError(f"username can't include {char}")


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('SIGN IN')


class UpdateProfileForm(FlaskForm):
    """
    form for updating the username and picture fields
    """
    new_username = StringField('New Username', validators=[DataRequired(), Length(min=2, max=20)])
    new_picture = FileField("Update Profile Picture", validators=[FileAllowed(['jpg', 'jpeg ', 'png'])])
    submit = SubmitField('SAVE CHANGES')

    def validate_new_username(self, new_username):
        # check if the new username is different from the current
        if new_username.data != current_user.username:
            # check that the new username is unique
            username_exist = User.query.filter_by(username=new_username.data).first()
            if username_exist:
                raise ValidationError('username is already taken!')


class RequestResetPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('SEND EMAIL')

    # check if the email doesn't exist
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('Email is not Registered! Please create an account!')
        if not user.active:
            raise ValidationError('You have deactivated your account. Please login to activate it first.')


class ResetPasswordForm(FlaskForm):
    """
    form for reseting the user password
    """
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_new_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('RESET PASSWORD')
