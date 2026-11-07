from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    SelectField,
    BooleanField,
    SubmitField
)
from wtforms.fields import DateTimeLocalField
from wtforms.validators import DataRequired, Length, Optional


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

    submit = SubmitField("Зберегти")