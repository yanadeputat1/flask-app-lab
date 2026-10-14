
from flask import render_template, redirect, url_for, request
from app.users import users


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
    return redirect(url_for("users.greetings", name="Administrator", age=45))
