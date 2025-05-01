# tests/conftest.py

import os
import asyncio
import pytest
import pytest_asyncio

from contextlib import asynccontextmanager

#Cuando se trabajo con asyn con pytests se intala pip install pytest-asyncio
# ----------------------------------------------------------
# testcontainers: para levantar y destruir un contenedor
#   de Postgres “de juguete” en cada sesión de pytest
#Se intala con pip install testcontainers[postgresql]
# ----------------------------------------------------------
from testcontainers.postgres import PostgresContainer
# ----------------------------------------------------------
# SQLModel/SQLAlchemy Async: crear engine y sesiones
# ----------------------------------------------------------
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# ----------------------------------------------------------
# Tu metadata (Base) donde están todos los modelos/tabledefs
# ----------------------------------------------------------
from database import Base

# ----------------------------------------------------------
# Para modificar (monkey-patch) la función get_session()
# dentro de tu módulo de repositorio
#se importa el modulo completo para cambiar la funcion get_session.
# ----------------------------------------------------------
import repository.user as user_repo_module

# La idea aquí es que estos fixture me ayuden a que cada test que se haga pueda experimentar como si estuviera conviviendo con una bd real.
# Se creo lo siguiente:
# 1. Contenedor de Postgres
# 2. Conexion async_engine
# 3. Sesion async_session
# 4. override_get_session que me ayuda a que si ocupo un método del repository de user este no ocupe las conexiones a la bd real.

# -----------------------------------------------------------------------------
# 2) postgres_container
# -----------------------------------------------------------------------------
# Levanta un contenedor de Postgres una sola vez por sesión de pytest
@pytest.fixture(scope="session")
def postgres_container():
    # Con `with` usamos el contexto de testcontainers
    with PostgresContainer("postgres:15-alpine", driver="asyncpg") as pg:
        pg.start()
        # Internamente hace docker run + wait-for-ready
        yield pg
    # Al salir del with, detiene y elimina el contenedor
    
# -----------------------------------------------------------------------------
# 3) async_engine
# -----------------------------------------------------------------------------
# Crea un SQLAlchemy AsyncEngine apuntando al Postgres del contenedor
@pytest_asyncio.fixture(scope="session")
async def async_engine(postgres_container):
    # Obtenemos la URL de conexión y la adaptamos para asyncpg
    url = postgres_container.get_connection_url()
    engine = create_async_engine(url, echo=False, future=True)

    # Creamos las tablas una sola vez al inicio
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # Cerramos el engine al final de la sesión
    await engine.dispose()

# -----------------------------------------------------------------------------
# 4) async_session
# -----------------------------------------------------------------------------
# Proporciona una AsyncSession limpia para cada test y hace rollback
@pytest_asyncio.fixture
async def async_session(async_engine):
    # Configura el sessionmaker para AsyncSession
    AsyncSessionLocal = sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    # Abrimos una sesión
    async with AsyncSessionLocal() as session:
        yield session
        # Rollback de todo lo hecho en el test para aislar estado
        await session.rollback()

# -----------------------------------------------------------------------------
# 5) override_get_session
# -----------------------------------------------------------------------------
# Monkey-patch automático de get_session() para que
# Reemplaza la función get_session() del módulo de repositorio para que no se modifique nuetsra bd real.
# apunte a nuestra async_session de pruebas
@pytest.fixture(autouse=True)
def override_get_session(async_session, monkeypatch):
    # Creamos un async context manager que yield-ea la sesión de pruebas
    @asynccontextmanager
    async def _get_session_override():
        yield async_session

    # Parcheamos get_session() para que use este async context manager
    monkeypatch.setattr(
        user_repo_module,
        "get_session",
        _get_session_override
    )