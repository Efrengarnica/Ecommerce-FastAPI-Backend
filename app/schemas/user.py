from pydantic import BaseModel
from uuid import UUID
from models.user import Role

#Esto es para validar la entrada, el id se genera automático.
class UserCreate(BaseModel):
    name: str 
    email: str 
    age: int | None = None  # Campo opcional
    password: str

#Esto es para validar la salida, sin contar la contraseña.
class UserResponse(BaseModel):
    id: UUID
    name: str 
    email: str 
    age: int | None 
    role: Role
    model_config = {
        "from_attributes": True,  
    }

#Para poder realizar el patch  
class UserPatch(BaseModel):
    name: str | None = None
    email: str | None = None
    age: int | None = None
    password: str | None = None
    
#Para poder realizar el put
class UserPut(BaseModel):
    id: UUID
    name: str 
    email: str 
    age: int | None
    password: str

#Para poder buscar el user por medio de su correo y contraseña
class UserLogin(BaseModel):
    email: str
    password: str
    
#Para poder cambiar la contraseña
class UserPassword(BaseModel):
    passwordActual: str 
    passwordNuevo:str 