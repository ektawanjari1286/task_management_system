from datetime import datetime

from extensions import db


class Task(db.Model):

    __tablename__ = "task"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(
        db.String(200),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    priority = db.Column(
        db.String(20),
        default="Medium",
        nullable=False
    )

    deadline = db.Column(
        db.DateTime,
        nullable=True
    )

    status = db.Column(
        db.String(20),
        default="Pending",
        nullable=False
    )

    completed = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    steps = db.relationship(
        "TaskStep",
        backref="task",
        lazy=True,
        cascade="all, delete-orphan",
        order_by="TaskStep.step_number"
    )

    def get_progress(self):
        """
        Automatically calculates task progress.
        """

        total_steps = len(self.steps)

        if total_steps == 0:
            return 0

        completed_steps = sum(
            1 for step in self.steps
            if step.completed
        )

        return int(
            (completed_steps / total_steps) * 100
        )

    def update_status(self):
        """
        Automatically updates task status
        according to step completion.
        """

        total_steps = len(self.steps)

        if total_steps == 0:
            self.status = "Pending"
            self.completed = False
            return

        completed_steps = sum(
            1 for step in self.steps
            if step.completed
        )

        if completed_steps == total_steps:

            self.status = "Completed"
            self.completed = True

        elif completed_steps > 0:

            self.status = "In Progress"
            self.completed = False

        else:

            self.status = "Pending"
            self.completed = False