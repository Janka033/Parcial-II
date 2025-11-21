# Aplicación principal FastAPI
from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database import create_db_and_tables
from .controllers import user_router, task_router


# Función para inicializar la app (crear tablas)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Al iniciar: crear las tablas en la BD
    create_db_and_tables()
    yield
    # Al cerrar: limpiar recursos si es necesario


# Crear la aplicación FastAPI
app = FastAPI(
    title="To-Do API",
    description="API REST para gestionar usuarios y tareas",
    version="1.0.0",
    lifespan=lifespan
)

# Incluir los routers
app.include_router(user_router)
app.include_router(task_router)


# Endpoint raíz
@app.get("/", tags=["Root"])
def root():
    return {
        "message": "To-Do API",
        "version": "1.0.0",
        "docs": "/docs"
    }


# Health check
@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}
