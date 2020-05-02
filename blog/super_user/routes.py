from flask import Blueprint, request, render_template
from blog.super_user.forms import AdminRegistrationForm
from flask_login import login_required
from blog.model import User

super_user = Blueprint('super_user', __name__)


@super_user.route("/register_admin", methods=['GET', 'POST'])
@login_required
def register_admin():
    form = AdminRegistrationForm()
    if request.method == "POST":
        email = form.email.data
        # if email exists, make the user an admin without changing his data
        email_exist = User.query.filter_by(email=email).first()
        if email_exist:

        admin_name = form.admin_name.data
        password = form.password.data
        else:


    return render_template("register.html", admin=True, form=form)
