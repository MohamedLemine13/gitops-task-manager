from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Task(db.Model):
    """Represents a task in the GitOps Task Manager."""

    __tablename__ = "tasks"

    VALID_STATUSES = ("TODO", "IN_PROGRESS", "DONE")

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True, default="")
    status = db.Column(db.String(20), nullable=False, default="TODO")
    created_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
        }

    def __repr__(self):
        return f"<Task {self.id}: {self.title} [{self.status}]>"
