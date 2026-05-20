import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration."""
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:00000000@localhost:5432/gitops_tasks"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")


class TestingConfig(Config):
    """Testing configuration – uses SQLite in-memory for fast, isolated tests."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
