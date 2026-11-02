
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    SubmitField,
    SelectField,
    DecimalField,
    IntegerField,
    FileField
)
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    NumberRange,
    Regexp
)


class ContactForm(FlaskForm):
    name = StringField(
        "Ім'я",
        validators=[
            DataRequired(message="Введіть ім'я."),
            Length(
                min=4,
                max=10,
                message="Ім'я має містити від 4 до 10 символів."
            )
        ]
    )

    email = StringField(
        "Електронна пошта",
        validators=[
            DataRequired(message="Введіть електронну пошту."),
            Email(message="Введіть правильну електронну пошту.")
        ]
    )

    phone = StringField(
        "Телефон",
        validators=[
            DataRequired(message="Введіть номер телефону."),
            Regexp(
                r"^\+380\d{9}$",
                message="Введіть номер у форматі +380XXXXXXXXX."
            )
        ]
    )

    subject = SelectField(
        "Тема звернення",
        choices=[
            ("question", "Запитання"),
            ("support", "Технічна підтримка"),
            ("cooperation", "Співпраця"),
            ("other", "Інше")
        ],
        validators=[
            DataRequired(message="Оберіть тему звернення.")
        ]
    )

    message = TextAreaField(
        "Повідомлення",
        validators=[
            DataRequired(message="Введіть повідомлення."),
            Length(
                max=500,
                message="Повідомлення не повинно перевищувати 500 символів."
            )
        ]
    )

    submit = SubmitField("Надіслати")


class ProductForm(FlaskForm):
    name = StringField(
        "Назва товару",
        validators=[
            DataRequired(message="Введіть назву товару."),
            Length(
                min=3,
                message="Назва має містити щонайменше 3 символи."
            )
        ]
    )

    content = TextAreaField(
        "Опис товару",
        validators=[
            DataRequired(message="Введіть опис товару."),
            Length(
                min=1,
                max=2000,
                message="Опис не повинен перевищувати 2000 символів."
            )
        ]
    )

    price = DecimalField(
        "Ціна",
        places=2,
        validators=[
            DataRequired(message="Введіть ціну."),
            NumberRange(
                min=0.01,
                message="Ціна має бути більшою за 0."
            )
        ]
    )

    category = SelectField(
        "Категорія",
        choices=[
            ("Електроніка", "Електроніка"),
            ("Одяг", "Одяг"),
            ("Книги", "Книги"),
            ("Інше", "Інше")
        ],
        validators=[
            DataRequired(message="Оберіть категорію.")
        ]
    )

    quantity = IntegerField(
        "Кількість",
        validators=[
            DataRequired(message="Введіть кількість."),
            NumberRange(
                min=0,
                message="Кількість не може бути від'ємною."
            )
        ]
    )

    image = FileField("Зображення товару")

    submit = SubmitField("Зберегти товар")
