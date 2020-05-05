from flask_mail import Message
from flask import url_for
from blog import mail


def new_admin_email(user):
    # create a token for the user
    token = user.reset_password_token()
    # create a Message instance
    msg = Message('New Admin Invitation', sender='norepley@alustudent.com',
                  recipients=[user.email])
    msg.body = f"""Hi {user.username},
I hope this email finds you well,

I would like to welcome you as a new Admin in ALU_Blog. 

Username: {user.username}
Login_email: {user.email}

Please visit this link within 2 hours to set your passowrd:
{url_for('users.reset_password', token=token, _external=True)}

or visit our website and click on forgot my password to reset your password.
"""
    mail.send(msg)
