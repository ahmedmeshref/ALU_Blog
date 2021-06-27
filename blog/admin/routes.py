from flask import Blueprint, request, render_template, flash, url_for, redirect, abort, jsonify
from blog.admin.forms import AdminRegistrationForm
from blog.admin.utils import new_admin_email
from flask_login import login_required, current_user
from blog.model import User, Post
from blog.users.routes import delete_user_helper
from blog import db, bcrypt
import random

admin = Blueprint('admin', __name__)


@admin.route("/register_admin", methods=['GET', 'POST'])
@login_required
def register_admin():
    # validate request, made by a super admin.
    if current_user.admin != 2:
        return abort(403)
    # create form
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
            return redirect(url_for("admin.register_admin"))
        else:
            flash('Data is not valid')
    return render_template("admin/add_admin.html", form=form)


@admin.route("/all_admins", methods=['GET'])
@login_required
def show_all_admins():
    # validate request, made by a super admin.
    if current_user.admin != 2:
        return abort(403)
    admins = User.query.filter(User.admin == 1).all()
    return render_template("search_results.html", users=admins, current_user=current_user)


def verify_admin_helper(user_id):
    # verify that the given id belongs to a current user
    user = User.query.get_or_404(user_id)
    # current user should be an admin
    # no user can delete a super user
    # a user can't delete another user with the same degree (admin -- admin)
    if not current_user.admin or user.admin == 2 or (current_user.admin == user.admin):
        abort(403)
    return user


@admin.route("/profile/<user_id>/delete_user", methods=['POST'])
@login_required
def delete_user(user_id):
    """
    Delete a user made by super admins, can delete users and admins, and admins, can delete users only.
    Note: This function can only called from a user profile page.
    :param user_id: the user_id of the  target user to delete
    :return: home page
    """
    user = verify_admin_helper(user_id)
    return delete_user_helper(user)


@admin.route("/delete_user", methods=['POST'])
@login_required
def admin_delete_user():
    """
    Delete a user made by super admins, can delete users and admins, and admins, can delete users only.
    :return: json file contains username and email of the deleted user
    """
    user_id = request.get_json()["user_id"]
    user = verify_admin_helper(user_id)
    deleted_user_data = {"username": user.username, "email": user.email}
    try:
        delete_q = Post.__table__.delete().where(Post.user_id == user.id)
        db.session.execute(delete_q)
        db.session.delete(user)
        db.session.commit()
        return jsonify(deleted_user_data)
    except:
        db.session.rollback()
        return abort(500)



