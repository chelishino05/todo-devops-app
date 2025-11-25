"""
Extra tests to exercise edge cases and error paths.

This file is only here to increase coverage without changing
any of your existing application code.
"""

import os
import sys
import sqlite3

import pytest

# Make sure we can import from backend/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import settings
from database import TodoDatabase, DatabaseError
from models import TodoCreate, TodoUpdate
from main import app
from fastapi.testclient import TestClient


def test_settings_basic_defaults():
    """Ensure Settings object is created and has expected attributes."""
    # These are safe, generic checks that should always hold
    assert isinstance(settings.app_name, str)
    assert isinstance(settings.app_version, str)
    assert isinstance(settings.debug_mode, bool)
    # Database name should look like a sqlite file name
    assert settings.database_name.endswith(".db")


def test_get_stats_empty_db(tmp_path):
    """
    When there are no todos in a fresh DB, stats should all be zero.

    This hits the get_stats logic for an empty table.
    """
    db_path = tmp_path / "stats_empty.db"
    db = TodoDatabase(str(db_path))

    stats = db.get_stats()

    assert stats["total"] == 0
    assert stats["completed"] == 0
    assert stats["pending"] == 0


def test_get_stats_with_data(tmp_path):
    """
    Create a couple of todos and mark one as completed to exercise
    the stats aggregation with non-empty data.
    """
    db_path = tmp_path / "stats_data.db"
    db = TodoDatabase(str(db_path))

    # Create two todos
    db.create_todo(TodoCreate(title="Todo A", description=None, due_date=None))
    db.create_todo(TodoCreate(title="Todo B", description=None, due_date=None))

    # Mark the first one as completed
    db.update_todo(1, TodoUpdate(completed=True))

    stats = db.get_stats()

    assert stats["total"] == 2
    assert stats["completed"] == 1
    assert stats["pending"] == 1


def test_database_error_on_connection_failure(monkeypatch, tmp_path):
    """
    Force sqlite3.connect to fail so we exercise the DatabaseError path.

    This makes sure the error-handling branches in the DB layer are covered.
    """

    def broken_connect(*args, **kwargs):
        raise sqlite3.Error("boom")

    # Replace sqlite3.connect just inside this test
    monkeypatch.setattr(sqlite3, "connect", broken_connect)

    db = TodoDatabase(str(tmp_path / "broken.db"))

    # Any DB operation that tries to open a connection should now raise DatabaseError
    with pytest.raises(DatabaseError):
        db.get_all_todos()


def test_health_check_unhealthy_branch(monkeypatch):
    """
    Force /health to go through the 'unhealthy' path (HTTP 503).

    We do this by making db.get_stats raise DatabaseError.
    """
    from main import db as main_db

    def broken_stats():
        raise DatabaseError("stats failed")

    monkeypatch.setattr(main_db, "get_stats", broken_stats)

    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code == 503
    body = response.json()
    assert body["status"] == "unhealthy"
    assert body["app_name"] == settings.app_name
