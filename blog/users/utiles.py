import os
import re
from PIL import Image
from flask import url_for
from blog import app, mail
from flask_login import current_user
from flask_mail import Message
import secrets


def save_picture(new_picture):
    # create a random string to be the name of the file
    random_token = secrets.token_hex(8)
    # extract the given picture's extension
    pic_ext = re.findall(r"\.[a-zA-Z]+", new_picture.filename)[-1]
    new_picture_fn = random_token + pic_ext
    # get the path to store the new picture in (application path + static folder)
    new_picture_path = os.path.join(app.root_path, 'static/profile_pics', new_picture_fn)
    # resize the image
    picture_f = Image.open(new_picture)
    picture_f.thumbnail((250, 250))
    # save the picture
    picture_f.save(new_picture_path)
    return new_picture_fn


def delete_current_picture():
    picture_file = current_user.profile_image
    # join the path of the current user's profile picture
    if picture_file != "my_profile.png":
        picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_file)
        # delete the picture
        os.remove(picture_path)


def send_reset_email(user):
    # create a token for the user
    token = user.reset_password_token()
    # create a Message instance
    msg = Message('Reset your password', sender='norepley@alustudent.com',
                  recipients=[user.email])
    msg.body = f"""Hi {user.username}, 

Please visit the link provided down within 2 hour to reset your password.

Link: {url_for('users.reset_password', token=token, _external=True)}
If you didn't request a password reset, please ignore this email
"""
    mail.send(msg)
