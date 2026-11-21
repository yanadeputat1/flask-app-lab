
from flask import render_template, redirect, url_for, request, flash
from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from app.users import users
from app.forms import RegistrationForm
from app.users.models import User
from app.extensions import db


# Реєстрація
@users.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.username.data.strip()
        email = form.email.data.strip()

        existing_username = User.query.filter_by(
            username=username
        ).first()

        if existing_username:
            flash("Це ім'я користувача вже зареєстроване.", "error")
            return redirect(url_for("users.register"))

        existing_email = User.query.filter_by(
            email=email
        ).first()

        if existing_email:
            flash("Ця електронна пошта вже зареєстрована.", "error")
            return redirect(url_for("users.register"))

        user = User(username=username, email=email)
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash("Реєстрація успішна! Ви увійшли в акаунт.", "success")

        return redirect(url_for("users.account"))

    return render_template(
        "users/register.html",
        title="Реєстрація",
        form=form
    )


# Вхід
@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("users.account"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash("Ви успішно увійшли!", "success")

            next_page = request.args.get("next")

            if next_page and next_page.startswith("/"):
                return redirect(next_page)

            return redirect(url_for("users.account"))

        flash("Неправильний логін або пароль.", "error")
        return redirect(url_for("users.login"))

    return render_template("users/login.html", title="Вхід")


# Сторінка профілю за вимогою методички: /account
@users.route("/account")
@login_required
def account():
    return render_template(
        "users/account.html",
        title="Мій профіль",
        user=current_user
    )


# Додаткова адреса профілю для сумісності зі старими посиланнями
@users.route("/profile")
@login_required
def profile():
    return redirect(url_for("users.account"))


# Вихід
@users.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    flash("Ви вийшли з акаунта.", "success")
    return redirect(url_for("users.login"))


# Список користувачів
@users.route("/users")
@login_required
def users_list():
    all_users = User.query.all()

    return render_template(
        "users/users.html",
        title="Користувачі",
        users=all_users
    )


# Привітання
@users.route("/hi/<name>")
def hi(name):
    return render_template(
        "users/hi.html",
        title="Привітання",
        name=name
    )


# Адмін-сторінка
@users.route("/admin")
def admin():
    return render_template(
        "users/profile.html",
        title="Адміністратор",
        user=current_user
    )


# Cookies
@users.route("/cookies")
@login_required
def cookies():
    return render_template(
        "users/profile.html",
        title="Cookies",
        user=current_user
    )


@users.route("/cookies/add", methods=["GET", "POST"])
@login_required
def add_cookie():
    response = redirect(url_for("users.cookies"))

    if request.method == "POST":
        key = request.form.get("key", "user").strip()
        value = request.form.get("value", str(current_user.username))
        days = request.form.get("days", "7")

        if not key or key in ["session", "csrf_token"]:
            flash("Некоректна назва cookie.", "error")
            return response

        try:
            max_age = int(days) * 24 * 60 * 60

            if max_age <= 0:
                raise ValueError

        except (ValueError, TypeError):
            flash("Кількість днів має бути додатним числом.", "error")
            return response

        response.set_cookie(
            key,
            value,
            max_age=max_age,
            httponly=True,
            samesite="Lax"
        )

        flash("Cookie успішно створено.", "success")
        return response

    response.set_cookie(
        "user",
        current_user.username,
        max_age=7 * 24 * 60 * 60
    )

    flash("Cookie успішно створено.", "success")
    return response


@users.route("/cookies/delete", methods=["GET", "POST"])
@login_required
def delete_cookie():
    key = (
        request.form.get("key", "user")
        if request.method == "POST"
        else "user"
    )

    response = redirect(url_for("users.cookies"))
    response.delete_cookie(key)

    flash("Cookie видалено.", "success")
    return response


@users.route("/cookies/delete-all", methods=["GET", "POST"])
@login_required
def delete_all_cookies():
    response = redirect(url_for("users.cookies"))

    for key in request.cookies:
        if key not in ["session", "csrf_token"]:
            response.delete_cookie(key)

    flash("Cookies видалено.", "success")
    return response


# Зміна теми
@users.route("/theme/<theme>")
def theme(theme):
    if theme not in ["light", "dark"]:
        theme = "light"

    response = redirect(
        request.referrer or url_for("users.account")
    )

    response.set_cookie("theme", theme)
    return response


@users.route("/change-theme/<theme>")
def change_theme(theme):
    return redirect(url_for("users.theme", theme=theme))

