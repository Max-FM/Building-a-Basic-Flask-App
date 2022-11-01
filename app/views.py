from flask import Blueprint, render_template, request, redirect

from . import db
from .models import Todo

views = Blueprint("views", __name__)


@views.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        db.session.add(new_task)
        db.session.commit()
        return redirect("/")

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template("index.html", tasks=tasks)


@views.route("/delete/<int:id>")
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect("/")


@views.route("/update/<int:id>", methods=['GET', 'POST'])
def update(id):
    task_to_update = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task_to_update.content = request.form['content']

        db.session.commit()
        return redirect("/")

    else:
        return render_template("update.html", task=task_to_update)
