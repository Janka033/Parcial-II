# Pruebas Unitarias - Servicios
import pytest
from sqlmodel import Session
from fastapi import HTTPException
from src.models import UserCreate, TaskCreate, TaskUpdate
from src import services


# ============ PRUEBAS DE SERVICIOS DE USUARIOS ============

def test_create_user_success(session: Session):
    # Crear un usuario válido
    user_data = UserCreate(name="Juan", email="juan@test.com")
    user = services.create_user(user_data, session)
    
    assert user.id is not None
    assert user.name == "Juan"
    assert user.email == "juan@test.com"


def test_create_user_duplicate_email(session: Session):
    # Crear primer usuario
    user_data = UserCreate(name="Juan", email="juan@test.com")
    services.create_user(user_data, session)
    
    # Intentar crear otro con el mismo email debe fallar
    with pytest.raises(HTTPException) as exc_info:
        services.create_user(user_data, session)
    
    assert exc_info.value.status_code == 400
    assert "email ya está registrado" in exc_info.value.detail


def test_get_user_success(session: Session):
    # Crear un usuario
    user_data = UserCreate(name="María", email="maria@test.com")
    created_user = services.create_user(user_data, session)
    
    # Obtener el usuario
    user = services.get_user(created_user.id, session)
    assert user.id == created_user.id
    assert user.name == "María"


def test_get_user_not_found(session: Session):
    # Buscar un usuario que no existe
    with pytest.raises(HTTPException) as exc_info:
        services.get_user(999, session)
    
    assert exc_info.value.status_code == 404


def test_list_users(session: Session):
    # Crear varios usuarios
    services.create_user(UserCreate(name="User1", email="user1@test.com"), session)
    services.create_user(UserCreate(name="User2", email="user2@test.com"), session)
    
    # Listar usuarios
    users = services.list_users(session)
    assert len(users) == 2


# ============ PRUEBAS DE SERVICIOS DE TAREAS ============

def test_create_task_success(session: Session):
    # Primero crear un usuario
    user_data = UserCreate(name="Pedro", email="pedro@test.com")
    user = services.create_user(user_data, session)
    
    # Crear una tarea para ese usuario
    task_data = TaskCreate(
        title="Comprar pan",
        description="Ir al supermercado",
        user_id=user.id
    )
    task = services.create_task(task_data, session)
    
    assert task.id is not None
    assert task.title == "Comprar pan"
    assert task.is_completed is False
    assert task.user_id == user.id


def test_create_task_user_not_found(session: Session):
    # Intentar crear tarea con usuario inexistente
    task_data = TaskCreate(title="Tarea", user_id=999)
    
    with pytest.raises(HTTPException) as exc_info:
        services.create_task(task_data, session)
    
    assert exc_info.value.status_code == 404


def test_list_user_tasks(session: Session):
    # Crear usuario
    user = services.create_user(UserCreate(name="Ana", email="ana@test.com"), session)
    
    # Crear varias tareas
    services.create_task(TaskCreate(title="Tarea 1", user_id=user.id), session)
    services.create_task(TaskCreate(title="Tarea 2", user_id=user.id), session)
    
    # Listar tareas del usuario
    tasks = services.list_user_tasks(user.id, session)
    assert len(tasks) == 2


def test_update_task_success(session: Session):
    # Crear usuario y tarea
    user = services.create_user(UserCreate(name="Luis", email="luis@test.com"), session)
    task = services.create_task(
        TaskCreate(title="Tarea original", user_id=user.id),
        session
    )
    
    # Actualizar la tarea
    update_data = TaskUpdate(title="Tarea actualizada", is_completed=True)
    updated_task = services.update_task(task.id, update_data, session)
    
    assert updated_task.title == "Tarea actualizada"
    assert updated_task.is_completed is True


def test_update_task_not_found(session: Session):
    # Intentar actualizar tarea inexistente
    with pytest.raises(HTTPException) as exc_info:
        services.update_task(999, TaskUpdate(title="Test"), session)
    
    assert exc_info.value.status_code == 404


def test_delete_task_success(session: Session):
    # Crear usuario y tarea
    user = services.create_user(UserCreate(name="Carlos", email="carlos@test.com"), session)
    task = services.create_task(TaskCreate(title="Tarea", user_id=user.id), session)
    
    # Eliminar tarea
    services.delete_task(task.id, session)
    
    # Verificar que ya no existe
    with pytest.raises(HTTPException):
        services.get_task(task.id, session)


def test_delete_task_not_found(session: Session):
    # Intentar eliminar tarea inexistente
    with pytest.raises(HTTPException) as exc_info:
        services.delete_task(999, session)
    
    assert exc_info.value.status_code == 404
