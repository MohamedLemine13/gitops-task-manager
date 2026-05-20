from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import db, Task
from config import Config


def create_app(config_class=Config):
    """Application factory."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    # ──────────────────────────── Routes ────────────────────────────

    @app.route("/")
    def index():
        """Display all tasks."""
        tasks = Task.query.order_by(Task.created_at.desc()).all()
        return render_template("index.html", tasks=tasks)

    @app.route("/tasks", methods=["POST"])
    def add_task():
        """Add a new task."""
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()

        if title:
            task = Task(title=title, description=description, status="TODO")
            db.session.add(task)
            db.session.commit()

        return redirect(url_for("index"))

    @app.route("/tasks/<int:task_id>/status", methods=["POST"])
    def update_status(task_id):
        """Cycle the task status: TODO → IN_PROGRESS → DONE → TODO."""
        task = Task.query.get_or_404(task_id)

        cycle = {"TODO": "IN_PROGRESS", "IN_PROGRESS": "DONE", "DONE": "TODO"}
        task.status = cycle.get(task.status, "TODO")
        db.session.commit()

        return redirect(url_for("index"))

    @app.route("/tasks/<int:task_id>/delete", methods=["POST"])
    def delete_task(task_id):
        """Delete a task."""
        task = Task.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()

        return redirect(url_for("index"))

    @app.route("/health")
    def health():
        """Health-check endpoint for CI/CD probes."""
        return jsonify({"status": "ok"}), 200

    return app


# ──────────────────────────── Entry point ────────────────────────────

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
