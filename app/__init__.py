import os

from dotenv import load_dotenv
from flask import Flask, flash, redirect, request, url_for, render_template
from flask_login import login_required, current_user

from app.config import config
from app.extensions import db, migrate, csrf, bcrypt, login_manager

load_dotenv()


def create_app(config_name=None):
    app = Flask(__name__)

    if config_name is None:
        config_name = os.getenv("FLASK_CONFIG", "development")

    app.config.from_object(config[config_name])

    # Увімкнення журналювання SQL-запитів
    app.config["SQLALCHEMY_ECHO"] = True
    app.config["MAX_CONTENT_LENGTH"] = 6 * 1024 * 1024

    # Ініціалізація розширень
    db.init_app(app)
    csrf.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)

    # Налаштування Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = "users.login"
    login_manager.login_message = "Спочатку увійдіть у свій акаунт."
    login_manager.login_message_category = "error"

    from app.views import register_routes
    register_routes(app)

    from app.users import users
    from app.products import products
    from app.posts import post_bp

    app.register_blueprint(users)
    app.register_blueprint(products)
    app.register_blueprint(post_bp)

    # Сторінка профілю за вимогою лабораторної роботи: /account
    @app.route("/account")
    @login_required
    def account():
        return render_template(
            "users/account.html",
            title="Мій профіль",
            user=current_user
        )

    from app.posts.models import Post
    from app.users.models import User
    from app.tags.models import Tag

    # Завантаження користувача для Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        try:
            return db.session.get(User, int(user_id))
        except (ValueError, TypeError):
            return None

    @app.errorhandler(413)
    def request_entity_too_large(error):
        flash(
            "Файл завеликий. Максимальний розмір зображення — 5 МБ.",
            "error"
        )

        if request.referrer:
            return redirect(request.referrer)

        return redirect(url_for("products.add_product"))

    return app


app = create_app()
