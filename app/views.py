from . import db
from .models import Task
from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_required, current_user

views = Blueprint("views", __name__)


@views.route("/", methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        task_content = request.form['content']

        if len(task_content) < 1:
            flash(
                "Task must contain at least 1 character!",
                category="error"
            )
        else:
            new_task = Task(content=task_content, user_id=current_user.id)

            db.session.add(new_task)
            db.session.commit()

            flash("Task created successfully!", category="success")

        return redirect(url_for("views.index"))

    else:
        tasks = Task.query.filter_by(
            user_id=current_user.id
        ).order_by(
            Task.date_created
        ).all()

        return render_template("index.html", tasks=tasks, user=current_user)


@views.route("/delete/<int:id>")
def delete(id):
    task_to_delete = Task.query.get_or_404(id)

    if task_to_delete.user_id == current_user.id:
        db.session.delete(task_to_delete)
        db.session.commit()
        flash("Task deleted successfully!", category="success")
    else:
        flash("Cannot delete task without authorization!", category="error")

    return redirect(url_for("views.index"))


@views.route("/update/<int:id>", methods=['GET', 'POST'])
def update(id):
    task_to_update = Task.query.get_or_404(id)

    if request.method == 'POST':
        task_to_update.content = request.form['content']

        db.session.commit()

        flash("Task updated successfully!", category="success")

        return redirect(url_for("views.index"))

    else:
        return render_template(
            "update.html",
            task=task_to_update,
            user=current_user
        )
