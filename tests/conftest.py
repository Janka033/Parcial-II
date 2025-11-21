# Configuración de pytest
import pytest
from sqlmodel import SQLModel, create_engine, Session
from sqlmodel.pool import StaticPool
from fastapi.testclient import TestClient
from src.main import app
from src.database import get_session


# Fixture para crear una sesión de BD en memoria (para tests)
@pytest.fixture(name="session")
def session_fixture():
    # Crear una BD SQLite en memoria para las pruebas
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


# Fixture para crear un cliente de pruebas
@pytest.fixture(name="client")
def client_fixture(session: Session):
    # Reemplazar la sesión real por la de pruebas
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
