"""
Additional tests to exercise error paths and push coverage over 70%.
These tests are written to match the current implementation in main.py and database.py.
"""

import os
import sys

import pytest
from fastapi.testclient import TestClient

# Make backend modules importable when running tests from backend/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import main  # noqa: E402
from database import DatabaseError  # noqa: E402


def test_database_error_on_connection_failure(monkeypatch):
    """
    Simulate a database error when listing todos and verify that
    the API returns a 500 with the expected error message.
    """

    class BrokenDB:
        def get_all_todos(self):
            raise DatabaseError("boom")

    # Use the broken DB for this test
    main.db = BrokenDB()
    client = TestClient(main.app)

    response = client.get("/api/todos")

    assert response.status_code == 500
    body = response.json()
    # This matches the detail set in main.get_all_todos() on DatabaseError
    assert body["detail"] == "Failed to retrieve todos"


def test_health_check_unhealthy_branch(monkeypatch):
    """
    Force the health check to go through the 'unhealthy' branch by
    making db.get_stats() raise a DatabaseError.
    """

    class BrokenDB:
        def get_stats(self):
            raise DatabaseError("boom")

    main.db = BrokenDB()
    client = TestClient(main.app)

    response = client.get("/health")

    assert response.status_code == 503
    data = response.json()
    assert data["status"] == "unhealthy"
    assert data["database"] == "disconnected"
    assert "boom" in data["error"]
