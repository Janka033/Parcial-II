# Pruebas de Integración - Endpoints
from fastapi.testclient import TestClient


# ============ PRUEBAS DE ENDPOINTS RAÍZ ============

def test_root_endpoint(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "To-Do API"


def test_health_endpoint(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


# ============ PRUEBAS DE INTEGRACIÓN DE USUARIOS ============

def test_create_and_get_user(client: TestClient):
    # Crear un usuario
    user_data = {"name": "Test User", "email": "test@example.com"}
    create_response = client.post("/users/", json=user_data)
    
    assert create_response.status_code == 201
    created_user = create_response.json()
    assert created_user["name"] == "Test User"
    assert "id" in created_user
    
    # Obtener el usuario creado
    user_id = created_user["id"]
    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 200
    assert get_response.json()["email"] == "test@example.com"


def test_list_users(client: TestClient):
    # Crear varios usuarios
    client.post("/users/", json={"name": "User 1", "email": "user1@test.com"})
    client.post("/users/", json={"name": "User 2", "email": "user2@test.com"})
    
    # Listar todos
    response = client.get("/users/")
    assert response.status_code == 200
    users = response.json()
    assert len(users) >= 2


def test_create_user_duplicate_email(client: TestClient):
    # Crear primer usuario
    user_data = {"name": "User", "email": "duplicate@test.com"}
    client.post("/users/", json=user_data)
    
    # Intentar crear con mismo email
    response = client.post("/users/", json=user_data)
    assert response.status_code == 400


# ============ PRUEBAS DE INTEGRACIÓN DE TAREAS ============

def test_create_and_get_task(client: TestClient):
    # Primero crear un usuario
    user_response = client.post("/users/", json={"name": "Owner", "email": "owner@test.com"})
    user_id = user_response.json()["id"]
    
    # Crear una tarea
    task_data = {
        "title": "Mi tarea",
        "description": "Descripción de prueba",
        "user_id": user_id
    }
    create_response = client.post("/tasks/", json=task_data)
    
    assert create_response.status_code == 201
    task = create_response.json()
    assert task["title"] == "Mi tarea"
    assert task["is_completed"] is False
    
    # Obtener la tarea
    task_id = task["id"]
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 200


def test_create_task_invalid_user(client: TestClient):
    # Intentar crear tarea con usuario inexistente
    task_data = {"title": "Tarea", "user_id": 9999}
    response = client.post("/tasks/", json=task_data)
    assert response.status_code == 404


def test_update_task(client: TestClient):
    # Crear usuario y tarea
    user = client.post("/users/", json={"name": "Test", "email": "update@test.com"}).json()
    task = client.post("/tasks/", json={"title": "Original", "user_id": user["id"]}).json()
    
    # Actualizar la tarea
    update_data = {"title": "Actualizada", "is_completed": True}
    response = client.put(f"/tasks/{task['id']}", json=update_data)
    
    assert response.status_code == 200
    updated = response.json()
    assert updated["title"] == "Actualizada"
    assert updated["is_completed"] is True


def test_delete_task(client: TestClient):
    # Crear usuario y tarea
    user = client.post("/users/", json={"name": "Test", "email": "delete@test.com"}).json()
    task = client.post("/tasks/", json={"title": "To Delete", "user_id": user["id"]}).json()
    
    # Eliminar la tarea
    delete_response = client.delete(f"/tasks/{task['id']}")
    assert delete_response.status_code == 204
    
    # Verificar que ya no existe
    get_response = client.get(f"/tasks/{task['id']}")
    assert get_response.status_code == 404


def test_get_user_tasks(client: TestClient):
    # Crear usuario
    user = client.post("/users/", json={"name": "Owner", "email": "tasks@test.com"}).json()
    user_id = user["id"]
    
    # Crear varias tareas para ese usuario
    client.post("/tasks/", json={"title": "Tarea 1", "user_id": user_id})
    client.post("/tasks/", json={"title": "Tarea 2", "user_id": user_id})
    client.post("/tasks/", json={"title": "Tarea 3", "user_id": user_id})
    
    # Obtener todas las tareas del usuario
    response = client.get(f"/users/{user_id}/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 3
