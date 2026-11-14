from pathlib import Path
from flask import Flask

from lab7_app.extensions import db, migrate


def create_app():
    app = Flask(__name__)

    project_root = Path(__file__).resolve().parent.parent
    instance_dir = project_root / "instance"
    instance_dir.mkdir(exist_ok=True)

    database_path = instance_dir / "lab7.sqlite"
    migrations_path = project_root / "migrations_lab7"

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"sqlite:///{database_path}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db, directory=str(migrations_path))

    from lab7_app.models import Product, Category

    @app.shell_context_processor
    def make_shell_context():
        return {
            "db": db,
            "Product": Product,
            "Category": Category
        }

    return app


app = create_app()