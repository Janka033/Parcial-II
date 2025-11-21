# Prueba End-to-End (E2E) - Flujo completo
from fastapi.testclient import TestClient


def test_complete_workflow_e2e(client: TestClient):
    
    #1: Crear un usuario
    user_data = {
        "name": "Usuario de Prueba E2E",
        "email": "e2e@test.com"
    }
    user_response = client.post("/users/", json=user_data)
    assert user_response.status_code == 201
    user = user_response.json()
    user_id = user["id"]
    print(f"✓ Usuario creado con ID: {user_id}")
    
    #2: Crear varias tareas para el usuario
    tasks_to_create = [
        {"title": "Estudiar FastAPI", "description": "Repasar conceptos", "user_id": user_id},
        {"title": "Hacer ejercicio", "description": "30 minutos", "user_id": user_id},
        {"title": "Leer libro", "description": "Capítulo 5", "user_id": user_id}
    ]
    
    created_tasks = []
    for task_data in tasks_to_create:
        task_response = client.post("/tasks/", json=task_data)
        assert task_response.status_code == 201
        task = task_response.json()
        created_tasks.append(task)
        assert task["is_completed"] is False
    
    print(f"✓ {len(created_tasks)} tareas creadas")
    
    #3: Listar todas las tareas del usuario
    tasks_response = client.get(f"/users/{user_id}/tasks")
    assert tasks_response.status_code == 200
    user_tasks = tasks_response.json()
    assert len(user_tasks) == 3
    print(f"✓ Tareas del usuario listadas: {len(user_tasks)}")
    
    #4: Actualizar el estado de una tarea (marcarla como completada)
    first_task_id = created_tasks[0]["id"]
    update_data = {
        "is_completed": True,
        "title": "Estudiar FastAPI - COMPLETADO"
    }
    update_response = client.put(f"/tasks/{first_task_id}", json=update_data)
    assert update_response.status_code == 200
    updated_task = update_response.json()
    assert updated_task["is_completed"] is True
    assert "COMPLETADO" in updated_task["title"]
    print(f"✓ Tarea {first_task_id} actualizada y marcada como completada")
    
    # Verificar que la actualización se guardó
    verify_response = client.get(f"/tasks/{first_task_id}")
    assert verify_response.status_code == 200
    assert verify_response.json()["is_completed"] is True
    
    #5: Eliminar una tarea
    second_task_id = created_tasks[1]["id"]
    delete_response = client.delete(f"/tasks/{second_task_id}")
    assert delete_response.status_code == 204
    print(f"✓ Tarea {second_task_id} eliminada")
    
    # Verificar que la tarea fue eliminada
    get_deleted_response = client.get(f"/tasks/{second_task_id}")
    assert get_deleted_response.status_code == 404
    
    #6: Verificar el estado final
    final_tasks_response = client.get(f"/users/{user_id}/tasks")
    assert final_tasks_response.status_code == 200
    final_tasks = final_tasks_response.json()
    
    # Deben quedar 2 tareas (se eliminó 1)
    assert len(final_tasks) == 2
    
    # Una debe estar completada
    completed_tasks = [t for t in final_tasks if t["is_completed"]]
    assert len(completed_tasks) == 1
    
    # Una debe estar pendiente
    pending_tasks = [t for t in final_tasks if not t["is_completed"]]
    assert len(pending_tasks) == 1
    
    print("✓ Estado final verificado correctamente")
    print(f"  - Tareas totales: {len(final_tasks)}")
    print(f"  - Completadas: {len(completed_tasks)}")
    print(f"  - Pendientes: {len(pending_tasks)}")
    
    print("\n✅ FLUJO E2E COMPLETADO EXITOSAMENTE")


def test_multiple_users_e2e(client: TestClient):
    """
    Prueba E2E con múltiples usuarios para verificar que las tareas
    están correctamente asociadas a cada usuario
    """
    
    # Crear dos usuarios diferentes
    user1 = client.post("/users/", json={"name": "Usuario 1", "email": "user1@e2e.com"}).json()
    user2 = client.post("/users/", json={"name": "Usuario 2", "email": "user2@e2e.com"}).json()
    
    # Crear tareas para cada usuario
    client.post("/tasks/", json={"title": "Tarea User1-1", "user_id": user1["id"]})
    client.post("/tasks/", json={"title": "Tarea User1-2", "user_id": user1["id"]})
    client.post("/tasks/", json={"title": "Tarea User2-1", "user_id": user2["id"]})
    
    # Verificar que cada usuario solo ve sus propias tareas
    user1_tasks = client.get(f"/users/{user1['id']}/tasks").json()
    user2_tasks = client.get(f"/users/{user2['id']}/tasks").json()
    
    assert len(user1_tasks) == 2
    assert len(user2_tasks) == 1
    
    # Verificar que las tareas tienen el user_id correcto
    for task in user1_tasks:
        assert task["user_id"] == user1["id"]
    
    for task in user2_tasks:
        assert task["user_id"] == user2["id"]
    
    print("✅ PRUEBA E2E MULTI-USUARIO EXITOSA")
