from flask import Blueprint, request, render_template, flash, url_for, redirect, abort
from blog.super_user.forms import AdminRegistrationForm
from blog.super_user.utils import new_admin_email
from flask_login import login_required, current_user
from blog.model import User
from blog import db, bcrypt
import random

super_user = Blueprint('super_user', __name__)


@super_user.route("/register_admin", methods=['GET', 'POST'])
@login_required
def register_admin():
    form = AdminRegistrationForm()
    if request.method == "POST":
        if form.validate_on_submit():
            email = form.email.data
            username = form.username.data
            # generate a random password
            possible_characters = "@#_abcdefghijklmnopqrstuvwxyz1234567890"
            random_password = "".join([random.choice(possible_characters) for _ in range(6)])
            # hash the passowrd
            hashed_pass = bcrypt.generate_password_hash(random_password).decode('utf-8')
            user = User(username=username.title(), email=email, password=hashed_pass, admin=1)
            db.session.add(user)
            db.session.commit()
            new_admin_email(user)
            flash("New admin was added successfully and an email was sent to him.", "success")
            return redirect(url_for("super_user.register_admin"))
    return render_template("super_user/add_admin.html", form=form)


@super_user.route("/all_admins", methods=['GET'])
@login_required
def show_all_admins():
    # validate request, made by a super user.
    if current_user.admin != 2:
        return abort(403)
    admins = User.query.filter(User.admin == 1).all()
    return render_template("search_results.html", users=admins, current_user=current_user)


# @super_user.route("/delete_user", methods=['POST'])
# @login_required
# def delete_user():
#     # check if user
#     if not current_user.admin:
#         abort(403)
#     user = User.query.filter(User.id == user_id).first()
#     if not user:
#         abort(404)
#
#     return render_template("search_results.html", users=admins, current_user=current_user)
