from flask import render_template, url_for, request, flash, redirect
from blog import app, db, bcrypt
from blog.forms import RegistrationForm, LoginForm
from blog.model import User, Post
from flask_login import login_user, current_user, logout_user, login_required

posts = [
    {
        "author": "Ahmed Meshref",
        "date_posted": "12/05/2019",
        "title": "Facilitators are bad",
        "content": "I need my tuition back!!"
    }
]


@app.route("/")
def home():
    return render_template("home.html", posts=posts)


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
                flash("incorrect Email or password", "danger")
    return render_template("login.html", title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/profile")
@login_required
def profile():
    profile_image = url_for('static', filename='profile.png')
    return render_template("profile.html", title="Account", profile_image=profile_image)
