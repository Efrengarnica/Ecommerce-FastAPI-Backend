""" Se supone que esto es para que mis modelos que cree se conviertan en entidades, esto tambien hace que esos modelos se guarden en 
    en un archivo que simula una base de datos.
"""
from typing import Generator
from sqlmodel import create_engine, Session, SQLModel
from contextlib import contextmanager
from app.models.user import User
from app.models.product import Product
from app.models.cart import Cart, CartItem

DATABASE_URL = "sqlite:///database.db"
engine = create_engine(DATABASE_URL, echo=True)  # `echo=True` muestra las consultas SQL en consola

# Crear la tabla en la base de datos
def create_db():
    SQLModel.metadata.create_all(engine)

create_db()


# Dependencia para la sesión de base de datos

# Dependencia para obtener la sesión de la base de datos
def get_session() -> Generator[Session, None, None]:
    session = Session(engine)
    try:
        yield session  # Esto permite que FastAPI maneje la sesión de forma adecuada
    finally:
        session.close()  # Se cierra la sesión una vez terminada
        