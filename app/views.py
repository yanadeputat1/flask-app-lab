
from app import app
from flask import render_template, redirect, url_for, flash
from app.forms import ContactForm
from datetime import datetime


@app.route("/")
def home():
    return render_template("homepage.html", title="Головна")


@app.route("/contacts", methods=["GET", "POST"])
def contacts():
    form = ContactForm()

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        subject = form.subject.data
        message = form.message.data

        with open("contacts.log", "a", encoding="utf-8") as file:
            file.write(
                f"{datetime.now()} | Ім'я: {name} | "
                f"Email: {email} | Тема: {subject} | "
                f"Повідомлення: {message}\n"
            )

        flash("Ваше повідомлення успішно надіслано!", "success")
        return redirect(url_for("contacts"))

    return render_template(
        "contacts.html",
        title="Контакти",
        form=form
    )


@app.route("/resume")
def resume():
    return render_template("resume.html", title="Резюме")
