from flask import render_template, request, Blueprint, redirect, url_for
from flask_login import current_user, login_required
from datetime import datetime
from sqlalchemy import desc
from blog.model import Post, User
from time import ctime

main = Blueprint('main', __name__)


@main.route("/")
def index():
    # start the journey from by login
    return redirect(url_for("users.login"))


@main.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    # get the current page, and put a default value of 1
    current_page = request.args.get('current_page', 1, type=int)
    posts = Post.query.order_by(desc(Post.date)).paginate(page=current_page, per_page=6)
    return render_template("home.html", posts=posts, now=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                           datetime=datetime, current_user=current_user, time=ctime())


@main.route("/about")
def about():
    return render_template("about.html", title='about')


@main.route('/results/', methods=['POST'])
@login_required
def search():
    search_text = request.form['search_value']
    users = User.query.filter(User.username.ilike(f"%{search_text}%")).all()
    posts = Post.query.filter(Post.title.ilike(f"%{search_text}%")).all()
    return render_template("search_results.html", users=users, posts=posts,
                           now=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                           datetime=datetime, current_user=current_user)
