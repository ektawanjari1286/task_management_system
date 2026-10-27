from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from extensions import db
from models.task import Task
from models.task_step import TaskStep


task_bp = Blueprint(
    "tasks",
    __name__
)




def generate_task_steps(task):

    
    TaskStep.query.filter_by(
        task_id=task.id
    ).delete()

    
    step_titles = [
        "Understand the task requirements",
        "Collect required study material",
        "Plan and organize the work",
        "Work on the main task",
        "Practice and verify the work",
        "Review and correct mistakes",
        "Complete final revision"
    ]

    for index, title in enumerate(step_titles, start=1):

        step = TaskStep(
            task_id=task.id,
            step_number=index,
            title=title,
            completed=False
        )

        db.session.add(step)

    db.session.commit()




@task_bp.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():

    if request.method == "POST":

        title = request.form.get("title")
        description = request.form.get("description")
        priority = request.form.get("priority", "Medium")
        deadline = request.form.get("deadline")

        if not title:

            flash(
                "Task title is required.",
                "danger"
            )

            return redirect(
                url_for("tasks.dashboard")
            )

        task = Task(
            title=title,
            description=description,
            priority=priority,
            user_id=current_user.id
        )

        
        if deadline:

            from datetime import datetime

            try:

                task.deadline = datetime.strptime(
                    deadline,
                    "%Y-%m-%d"
                )

            except ValueError:

                task.deadline = None

        db.session.add(task)

        db.session.commit()

        
        generate_task_steps(task)

        flash(
            "Task created successfully. Steps were generated automatically!",
            "success"
        )

        return redirect(
            url_for("tasks.dashboard")
        )

    
    tasks = Task.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Task.id.desc()
    ).all()

  
    for task in tasks:

        task.update_status()

    db.session.commit()

    return render_template(
        "dashboard.html",
        tasks=tasks
    )


@task_bp.route(
    "/task/<int:task_id>/step/<int:step_id>/complete",
    methods=["POST"]
)
@login_required
def complete_step(task_id, step_id):

    task = Task.query.filter_by(
        id=task_id,
        user_id=current_user.id
    ).first_or_404()

    step = TaskStep.query.filter_by(
        id=step_id,
        task_id=task.id
    ).first_or_404()

    step.completed = True

    from datetime import datetime

    step.completed_at = datetime.utcnow()

    task.update_status()

    db.session.commit()

    return redirect(
        url_for("tasks.dashboard")
    )


@task_bp.route(
    "/task/<int:task_id>/step/<int:step_id>/undo",
    methods=["POST"]
)
@login_required
def undo_step(task_id, step_id):

    task = Task.query.filter_by(
        id=task_id,
        user_id=current_user.id
    ).first_or_404()

    step = TaskStep.query.filter_by(
        id=step_id,
        task_id=task.id
    ).first_or_404()

    step.completed = False
    step.completed_at = None

    task.update_status()

    db.session.commit()

    return redirect(
        url_for("tasks.dashboard")
    )


@task_bp.route(
    "/task/<int:task_id>/delete",
    methods=["POST"]
)
@login_required
def delete_task(task_id):

    task = Task.query.filter_by(
        id=task_id,
        user_id=current_user.id
    ).first_or_404()

    db.session.delete(task)

    db.session.commit()

    flash(
        "Task deleted successfully.",
        "success"
    )

    return redirect(
        url_for("tasks.dashboard")
    )