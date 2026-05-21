"""
Tests for GitOps Task Manager.

Uses an in-memory SQLite database so PostgreSQL is NOT required to run tests.
"""

import pytest
from app import create_app
from config import TestingConfig
from models import db as _db


@pytest.fixture()
def app():
    """Create and configure a test application instance."""
    app = create_app(TestingConfig)
    yield app


@pytest.fixture()
def client(app):
    """Provide a Flask test client."""
    return app.test_client()


@pytest.fixture(autouse=True)
def init_db(app):
    """Ensure a fresh database for every test."""
    with app.app_context():
        _db.create_all()
        yield
        _db.session.remove()
        _db.drop_all()


# ──────────────────────────── Tests ────────────────────────────


class TestHealthEndpoint:
    """Health-check endpoint."""

    def test_health_returns_ok(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "ok"


class TestIndexPage:
    """Main page rendering."""

    def test_index_returns_200(self, client):
        response = client.get("/")
        assert response.status_code == 200

    def test_index_contains_title(self, client):
        response = client.get("/")
        assert b"GitOps Task Manager" in response.data

class TestTaskCRUD:
    """Task creation, status update and deletion."""

    def test_add_task(self, client):
        response = client.post(
            "/tasks",
            data={"title": "Test Task", "description": "A test task"},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Test Task" in response.data

    def test_add_task_empty_title_ignored(self, client):
        """Submitting an empty title should not create a task."""
        client.post("/tasks", data={"title": "", "description": ""}, follow_redirects=True)
        response = client.get("/")
        assert b"task-card" not in response.data

    def test_update_status(self, client):
        # Create a task first
        client.post(
            "/tasks",
            data={"title": "Status Test", "description": ""},
            follow_redirects=True,
        )
        # Cycle status: TODO → IN_PROGRESS
        response = client.post("/tasks/1/status", follow_redirects=True)
        assert response.status_code == 200
        assert "En cours".encode() in response.data

    def test_delete_task(self, client):
        # Create then delete
        client.post(
            "/tasks",
            data={"title": "Delete Me", "description": ""},
            follow_redirects=True,
        )
        response = client.post("/tasks/1/delete", follow_redirects=True)
        assert response.status_code == 200
        assert b"Delete Me" not in response.data

    def test_delete_nonexistent_task_returns_404(self, client):
        response = client.post("/tasks/999/delete")
        assert response.status_code == 404
