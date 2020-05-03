from flask_mail import Message
from flask import url_for
from blog import mail


def new_admin_email(user, password):
    # create a Message instance
    msg = Message('New Admin Invitation', sender='norepley@alustudent.com',
                  recipients=[user.email])
    msg.body = f"""Hi {user.username},
I hope this email finds you well,

I would like to welcome you as a new Admin in ALU_Blog. 

Username: {user.username}
Login_email: {user.email}
Login_password: {user.password}
"""
    mail.send(msg)
