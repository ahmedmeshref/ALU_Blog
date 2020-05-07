from flask import render_template, url_for, request, flash, redirect, abort, jsonify
from blog import db
from blog.posts.forms import UpdatePostForm
from blog.model import Post
from flask_login import current_user, login_required
from datetime import datetime
from flask import Blueprint

posts = Blueprint('posts', __name__)


@posts.route("/new_post", methods=["POST"])
@login_required
def new_post():
    title = request.get_json()['title']
    description = request.get_json()['description']
    try:
        new_post = Post(title=title, content=description, author=current_user)
        db.session.add(new_post)
        db.session.commit()
        return jsonify({
            'id': new_post.id,
            'title': new_post.title,
            'description': new_post.content,
            'profile_image': new_post.author.profile_image,
            'username': new_post.author.username,
            'author_id': new_post.author.id
        })
    except:
        db.rollback()
        abort(500)

@posts.route("/post/<int:post_id>")
def show_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post:
        return render_template('show_post.html', post=post, now=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                               datetime=datetime, current_user=current_user)
    else:
        return abort(404)


def validate_post(post_id):
    # check if post exists or not
    post = Post.query.get_or_404(post_id)
    # check if current user is the author or the current user is an admin and the author is an end user
    if (post.author == current_user) or (current_user.admin == 1 and post.author.admin == 0):
        return post
    abort(403)


@posts.route("/posts/delete_post", methods=['POST'])
@login_required
def delete_post():
    post_id = request.get_json()['post_id']
    post = validate_post(post_id)
    data = jsonify({
        'post_id': post.id,
        'title': post.title
    })
    db.session.delete(post)
    db.session.commit()
    return data


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = validate_post(post_id)
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
