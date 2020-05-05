from flask import render_template, url_for, request, flash, redirect, abort, jsonify
from blog import db
from blog.posts.forms import UpdatePostForm
from blog.model import Post
from flask_login import current_user, login_required
from datetime import datetime
from flask import Blueprint

posts = Blueprint('posts', __name__)


@posts.route("/new_post/", methods=["POST"])
@login_required
def new_post():
    title = request.get_json()['title']
    description = request.get_json()['description']
    error = False
    data = {}
    new_post = Post(title=title, content=description, author=current_user)
    db.session.add(new_post)
    db.session.commit()
    data['description'] = description
    data['title'] = title
    return jsonify(data)


@posts.route("/post/<int:post_id>")
def show_post(post_id):
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
def update_post(post_id):
    # check if post exists or not
    post = Post.query.get_or_404(post_id)
    # check if current user is the author or the current user is an admin and the author is an end user
    if (post.author != current_user) or not (current_user.admin == 1 and not post.author.admin):
        abort(403)
    # use the add post form to update the post
    form = UpdatePostForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            # check if the user updated any data
            if post.title != form.title.data or post.content != form.content.data:
                post.title = form.title.data
                post.content = form.content.data
                db.session.commit()
                flash("Updated successfully", "success")
            return redirect(url_for('posts.show_post',post_id=post.id))
    form.title.data = post.title
    form.content.data = post.content
    return render_template("update_post.html", title="Update Post", form=form)
