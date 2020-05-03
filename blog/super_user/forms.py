from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from blog.model import User


class AdminRegistrationForm(FlaskForm):
    username = StringField('Admin name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=5, max=50)])
    submit = SubmitField('Register Admin')

    # check if the email is unique
    def validate_email(self, email):
        email_exist = User.query.filter_by(email=email.data).first()
        if email_exist:
            raise ValidationError("email is already registered!")

    # check if the username already exist
    def validate_username(self, username):
        username_exist = User.query.filter_by(username=username.data.title()).first()
        if username_exist:
            raise ValidationError('username is already taken!')
        unvalid_chars = ["@", "&", "'", "(", ")", "<", ">", '"']
        for char in unvalid_chars:
            if char not in username.data:
                continue
            raise ValidationError(f"username can't include {char}")
