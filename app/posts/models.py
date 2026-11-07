from datetime import datetime
from enum import Enum

from app.extensions import db


class PostCategory(Enum):
    NEWS = "news"
    PUBLICATION = "publication"
    TECH = "tech"
    OTHER = "other"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(150), nullable=False)

    content = db.Column(db.Text, nullable=False)

    posted = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    category = db.Column(
        db.Enum(
            PostCategory,
            values_callable=lambda categories: [
                category.value for category in categories
            ],
            native_enum=False
        ),
        nullable=False,
        default=PostCategory.OTHER
    )

    is_active = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    author = db.Column(
        db.String(20),
        default="Anonymous",
        nullable=False
    )

    def __repr__(self):
        return f"<Post {self.title}>"