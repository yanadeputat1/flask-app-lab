
from functools import wraps

from flask import (
    render_template,
    redirect,
    url_for,
    request,
    session,
    flash
)

from app.users import users


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "username" not in session:
            flash("Спочатку увійдіть у свій акаунт.", "error")
            return redirect(url_for("users.login"))

        return func(*args, **kwargs)

    return wrapper


@users.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        if username == "student" and password == "12345":
            session.clear()
            session["username"] = username
            flash("Ви успішно увійшли!", "success")
            return redirect(url_for("users.profile"))

        flash("Неправильний логін або пароль.", "error")
        return redirect(url_for("users.login"))

    return render_template("users/login.html", title="Вхід")


@users.route("/profile")
@login_required
def profile():
    return render_template(
        "users/profile.html",
        title="Профіль",
        username=session["username"]
    )


@users.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("Ви вийшли з акаунта.", "success")
    return redirect(url_for("users.login"))

@users.route("/cookies/add", methods=["POST"])
@login_required
def add_cookie():
    key = request.form.get("key", "").strip()
    value = request.form.get("value", "").strip()
    days_text = request.form.get("days", "7").strip()

    if not key or not value:
        flash("Введіть назву та значення cookie.", "error")
        return redirect(url_for("users.profile"))

    if key.lower() in ("session", "theme"):
        flash("Цю назву cookie використовувати не можна.", "error")
        return redirect(url_for("users.profile"))

    try:
        days = int(days_text)
        if not 1 <= days <= 3650:
            raise ValueError
    except ValueError:
        flash("Термін дії має бути від 1 до 3650 днів.", "error")
        return redirect(url_for("users.profile"))

    response = redirect(url_for("users.profile"))
    response.set_cookie(
        key,
        value,
        max_age=days * 24 * 60 * 60,
        httponly=True,
        samesite="Lax"
    )

    flash("Cookie успішно додано.", "success")
    return response


@users.route("/cookies/delete", methods=["POST"])
@login_required
def delete_cookie():
    key = request.form.get("key", "").strip()

    if key.lower() in ("session", "theme"):
        flash("Цю cookie видаляти не можна.", "error")
        return redirect(url_for("users.profile"))

    if key not in request.cookies:
        flash("Cookie не знайдено.", "error")
        return redirect(url_for("users.profile"))

    response = redirect(url_for("users.profile"))
    response.delete_cookie(key)
    flash("Cookie видалено.", "success")
    return response


@users.route("/cookies/delete-all", methods=["POST"])
@login_required
def delete_all_cookies():
    response = redirect(url_for("users.profile"))

    for key in request.cookies:
        if key not in ("session", "theme"):
            response.delete_cookie(key)

    flash("Усі користувацькі cookies видалено.", "success")
    return response

@users.route("/hi/<name>")
def greetings(name):
    age = request.args.get("age", "")

    return render_template(
        "users/hi.html",
        name=name.upper(),
        age=age
    )


@users.route("/admin")
def admin():
    return redirect(
        url_for("users.greetings", name="Administrator", age=45)
    )

@users.route("/theme/<theme>", methods=["POST"])
@login_required
def change_theme(theme):
    if theme not in ("light", "dark"):
        flash("Невідома тема оформлення.", "error")
        return redirect(url_for("users.profile"))

    response = redirect(url_for("users.profile"))
    response.set_cookie(
        "theme",
        theme,
        max_age=365 * 24 * 60 * 60,
        httponly=True,
        samesite="Lax"
    )

    flash("Тему оформлення змінено.", "success")
    return response
