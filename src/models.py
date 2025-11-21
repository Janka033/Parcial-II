# Modelos de la base de datos
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime


# Modelo de Usuario
class User(SQLModel, table=True):
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(min_length=2, max_length=100)
    email: str = Field(unique=True, index=True, max_length=100)
    
    # Relación con tasks (un usuario puede tener muchas tareas)
    tasks: List["Task"] = Relationship(back_populates="user")


# Modelo de Tarea
class Task(SQLModel, table=True):
    __tablename__ = "tasks"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    is_completed: bool = Field(default=False)
    user_id: int = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.now)
    
    # Relación con user (cada tarea pertenece a un usuario)
    user: Optional[User] = Relationship(back_populates="tasks")


# Schemas para crear y leer datos

# Para crear un usuario nuevo
class UserCreate(SQLModel):
    name: str = Field(min_length=2, max_length=100)
    email: str = Field(max_length=100)


# Para mostrar un usuario (con sus datos)
class UserRead(SQLModel):
    id: int
    name: str
    email: str


# Para crear una tarea nueva
class TaskCreate(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = None
    user_id: int


# Para actualizar una tarea
class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None


# Para mostrar una tarea completa
class TaskRead(SQLModel):
    id: int
    title: str
    description: Optional[str]
    is_completed: bool
    user_id: int
    created_at: datetime


# Para mostrar un usuario con sus tareas
class UserWithTasks(UserRead):
    tasks: List[TaskRead] = []
