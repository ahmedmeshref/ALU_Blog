import os
import re
from PIL import Image
from flask import render_template, url_for, request, flash, redirect, Markup
from blog import app, db, bcrypt
from blog.forms import RegistrationForm, LoginForm, UpdateProfileForm, AddPostForm
from blog.model import User, Post
from flask_login import login_user, current_user, logout_user, login_required
import secrets
from datetime import datetime
from sqlalchemy import desc


@app.route("/")
def home():
    posts = Post.query.order_by(desc(Post.date)).all()
    return render_template("home.html", posts=posts, now=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                           datetime=datetime, current_user=current_user)


@app.route("/about")
def about():
    return render_template("about.html", title='about')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=hashed_pass)
            db.session.add(user)
            db.session.commit()
            flash(f"Account created successfully! Now you can login", 'success')
            return redirect(url_for("login"))
    return render_template("register.html", title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            correct_email = User.query.filter_by(email=form.email.data).first()
            if correct_email and bcrypt.check_password_hash(correct_email.password, form.password.data):
                login_user(correct_email, remember=form.remember_me.data)
                # get the next page if the user have tried to access any and was
                # redirected to login first
                next_page = request.args.get('next')
                flash("Logged in successfully", 'success')
                if next_page:
                    return redirect(next_page)
                return redirect(url_for("home"))
            else:
                flash("incorrect email or password!", "danger")
    return render_template("login.html", title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == "POST":
        return redirect(url_for('change_profile'))
    image_f = url_for('static', filename='profile_pics/' + current_user.profile_image)
    return render_template("profile.html", title=f"profile - {current_user.username}",
                           profile_image=image_f, change_profile=True, hide_side_bar=True,
                           now=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                           datetime=datetime,
                           posts=Post.query.filter_by(user_id=current_user.id).all())


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
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_file)
    # delete the picture
    os.remove(picture_path)


@app.route("/change_profile_info", methods=['POST', 'GET'])
@login_required
def change_profile():
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
            if form.new_username.data != current_user.username:
                current_user.username = form.new_username.data
                flash("Your username has been updated successfully", "success")
            db.session.commit()
            return redirect(url_for('profile'))
    # set the value of the new username to the current username
    form.new_username.data = current_user.username
    image_f = url_for('static', filename='profile_pics/' + current_user.profile_image)
    return render_template("edit_profile.html", title="Edit Profile",
                           profile_image=image_f, form=form, hide_side_bar=True)


@app.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = AddPostForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            post = Post(title=form.title.data, content=form.content.data, author=current_user)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('home'))
    return render_template("add_post.html", title="Add New Post", form=form)


@app.route("/delete_post/<int:post_id>")
def delete_post(post_id):
    pass


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
def edit_post(post_id):
    pass
