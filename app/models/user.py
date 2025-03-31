from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4

""" Se supone que SQLModel ya trae BaseModel y además esto hace que mi modelo sea una entidad """
class User(SQLModel, table = True): #Table True hace que sea una tabla en mi base de datos
    id: UUID = Field(primary_key = True, default_factory = uuid4) # Clave primaria
    name: str
    email: str = Field(index = True, unique = True) # Indexado y único
    age: int | None = None  # Campo opcional
    password: str