
from datetime import datetime
from enum import Enum

from app.extensions import db


class PostCategory(Enum):
    NEWS = "news"
    PUBLICATION = "publication"
    TECH = "tech"
    OTHER = "other"


# Проміжна таблиця для зв'язку Many-to-Many
post_tags = db.Table(
    "post_tags",
    db.Column(
        "post_id",
        db.Integer,
        db.ForeignKey("post.id"),
        primary_key=True
    ),
    db.Column(
        "tag_id",
        db.Integer,
        db.ForeignKey("tags.id"),
        primary_key=True
    )
)


class Post(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(150),
        nullable=False
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    # Назва файлу фотографії
    image = db.Column(
        db.String(255),
        nullable=True
    )

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

    # Зв'язок Post → User
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    user = db.relationship(
        "User",
        back_populates="posts"
    )

    # Зв'язок Post ↔ Tag
    tags = db.relationship(
        "Tag",
        secondary=post_tags,
        back_populates="posts"
    )

    def __repr__(self):
        return f"<Post {self.title}>"
