
import os
import uuid
from datetime import datetime

from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    request,
    current_app
)

from werkzeug.utils import secure_filename

from app.extensions import db
from app.posts import post_bp
from app.posts.models import Post, PostCategory
from app.posts.forms import PostForm
from app.users.models import User
from app.tags.models import Tag


ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}


def fill_form_choices(form):
    users = db.session.scalars(
        db.select(User).order_by(User.username)
    ).all()

    tags = db.session.scalars(
        db.select(Tag).order_by(Tag.name)
    ).all()

    form.author.choices = [
        (user.id, user.username)
        for user in users
    ]

    form.tags.choices = [
        (tag.id, tag.name)
        for tag in tags
    ]


def save_post_image(file):
    if not file or not file.filename:
        return None

    filename = secure_filename(file.filename)
    extension = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(
            "Дозволені формати фотографій: PNG, JPG, JPEG, GIF, WEBP."
        )

    new_filename = f"{uuid.uuid4().hex}.{extension}"

    upload_folder = os.path.join(
        current_app.root_path,
        "static",
        "uploads",
        "posts"
    )

    os.makedirs(upload_folder, exist_ok=True)

    file.save(os.path.join(upload_folder, new_filename))

    return new_filename


@post_bp.route("/create", methods=["GET", "POST"])
def create_post():
    form = PostForm()
    fill_form_choices(form)

    if form.validate_on_submit():
        try:
            image_filename = save_post_image(form.image.data)
        except ValueError as error:
            flash(str(error), "error")
            return render_template(
                "posts/add_post.html",
                title="Створення допису",
                form=form
            )

        user = db.get_or_404(User, form.author.data)

        selected_tags = db.session.scalars(
            db.select(Tag).where(Tag.id.in_(form.tags.data))
        ).all() if form.tags.data else []

        post = Post(
            title=form.title.data,
            content=form.content.data,
            image=image_filename,
            posted=form.publish_date.data or datetime.utcnow(),
            category=PostCategory(form.category.data),
            is_active=form.enabled.data,
            user=user,
            tags=selected_tags
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

    fill_form_choices(form)

    if request.method == "GET":
        form.enabled.data = post.is_active
        form.publish_date.data = post.posted
        form.category.data = post.category.value
        form.author.data = post.user_id
        form.tags.data = [tag.id for tag in post.tags]

    if form.validate_on_submit():
        try:
            image_filename = save_post_image(form.image.data)
        except ValueError as error:
            flash(str(error), "error")
            return render_template(
                "posts/add_post.html",
                title="Редагування допису",
                form=form
            )

        selected_tags = db.session.scalars(
            db.select(Tag).where(Tag.id.in_(form.tags.data))
        ).all() if form.tags.data else []

        post.title = form.title.data
        post.content = form.content.data
        post.posted = form.publish_date.data or datetime.utcnow()
        post.category = PostCategory(form.category.data)
        post.is_active = form.enabled.data
        post.user = db.get_or_404(User, form.author.data)
        post.tags = selected_tags

        if image_filename:
            post.image = image_filename

        db.session.commit()

        flash("Допис успішно оновлено!", "success")

        return redirect(
            url_for("posts.detail_post", post_id=post.id)
        )

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
