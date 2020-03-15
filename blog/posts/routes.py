from flask import render_template, url_for, request, flash, redirect, abort
from blog import db
from blog.posts.forms import AddPostForm
from blog.model import Post
from flask_login import current_user, login_required
from datetime import datetime
from flask import Blueprint

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = AddPostForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            post = Post(title=form.title.data, content=form.content.data, author=current_user)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('main.home'))
    return render_template("add_post.html", title="Add New Post", form=form, legend="Add New Post")


@posts.route("/post/<username>/<int:post_id>")
def show_post(username, post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post:
        return render_template('show_post.html', post=post, now=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                               datetime=datetime, current_user=current_user)
    else:
        return abort(404)


@posts.route("/post/<post_id>/delete/", methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    # check if post exists or not
    post = Post.query.get_or_404(post_id)
    # check if a user is using the url to update someone else's post
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Deleted Successfully", "success")
    return redirect(url_for('main.home'))


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    # check if post exists or not
    post = Post.query.get_or_404(post_id)
    # check if a user is using the url to update someone else's post
    if post.author != current_user:
        abort(403)
    # use the add post form to update the post
    form = AddPostForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            # check if the user updated any data
            if post.title != form.title.data or post.content != form.content.data:
                post.title = form.title.data
                post.content = form.content.data
                db.session.commit()
                flash("Updated successfully", "success")
            return redirect(url_for('posts.show_post', username=post.author.username,
                                    post_id=post.id))
    form.title.data = post.title
    form.content.data = post.content
    return render_template("add_post.html", title="Update Post", form=form, legend="Update Post")
