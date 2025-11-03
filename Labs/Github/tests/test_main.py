import pytest
from fastapi.testclient import TestClient
from main import app, tasks, task_id_counter

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_data():
    """Reset the in-memory storage before each test"""
    tasks.clear()
    # Reset the counter
    import main
    main.task_id_counter = 1
    yield


def test_read_root():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Task API"}


def test_create_task():
    """Test creating a new task"""
    task_data = {
        "title": "Buy groceries",
        "description": "Get milk and bread",
        "completed": False
    }
    response = client.post("/tasks", json=task_data)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Buy groceries"
    assert data["description"] == "Get milk and bread"
    assert data["completed"] is False


def test_create_multiple_tasks():
    """Test creating multiple tasks with incrementing IDs"""
    task1 = {"title": "Task 1", "description": "First task"}
    task2 = {"title": "Task 2", "description": "Second task"}
    
    response1 = client.post("/tasks", json=task1)
    response2 = client.post("/tasks", json=task2)
    
    assert response1.json()["id"] == 1
    assert response2.json()["id"] == 2


def test_get_tasks_empty():
    """Test getting tasks when none exist"""
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_get_tasks_with_data():
    """Test getting all tasks"""
    # Create some tasks first
    client.post("/tasks", json={"title": "Task 1", "description": "First"})
    client.post("/tasks", json={"title": "Task 2", "description": "Second"})
    
    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Task 1"
    assert data[1]["title"] == "Task 2"


def test_get_task_by_id():
    """Test getting a specific task by ID"""
    # Create a task
    create_response = client.post("/tasks", json={
        "title": "Test Task",
        "description": "Testing"
    })
    task_id = create_response.json()["id"]
    
    # Get the task
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Test Task"


def test_get_task_not_found():
    """Test getting a task that doesn't exist"""
    response = client.get("/tasks/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_update_task():
    """Test updating an existing task"""
    # Create a task
    create_response = client.post("/tasks", json={
        "title": "Original Title",
        "description": "Original Description"
    })
    task_id = create_response.json()["id"]
    
    # Update the task
    updated_data = {
        "title": "Updated Title",
        "description": "Updated Description",
        "completed": True
    }
    response = client.put(f"/tasks/{task_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["completed"] is True


def test_update_task_not_found():
    """Test updating a task that doesn't exist"""
    response = client.put("/tasks/999", json={
        "title": "Test",
        "description": "Test"
    })
    assert response.status_code == 404


def test_delete_task():
    """Test deleting a task"""
    # Create a task
    create_response = client.post("/tasks", json={
        "title": "To Delete",
        "description": "This will be deleted"
    })
    task_id = create_response.json()["id"]
    
    # Delete the task
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Task deleted successfully"
    
    # Verify it's deleted
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404


def test_delete_task_not_found():
    """Test deleting a task that doesn't exist"""
    response = client.delete("/tasks/999")
    assert response.status_code == 404


def test_task_completed_default():
    """Test that completed defaults to False"""
    response = client.post("/tasks", json={
        "title": "Test",
        "description": "Test description"
    })
    assert response.json()["completed"] is False


def test_full_workflow():
    """Test a complete workflow: create, read, update, delete"""
    # Create
    create_resp = client.post("/tasks", json={
        "title": "Workflow Test",
        "description": "Testing complete workflow"
    })
    assert create_resp.status_code == 200
    task_id = create_resp.json()["id"]
    
    # Read
    read_resp = client.get(f"/tasks/{task_id}")
    assert read_resp.status_code == 200
    assert read_resp.json()["title"] == "Workflow Test"
    
    # Update
    update_resp = client.put(f"/tasks/{task_id}", json={
        "title": "Updated Workflow",
        "description": "Updated description",
        "completed": True
    })
    assert update_resp.status_code == 200
    assert update_resp.json()["completed"] is True
    
    # Delete
    delete_resp = client.delete(f"/tasks/{task_id}")
    assert delete_resp.status_code == 200
    
    # Verify deletion
    final_resp = client.get(f"/tasks/{task_id}")
    assert final_resp.status_code == 404

# Failing this test on purpose
def test_update_task_not_found_fail():
    """Test updating a task that doesn't exist"""
    response = client.put("/tasks/999", json={
        "title": "Test",
        "description": "Test"
    })
    assert response.status_code == 200