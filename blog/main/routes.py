from flask import render_template, request, Blueprint, redirect, url_for
from flask_login import current_user, login_required
from datetime import datetime
from sqlalchemy import desc
from blog.main.forms import SearchForm
from blog.model import Post, User

main = Blueprint('main', __name__)


@main.route("/")
def index():
    # start the journey from by login
    return redirect(url_for("users.login"))


@main.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    search_form = SearchForm()
    # get the current page, and put a default value of 1
    current_page = request.args.get('current_page', 1, type=int)
    posts = Post.query.order_by(desc(Post.date)).paginate(page=current_page, per_page=6)
    return render_template("home.html", posts=posts, now=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                           datetime=datetime, current_user=current_user, search_form=search_form)


@main.route("/about")
def about():
    search_form = SearchForm()
    if search_form.search.data:
        return redirect(url_for('main.search', search_text=search_form.search.data))
    return render_template("about.html", title='about', search_form=search_form)


@main.route('/search/<search_text>', methods=['GET', 'POST'])
def search(search_text):
    search_form = SearchForm()
    users = User.query.filter(User.username.ilike(f"%{search_text}%")).all()
    posts = Post.query.filter(Post.title.ilike(f"%{search_text}%")).all()
    return render_template("search_results.html", users=users, posts=posts,
                           now=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                           datetime=datetime, current_user=current_user, search_form=search_form)
