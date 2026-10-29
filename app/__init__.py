
import os
from flask import Flask, flash, redirect, request, url_for

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY")

if not app.secret_key:
    raise RuntimeError(
        "Не задано SECRET_KEY для Flask"
    )

# Максимальний розмір запиту — 6 МБ
app.config["MAX_CONTENT_LENGTH"] = 6 * 1024 * 1024


@app.errorhandler(413)
def request_entity_too_large(error):
    flash(
        "Файл завеликий. Максимальний розмір зображення — 5 МБ.",
        "error"
    )

    if request.referrer:
        return redirect(request.referrer)

    return redirect(url_for("products.add_product"))


from app import views
from app.users import users
from app.products import products

app.register_blueprint(users)
app.register_blueprint(products)
