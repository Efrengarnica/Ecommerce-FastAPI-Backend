""" Se supone que esto es para que mis modelos que cree se conviertan en entidades, esto tambien hace que esos modelos se guarden en 
    en un archivo que simula una base de datos.
    Aparte de definir mis modelos como table = True debo de importarlo aqui para que cuando levante el servidor estos se conviertan 
    automaticamente en tables de mi base de datos, si no hago los imports no se crean las tablas.
"""
""" from typing import Generator
from contextlib import contextmanager
from sqlmodel import create_engine, Session, SQLModel """

from typing import AsyncGenerator
from sqlmodel import SQLModel
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


from models.user import User
from models.product import Product
from models.cart import Cart, CartItem

Base = SQLModel #Esta parte me ayuda a que mi metadata tenga un nombre y pueda ser usada en el test de pytest
# Base.metadata.create_all(engine) #Esto crea las tablas en una base de datos, esto sera usado en el confest.py para que al momento de levantar el contenedor 
# de juguete se creen las tablas.


from settings.base import DB_PORT, DB_HOST, DB_NAME, DB_USER, DB_PASSWORD

#Base de datos sqlLite que es un doc en donde se guardan mis datos.
#DATABASE_URL = "sqlite:///database.db"
#DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
#engine = create_engine(DATABASE_URL, echo=False)  # `echo=True` muestra las consultas SQL en consola

DATABASE_URL = (
    f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_async_engine(DATABASE_URL, echo=False, future=True)



# Crear la tabla en la base de datos
#def create_db():
   # SQLModel.metadata.create_all(engine)
#Funcion que cuando se levanta el servidor se ejecuta, esto busca todos los modelos que cumplan con table = True y los agrega a la base de datos 
#create_db()

# Dependencia para obtener la sesión de la base de datos
#Por lo que entiendo esto genera una sesion, pero la va a estar manejando FastAPI y cada que termine de ocuparla la cierra en automático
#Esto es difrente a como nos dijo Alexis.
""" @contextmanager
def get_session() -> Generator[Session, None, None]: #Sesion es lo que pausa el yield, elt ipo de dato, 1er None es porque No recibe nada la funcion
    #El tercer None es porque la funcion no retorna nada
    session = Session(engine)
    try:
        yield session  # Esto permite que FastAPI maneje la sesión de forma adecuada, yield pausa una funcionhasta que la empiecen a ocupar
        #En este caso cada vez que en una funciopn ocupamos yield entonces esa fuencion regresa un generador, que es un funncion que produce valores de manera
        #pausada.
    finally:
        session.close()  # Se cierra la sesión una vez terminada """
        
@asynccontextmanager
async def get_session() -> AsyncGenerator[None, None]:
    """
    Creates an async session
    """
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session