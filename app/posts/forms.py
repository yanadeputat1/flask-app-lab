
from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    TextAreaField,
    SelectField,
    SelectMultipleField,
    BooleanField,
    SubmitField
)

from wtforms.fields import DateTimeLocalField
from wtforms.validators import DataRequired, Length, Optional
from flask_wtf.file import FileField


class PostForm(FlaskForm):

    title = StringField(
        "Заголовок",
        validators=[
            DataRequired(message="Введіть заголовок"),
            Length(max=150)
        ]
    )

    content = TextAreaField(
        "Текст допису",
        validators=[
            DataRequired(message="Введіть текст допису")
        ]
    )

    image = FileField("Фотографія допису")

    enabled = BooleanField("Активний допис")

    publish_date = DateTimeLocalField(
        "Дата публікації",
        format="%Y-%m-%dT%H:%M",
        validators=[Optional()]
    )

    category = SelectField(
        "Категорія",
        choices=[
            ("news", "Новини"),
            ("publication", "Публікації"),
            ("tech", "Технології"),
            ("other", "Інше")
        ],
        validators=[DataRequired()]
    )

    author = SelectField(
        "Автор допису",
        coerce=int,
        validators=[DataRequired()]
    )

    tags = SelectMultipleField(
        "Теги",
        coerce=int,
        validators=[Optional()]
    )

    submit = SubmitField("Зберегти")
