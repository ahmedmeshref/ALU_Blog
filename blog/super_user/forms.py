from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from blog.model import User


class AdminRegistrationForm(FlaskForm):
    admin_name = StringField('Admin name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=5, max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=50)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register Admin')

    # check if the username already exist
    def validate_adminname(self, admin_name):
        username_exist = User.query.filter_by(username=admin_name.data).first()
        if username_exist:
            raise ValidationError('username is already taken!')
        unvalid_chars = ["@", "&", "'", "(", ")", "<", ">", '"']
        for char in unvalid_chars:
            if char not in admin_name.data:
                continue
            raise ValidationError(f"username can't include {char}")
