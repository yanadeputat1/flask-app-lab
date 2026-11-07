
import os

from dotenv import load_dotenv
from flask import Flask, flash, redirect, request, url_for

from app.config import config
from app.extensions import db, migrate, csrf

load_dotenv()


def create_app(config_name=None):
    app = Flask(__name__)

    if config_name is None:
        config_name = os.getenv("FLASK_CONFIG", "development")

    app.config.from_object(config[config_name])

    # Обмеження розміру запиту — 6 МБ
    app.config["MAX_CONTENT_LENGTH"] = 6 * 1024 * 1024

    # Підключення SQLAlchemy
    db.init_app(app)

    # Підключення Flask-WTF CSRF
    csrf.init_app(app)

    # Підключення Flask-Migrate
    migrate.init_app(app, db)

    # Реєстрація основних маршрутів
    from app.views import register_routes
    register_routes(app)

    # Реєстрація Blueprints
    from app.users import users
    from app.products import products
    from app.posts import post_bp

    app.register_blueprint(users)
    app.register_blueprint(products)
    app.register_blueprint(post_bp)

    # Імпорт моделі для Flask-Migrate
    from app.posts.models import Post

    # Обробка завеликого запиту
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
