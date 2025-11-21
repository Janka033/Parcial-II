# Servicios - Lógica de negocio
from sqlmodel import Session, select
from fastapi import HTTPException, status
from .models import User, Task, UserCreate, TaskCreate, TaskUpdate
from typing import List


# ============ SERVICIOS DE USUARIOS ============

# Crear un usuario nuevo
def create_user(user_data: UserCreate, session: Session) -> User:
    # Verificar si el email ya existe
    existing_user = session.exec(select(User).where(User.email == user_data.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    
    # Crear el usuario
    user = User.model_validate(user_data)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


# Obtener un usuario por ID
def get_user(user_id: int, session: Session) -> User:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return user


# Listar todos los usuarios
def list_users(session: Session, skip: int = 0, limit: int = 100) -> List[User]:
    users = session.exec(select(User).offset(skip).limit(limit)).all()
    return users


# ============ SERVICIOS DE TAREAS ============

# Crear una tarea para un usuario
def create_task(task_data: TaskCreate, session: Session) -> Task:
    # Verificar que el usuario existe
    user = session.get(User, task_data.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # Crear la tarea
    task = Task.model_validate(task_data)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


# Listar tareas de un usuario específico
def list_user_tasks(user_id: int, session: Session) -> List[Task]:
    # Verificar que el usuario existe
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    # Obtener todas las tareas del usuario
    tasks = session.exec(select(Task).where(Task.user_id == user_id)).all()
    return tasks


# Obtener una tarea por ID
def get_task(task_id: int, session: Session) -> Task:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarea no encontrada"
        )
    return task


# Actualizar una tarea (título, descripción o estado)
def update_task(task_id: int, task_data: TaskUpdate, session: Session) -> Task:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarea no encontrada"
        )
    
    # Actualizar solo los campos que vienen en la petición
    task_update_dict = task_data.model_dump(exclude_unset=True)
    for key, value in task_update_dict.items():
        setattr(task, key, value)
    
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


# Eliminar una tarea
def delete_task(task_id: int, session: Session) -> None:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarea no encontrada"
        )
    
    session.delete(task)
    session.commit()
