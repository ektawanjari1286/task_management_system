from datetime import datetime

from extensions import db


class TaskStep(db.Model):

    __tablename__ = "task_step"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    task_id = db.Column(
        db.Integer,
        db.ForeignKey("task.id"),
        nullable=False
    )

    step_number = db.Column(
        db.Integer,
        nullable=False
    )

    title = db.Column(
        db.String(255),
        nullable=False
    )

    completed = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    completed_at = db.Column(
        db.DateTime,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )