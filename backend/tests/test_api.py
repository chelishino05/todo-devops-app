"""
Integration tests for FastAPI endpoints
Tests API routes and responses including error cases
"""

import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture(scope="function", autouse=True)
def setup_test_db():
    """Setup test database before each test"""
    from database import TodoDatabase
    import main
    
    db_name = "test_api.db"
    main.db = TodoDatabase(db_name)
    
    yield
    
    # Cleanup
    if os.path.exists(db_name):
        os.remove(db_name)


def test_root_endpoint():
    """Test root endpoint returns HTML"""
    from main import app
    from fastapi.testclient import TestClient
    
    client = TestClient(app)
    response = client.get("/")
    
    assert response.status_code == 200


def test_health_check():
    """Test health check endpoint"""
    from main import app
    from fastapi.testclient import TestClient
    
    client = TestClient(app)
    response = client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'healthy'
    assert 'database' in data
    assert 'stats' in data


def test_metrics_endpoint():
    """Test Prometheus metrics endpoint"""
    from main import app
    from fastapi.testclient import TestClient
    
    client = TestClient(app)
    response = client.get("/metrics")
    
    assert response.status_code == 200


def test_create_todo():
    """Test creating a todo via API"""
    from main import app
    from fastapi.testclient import TestClient
    
    client = TestClient(app)
    todo_data = {
        "title": "Test Todo",
        "description": "Test Description",
        "due_date": "2025-12-31"
    }
    
    response = client.post("/api/todos", json=todo_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data['title'] == "Test Todo"
    assert data['description'] == "Test Description"


def test_create_todo_minimal():
    """Test creating todo with only required fields"""
    from main import app
    from fastapi.testclient import TestClient
    
    client = TestClient(app)
    todo_data = {"title": "Minimal Todo"}
    
    response = client.post("/api/todos", json=todo_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data['title'] == "Minimal Todo"


def test_get_all_todos():
    """Test getting all todos"""
    from main import app
    from fastapi.testclient import TestClient
    
    client = TestClient(app)
    
    # Create some todos first
    client.post("/api/todos", json={"title": "Todo 1"})
    client.post("/api/todos", json={"title": "Todo 2"})
    
    response = client.get("/api/todos")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2


def test_get_all_todos_empty():
    """Test getting todos when none exist"""
    from main import app
    from fastapi.testclient import TestClient
    
    client = TestClient(app)
    response = client.get("/api/todos")
    
    assert response.status_code == 200
    assert response.json() == []


def test_get_todo_by_id():
    """Test getting a specific todo"""
    from main import app
    from fastapi.testclient import TestClient
    
    client = TestClient(app)
    
    # Create a todo first
    create_response = client.post("/api/todos", json={"title": "Find Me"})
    todo_id = create_response.json()['id']
    
    # Get it by ID
    response = client.get(f"/api/todos/{todo_id}")
    
    assert response.status_code == 200
    assert response.json()['title'] == "Find Me"


def test_get_todo_by_id_not_found():
    """Test getting non-existent todo returns 404"""
    from main import app
    from fastapi.testclient import TestClient
    
    client = TestClient(app)
    response = client.get("/api/todos/99999")
    
    assert response.status_code == 404
    assert "not found" in response.json()['detail'].lower()


def test_update_todo():
    """Test updating a todo"""
    from main import app
    from fastapi.testclient import TestClient
    
    client = TestClient(app)
    
    # Create a todo
    create_response = client.post("/api/todos", json={"title": "Original"})
    todo_id = create_response.json()['id']
    
    # Update it
    response = client.put(
        f"/api/todos/{todo_id}", 
        json={"title": "Updated", "completed": True}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data['title'] == "Updated"
    assert data['completed'] == True


def test_update_todo_partial():
    """Test partial update of todo"""
    from main import app
    from fastapi.testclient import TestClient
    
    client = TestClient(app)
    
    # Create a todo
    create_response = client.post("/api/todos", json={"title": "Original", "description": "Desc"})
    todo_id = create_response.json()['id']
    
    # Update only title
    response = client.put(f"/api/todos/{todo_id}", json={"title": "New Title"})
    
    assert response.status_code == 200
    data = response.json()
    assert data['title'] == "New Title"


def test_update_todo_not_found():
    """Test updating non-existent todo returns 404"""
    from main import app
    from fastapi.testclient import TestClient
    
    client = TestClient(app)
    response = client.put("/api/todos/99999", json={"title": "Updated"})
    
    assert response.status_code == 404
    assert "not found" in response.json()['detail'].lower()


def test_delete_todo():
    """Test deleting a todo"""
    from main import app
    from fastapi.testclient import TestClient
    
    client = TestClient(app)
    
    # Create a todo
    create_response = client.post("/api/todos", json={"title": "Delete Me"})
    todo_id = create_response.json()['id']
    
    # Delete it
    response = client.delete(f"/api/todos/{todo_id}")
    
    assert response.status_code == 200
    assert "deleted" in response.json()['message'].lower()
    
    # Verify it's gone
    get_response = client.get(f"/api/todos/{todo_id}")
    assert get_response.status_code == 404


def test_delete_todo_not_found():
    """Test deleting non-existent todo returns 404"""
    from main import app
    from fastapi.testclient import TestClient
    
    client = TestClient(app)
    response = client.delete("/api/todos/99999")
    
    assert response.status_code == 404
    assert "not found" in response.json()['detail'].lower()


def test_update_todo_complete_workflow():
    """Test complete todo lifecycle"""
    from main import app
    from fastapi.testclient import TestClient
    
    client = TestClient(app)
    
    # Create
    create_response = client.post("/api/todos", json={"title": "Lifecycle Test"})
    assert create_response.status_code == 201
    todo_id = create_response.json()['id']
    
    # Read
    get_response = client.get(f"/api/todos/{todo_id}")
    assert get_response.status_code == 200
    
    # Update
    update_response = client.put(f"/api/todos/{todo_id}", json={"completed": True})
    assert update_response.status_code == 200
    assert update_response.json()['completed'] == True
    
    # Delete
    delete_response = client.delete(f"/api/todos/{todo_id}")
    assert delete_response.status_code == 200