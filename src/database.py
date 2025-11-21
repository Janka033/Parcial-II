# Configuración de la base de datos
from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv
import os

# Cargar variables del archivo .env
load_dotenv()

# Obtener la URL de conexión a la BD
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:@localhost:3306/parcial_db")

# Crear el motor de la base de datos
engine = create_engine(DATABASE_URL, echo=True)


# Función para crear las tablas en la BD
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# Función para obtener una sesión de BD
def get_session():
    with Session(engine) as session:
        yield session
