# Controladores (Routers) - Endpoints de la API
from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from typing import List
from .database import get_session
from .models import UserCreate, UserRead, TaskCreate, TaskRead, TaskUpdate
from . import services

# Router para usuarios
user_router = APIRouter(prefix="/users", tags=["Users"])

# Router para tareas
task_router = APIRouter(prefix="/tasks", tags=["Tasks"])


# ============ ENDPOINTS DE USUARIOS ============

# Crear un usuario
@user_router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    return services.create_user(user, session)


# Listar todos los usuarios
@user_router.get("/", response_model=List[UserRead])
def list_users(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    return services.list_users(session, skip, limit)


# Obtener un usuario por ID
@user_router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, session: Session = Depends(get_session)):
    return services.get_user(user_id, session)


# Obtener las tareas de un usuario
@user_router.get("/{user_id}/tasks", response_model=List[TaskRead])
def get_user_tasks(user_id: int, session: Session = Depends(get_session)):
    return services.list_user_tasks(user_id, session)


# ============ ENDPOINTS DE TAREAS ============

# Crear una tarea
@task_router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate, session: Session = Depends(get_session)):
    return services.create_task(task, session)


# Obtener una tarea por ID
@task_router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: int, session: Session = Depends(get_session)):
    return services.get_task(task_id, session)


# Actualizar una tarea
@task_router.put("/{task_id}", response_model=TaskRead)
def update_task(task_id: int, task: TaskUpdate, session: Session = Depends(get_session)):
    return services.update_task(task_id, task, session)


# Eliminar una tarea
@task_router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, session: Session = Depends(get_session)):
    services.delete_task(task_id, session)
    return None
