from flask import render_template, url_for, request, flash, redirect, abort, Blueprint
from blog import db, bcrypt
from blog.users.forms import (RegistrationForm, LoginForm, UpdateProfileForm,
                              RequestResetPasswordForm, ResetPasswordForm)
from blog.model import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
from sqlalchemy import desc
from blog.users.utiles import send_reset_email, save_picture, delete_current_picture

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            if form.email.data == "a.meshref@alustudent.com":
                user = User(username=form.username.data.title(), email=form.email.data, password=hashed_pass, admin=2)
            else:
                user = User(username=form.username.data.title(), email=form.email.data, password=hashed_pass)
            db.session.add(user)
            db.session.commit()
            flash(f"Account created successfully! Now you can login", 'success')
            return redirect(url_for("users.login"))
    return render_template("register.html", title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    # get any args that might be send with a get request to the login route since the user needs to login before
    # accessing any other method
    next_page = request.args.get('next')
    if request.method == 'POST':
        if form.validate_on_submit():
            existing_user = User.query.filter_by(email=form.email.data).first()
            if existing_user and bcrypt.check_password_hash(existing_user.password, form.password.data):
                if not existing_user.active:
                    existing_user.active = True
                    flash("Account activated successfully", 'success')
                login_user(existing_user, remember=form.remember_me.data)
                flash("Logged in successfully", 'success')
                # get the next page if the user have tried to access any and was
                if next_page:
                    return redirect(next_page)
                return redirect(url_for("main.home"))
            else:
                flash("incorrect email or password!", "danger")
    return render_template("login.html", title='Login', form=form)


@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("users.login"))


@users.route("/profile/<user_id>", methods=['GET', 'POST'])
@login_required
def profile(user_id):
    # check if the current user is viewing his own profile or someone else's
    user = User.query.get_or_404(user_id)
    if request.method == "POST":
        return redirect(url_for('users.change_profile', user_id=user.id))
    # send the user posts
    current_page = request.args.get('current_page', 1, type=int)
    posts = Post.query.filter_by(author=user).order_by(desc(Post.date)).paginate(page=current_page, per_page=6)
    return render_template("profile.html", title=f"profile - {user.username}", posts=posts,
                           now=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), datetime=datetime, user=user)


@users.route("/profile/<user_id>/update_profile", methods=['POST', 'GET'])
@login_required
def change_profile(user_id):
    # check if the given user_id exist
    user = User.query.get_or_404(user_id)
    # check if the request was made by the account user
    if user != current_user:
        # if not return forbidden page error
        abort(403)
    form = UpdateProfileForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if form.new_picture.data:
                # delete the current picture from the profile_pics file locally
                delete_current_picture()
                # add the given picture to the profile_pics file and get the path of the picture
                new_picture_fn = save_picture(form.new_picture.data)
                # change the name of the profile picture in the database in the database
                current_user.profile_image = new_picture_fn
                flash("Your profile picture has been updated successfully", "success")
            if form.new_username.data.title() != current_user.username:
                current_user.username = form.new_username.data.title()
                flash("Your username has been updated successfully", "success")
            db.session.commit()
            return redirect(url_for('users.profile', user_id=current_user.id))
    # set the value of the new username to the current username
    form.new_username.data = current_user.username
    image_f = url_for('static', filename='profile_pics/' + current_user.profile_image)
    return render_template("edit_profile.html", title="Edit Profile",
                           profile_image=image_f, form=form)


@users.route("/reset_password_email", methods=['GET', 'POST'])
def request_reset_password():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RequestResetPasswordForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            send_reset_email(user)
            flash('reset password email has been sent successfully! please check your email', 'success')
            return redirect(url_for('users.login'))
    return render_template("request_reset.html", title="Request Reset", form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    user = User.verify_reset_password_token(token)
    if not user:
        flash("Token is expired or invalid", "warning")
        return redirect(url_for('users.request_reset_password'))
    form = ResetPasswordForm()
    if request.method == "POST":
        if form.validate_on_submit():
            hashed_new_pass = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
            user.password = hashed_new_pass
            db.session.commit()
            flash(f"Password updated successfully", 'success')
            return redirect(url_for("users.login"))
    return render_template("reset_password.html", title="Create New Password", form=form)


@users.route('/profile/deactivate_account/<user_id>', methods=['POST'])
@login_required
def deactivate_account(user_id):
    # check if user exists or not
    user = User.query.get_or_404(user_id)
    # check if a user is using the url to update someone else's post
    if user != current_user:
        abort(403)
    current_user.active = False
    delete_current_picture()
    current_user.profile_image = "in_active.png"
    db.session.commit()
    flash("Account deactivated Successfully", "success")
    return redirect(url_for('users.logout'))


@users.route("/delete_my_account/<user_id>", methods=['POST'])
@login_required
def delete_my_account(user_id):
    # check if user exists or not
    user = User.query.get_or_404(user_id)
    # check if a user is using the url to update someone else's post
    if user != current_user:
        abort(403)
    return delete_user_helper(user)


def delete_user_helper(user):
    try:
        delete_q = Post.__table__.delete().where(Post.user_id == user.id)
        db.session.execute(delete_q)
        db.session.delete(user)
        db.session.commit()
        flash("Account deleted Successfully", "success")
        return redirect(url_for('users.login'))
    except:
        db.session.rollback()
        return abort(500)
