from pydantic import BaseModel
from uuid import UUID

#Esto es para validar la entrada, el id se genera automático.
class UserCreate(BaseModel):
    name: str 
    email: str 
    age: int 
    password: str

#Esto es para validar la salida, sin contar la contraseña.
class UserResponse(BaseModel):
    id: UUID
    name: str 
    email: str 
    age: int
    password: str
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