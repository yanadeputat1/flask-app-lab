
from app.extensions import db
from app.posts.models import post_tags


class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(50),
        nullable=False,
        unique=True
    )

    posts = db.relationship(
        "Post",
        secondary=post_tags,
        back_populates="tags"
    )

    def __repr__(self):
        return f"<Tag {self.name}>"
