from . import db
from .models import User
from flask import Blueprint, render_template, redirect, request, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(
            username=username
        ).scalar()

        if user:
            if check_password_hash(user.password, password):
                flash("Login successful!", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.index"))
            else:
                flash(
                    "Incorrect username or password! Please try again.",
                    category="error"
                )
        else:
            flash(
                "Incorrect username or password! Please try again.",
                category="error"
            )

    return render_template("login.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password_confirm = request.form.get("password_confirm")

        user = User.query.filter_by(
            username=username
        ).first()

        if user:
            flash(
                "Username already exists!",
                category="error"
            )
        elif len(username) < 4:
            flash(
                "Username must be at least 4 characters long!",
                category="error"
            )
        elif len(password) < 4:
            flash(
                "Password must be at least 4 characters long!",
                category="error"
            )

        elif password != password_confirm:
            flash(
                "Passwords do not match!",
                category="error"
            )
        else:
            new_user = User(
                username=username,
                password=generate_password_hash(
                    password,
                    method="sha256"
                ),
            )
            db.session.add(new_user)
            db.session.commit()
            flash(
                "Account created!",
                category="success"
            )
            login_user(user, remember=True)
            return redirect(url_for("views.index"))

    return render_template("signup.html")
