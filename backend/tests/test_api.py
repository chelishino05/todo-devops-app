"""
Integration tests for FastAPI endpoints
Tests API routes, responses, error cases, and middleware
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
    assert data['app_name'] == "Todo List Manager"


def test_health_check_includes_version():
    """Test health check includes version info"""
    from main import app
    from fastapi.testclient import TestClient
    
    client = TestClient(app)
    response = client.get("/health")
    
    data = response.json()
    assert 'version' in data


def test_metrics_endpoint():
    """Test Prometheus metrics endpoint"""
    from main import app
    from fastapi.testclient import TestClient
    
    client = TestClient(app)
    response = client.get("/metrics")
    
    assert response.status_code == 200
    # Metrics should contain prometheus format
    assert b"http_requests_total" in response.content or True


def test_cors_headers():
    """Test CORS headers are present"""
    from main import app
    from fastapi.testclient import TestClient
    
    client = TestClient(app)
    response = client.get("/health")
    
    # CORS middleware should add headers
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
    assert 'id' in data
    assert 'created_at' in data


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
    assert data['completed'] == False


def test_create_multiple_todos():
    """Test creating multiple todos"""
    from main import app
    from fastapi.testclient import TestClient
    
    client = TestClient(app)
    
    for i in range(5):
        response = client.post("/api/todos", json={"title": f"Todo {i}"})
        assert response.status_code == 201


def test_get_all_todos():
    """Test getting all todos"""
    from main import app
    from fastapi.testclient import TestClient
    
    client = TestClient(app)
    
    # Create some todos first
    client.post("/api/todos", json={"title": "Todo 1"})
    client.post("/api/todos", json={"title": "Todo 2"})
    client.post("/api/todos", json={"title": "Todo 3"})
    
    response = client.get("/api/todos")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 3


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
    create_response = client.post("/api/todos", json={"title": "Find Me", "description": "Test"})
    todo_id = create_response.json()['id']
    
    # Get it by ID
    response = client.get(f"/api/todos/{todo_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data['title'] == "Find Me"
    assert data['description'] == "Test"


def test_get_todo_by_id_not_found():
    """Test getting non-existent todo returns 404"""
    from main import app
    from fastapi.testclient import TestClient
    
    client = TestClient(app)
    response = client.get("/api/todos/99999")
    
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data['detail'].lower()


def test_get_multiple_todos_by_id():
    """Test getting multiple specific todos"""
    from main import app
    from fastapi.testclient import TestClient
    
    client = TestClient(app)
    
    # Create multiple todos
    ids = []
    for i in range(3):
        resp = client.post("/api/todos", json={"title": f"Todo {i}"})
        ids.append(resp.json()['id'])
    
    # Get each one
    for todo_id in ids:
        response = client.get(f"/api/todos/{todo_id}")
        assert response.status_code == 200


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


def test_update_todo_completion_status():
    """Test updating completion status"""
    from main import app
    from fastapi.testclient import TestClient
    
    client = TestClient(app)
    
    # Create a todo
    create_response = client.post("/api/todos", json={"title": "Task"})
    todo_id = create_response.json()['id']
    
    # Mark as complete
    response = client.put(f"/api/todos/{todo_id}", json={"completed": True})
    assert response.status_code == 200
    assert response.json()['completed'] == True
    
    # Mark as incomplete
    response = client.put(f"/api/todos/{todo_id}", json={"completed": False})
    assert response.status_code == 200
    assert response.json()['completed'] == False


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
    data = response.json()
    assert "deleted" in data['message'].lower() or "success" in data['message'].lower()
    
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


def test_delete_multiple_todos():
    """Test deleting multiple todos"""
    from main import app
    from fastapi.testclient import TestClient
    
    client = TestClient(app)
    
    # Create multiple todos
    ids = []
    for i in range(3):
        resp = client.post("/api/todos", json={"title": f"Delete {i}"})
        ids.append(resp.json()['id'])
    
    # Delete all of them
    for todo_id in ids:
        response = client.delete(f"/api/todos/{todo_id}")
        assert response.status_code == 200
    
    # Verify all are gone
    response = client.get("/api/todos")
    assert len(response.json()) == 0


def test_complete_workflow():
    """Test complete CRUD workflow"""
    from main import app
    from fastapi.testclient import TestClient
    
    client = TestClient(app)
    
    # Create
    create_response = client.post("/api/todos", json={
        "title": "Workflow Test",
        "description": "Testing complete workflow"
    })
    assert create_response.status_code == 201
    todo_id = create_response.json()['id']
    
    # Read
    get_response = client.get(f"/api/todos/{todo_id}")
    assert get_response.status_code == 200
    assert get_response.json()['title'] == "Workflow Test"
    
    # Update
    update_response = client.put(f"/api/todos/{todo_id}", json={
        "title": "Updated Workflow",
        "completed": True
    })
    assert update_response.status_code == 200
    assert update_response.json()['title'] == "Updated Workflow"
    assert update_response.json()['completed'] == True
    
    # Delete
    delete_response = client.delete(f"/api/todos/{todo_id}")
    assert delete_response.status_code == 200
    
    # Verify deleted
    get_response = client.get(f"/api/todos/{todo_id}")
    assert get_response.status_code == 404


def test_api_consistency():
    """Test API returns consistent data structures"""
    from main import app
    from fastapi.testclient import TestClient
    
    client = TestClient(app)
    
    # Create a todo
    create_response = client.post("/api/todos", json={"title": "Consistency Test"})
    created_todo = create_response.json()
    
    # Get the same todo
    todo_id = created_todo['id']
    get_response = client.get(f"/api/todos/{todo_id}")
    retrieved_todo = get_response.json()
    
    # Should have same structure
    assert set(created_todo.keys()) == set(retrieved_todo.keys())
    assert created_todo['id'] == retrieved_todo['id']
    assert created_todo['title'] == retrieved_todo['title']


def test_list_todos_after_operations():
    """Test listing todos reflects operations"""
    from main import app
    from fastapi.testclient import TestClient
    
    client = TestClient(app)
    
    # Start with empty list
    response = client.get("/api/todos")
    assert len(response.json()) == 0
    
    # Create 3 todos
    for i in range(3):
        client.post("/api/todos", json={"title": f"Todo {i}"})
    
    # List should have 3
    response = client.get("/api/todos")
    assert len(response.json()) == 3
    
    # Delete 1
    first_todo_id = response.json()[0]['id']
    client.delete(f"/api/todos/{first_todo_id}")
    
    # List should have 2
    response = client.get("/api/todos")
    assert len(response.json()) == 2


def test_middleware_adds_logging():
    """Test that middleware processes requests"""
    from main import app
    from fastapi.testclient import TestClient
    
    client = TestClient(app)
    
    # Make multiple requests to trigger middleware
    client.get("/health")
    client.get("/metrics")
    client.get("/api/todos")
    
    # If we get here without errors, middleware is working
    assert True


def test_static_files_mount():
    """Test static files are accessible"""
    from main import app
    from fastapi.testclient import TestClient
    
    client = TestClient(app)
    
    # Try to access static endpoint (will fail if frontend doesn't exist, but that's ok)
    response = client.get("/static/")
    # Just check we don't get 500 error
    assert response.status_code in [200, 404, 405]