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
    return render_template("admin/add_admin.html", form=form)


@admin.route("/all_admins", methods=['GET'])
@login_required
def show_all_admins():
    # validate request, made by a super admin.
    if current_user.admin != 2:
        return abort(403)
    admins = User.query.filter(User.admin == 1).all()
    return render_template("search_results.html", users=admins, current_user=current_user)


@admin.route("/profile/<user_id>/delete_user", methods=['POST'])
@login_required
def delete_user(user_id):
    """
    Delete a user made by super admins, can delete users and admins, and admins, can delete users only.
    :param user_id: the user_id of the  target user to delete
    :return: home page
    """
    # verify that a user is not deleting himself
    if current_user.id == user_id:
        abort(403)
    # verify that the given id belongs to a current user
    user = User.query.get_or_404(user_id)
    # admin can't delete an admin, also no user can delete a super user
    if user.admin == 2 or (current_user.admin == 1 and user.admin == 1):
        abort(403)
    return delete_user_helper(user)


@admin.route("/delete_user", methods=['POST'])
@login_required
def delete_exisiting_user():
    user_id = request.get_json()["user_id"]
    # verify that the current user is a super admin
    if current_user.admin != 2:
        abort(403)
    user = User.query.get_or_404(user_id)
    # verify that the request is not to delete another super admin
    if user.admin == 2:
        abort(403)
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



