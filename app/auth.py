from flask import Blueprint, render_template, redirect, request, flash
from . import db
from .models import Users

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    return render_template("login.html")


@auth.route("/logout")
def logout():
    return redirect("/")


@auth.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password_confirm = request.form.get("password_confirm")

        exists = db.session.query(
            Users.id
        ).filter_by(
            username=username
        ).first() is not None

        if len(username) < 4:
            flash(
                "Username must be at least 4 characters long!",
                category="error"
            )
        elif len(password) < 4:
            flash(
                "Password must be at least 4 characters long!",
                category="error"
            )
        elif exists:
            flash(
                "Username already exists!",
                category="error"
            )
        elif password != password_confirm:
            flash(
                "Passwords do not match!",
                category="error"
            )
        else:
            flash(
                "Account created!",
                category="success"
            )
            new_user = Users(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()

            return redirect("/")

    return render_template("signup.html")
