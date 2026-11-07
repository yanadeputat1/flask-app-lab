from datetime import datetime

from flask import render_template, redirect, url_for, flash, request

from app.extensions import db
from app.posts import post_bp
from app.posts.models import Post, PostCategory
from app.posts.forms import PostForm


@post_bp.route("/create", methods=["GET", "POST"])
def create_post():
    form = PostForm()

    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            posted=form.publish_date.data or datetime.utcnow(),
            category=PostCategory(form.category.data),
            is_active=form.enabled.data,
            author="Anonymous"
        )

        db.session.add(post)
        db.session.commit()

        flash("Допис успішно додано!", "success")
        return redirect(url_for("posts.all_posts"))

    return render_template(
        "posts/add_post.html",
        title="Створення допису",
        form=form
    )


@post_bp.route("/")
def all_posts():
    posts = Post.query.order_by(Post.posted.desc()).all()

    return render_template(
        "posts/all_posts.html",
        title="Усі дописи",
        posts=posts
    )


@post_bp.route("/<int:post_id>")
def detail_post(post_id):
    post = db.get_or_404(Post, post_id)

    return render_template(
        "posts/detail_post.html",
        title=post.title,
        post=post
    )


@post_bp.route("/<int:post_id>/update", methods=["GET", "POST"])
def update_post(post_id):
    post = db.get_or_404(Post, post_id)
    form = PostForm(obj=post)

    if request.method == "GET":
        form.enabled.data = post.is_active
        form.publish_date.data = post.posted
        form.category.data = post.category.value

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.posted = form.publish_date.data or datetime.utcnow()
        post.category = PostCategory(form.category.data)
        post.is_active = form.enabled.data

        db.session.commit()

        flash("Допис успішно оновлено!", "success")
        return redirect(url_for("posts.detail_post", post_id=post.id))

    return render_template(
        "posts/add_post.html",
        title="Редагування допису",
        form=form
    )


@post_bp.route("/<int:post_id>/delete", methods=["GET", "POST"])
def delete_post(post_id):
    post = db.get_or_404(Post, post_id)

    if request.method == "POST":
        db.session.delete(post)
        db.session.commit()

        flash("Допис успішно видалено!", "success")
        return redirect(url_for("posts.all_posts"))

    return render_template(
        "posts/delete_confirm.html",
        title="Видалення допису",
        post=post
    )