from passlib.context import CryptContext
from sqlite3 import IntegrityError
from uuid import UUID
from models.user import User
from schemas.user import UserCreate, UserLogin, UserPassword, UserPatch
from repository.user import UserRepository
from exceptions.exceptions import (DatabaseIntegrityException, InternalServerErrorException, InvalidCredentialsException)

class UserGateway:
    # Crea un contexto para poder hashear la contraseña, se usa bcrypt.
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
 
    #Método para hashear la contraseña.
    @classmethod
    def hash_password(cls, password: str) -> str:
        """
        Hash the password using bcrypt.
        """
        return cls.pwd_context.hash(password)
    
    @classmethod
    async def create_user(cls, user_create: UserCreate) -> User:
        try:
            hashed_password = cls.hash_password(user_create.password)
            #Por como lo definí, cuando lo creas sin role el role es client.
            # No validamos eso lo hace baseModel cuando se crea el User, si se le da un role que no existe en model User entonces no se crea el user.
            user = User(
                name=user_create.name,
                email=user_create.email,
                age=user_create.age,
                password=hashed_password
            )
            return await UserRepository.create_user(user)
        except IntegrityError as e:
            raise DatabaseIntegrityException(str(e))
      
    #Método que me ayuda a registrar un usuario y un carrito al mismo tiempo.  
    @classmethod
    async def create_user_and_cart(cls, user_create:UserCreate) -> User:
        try:
            hashed_password = cls.hash_password(user_create.password)
            #Por como lo definí, cuando lo creas sin role el role es client.
            # No validamos eso lo hace baseModel cuando se crea el User, si se le da un role que no existe en model User entonces no se crea el user.
            user = User(
                name=user_create.name,
                email=user_create.email,
                age=user_create.age,
                password=hashed_password
            )
            return await UserRepository.create_user_and_cart(user)
        except IntegrityError as e:
            raise DatabaseIntegrityException(str(e))
    
    @classmethod
    async def verify_user_and_password(cls, user_data: UserLogin) -> User:
        """
        Verify the user and password.
        """
        user = await UserRepository.get_user_login(user_data)
        
        # Verify the password
        if not cls.pwd_context.verify(user_data.password, user.password):
            raise InvalidCredentialsException("Las credenciales proporcionadas no coinciden.")
        
        return user
        
    @classmethod
    async def get_users(cls) -> list[User]:
        try:
            return await UserRepository.get_users()
        except Exception as e:
            raise InternalServerErrorException(str(e))
    
    @classmethod
    async def get_user(cls, user_id: UUID) -> User:
        return await UserRepository.get_user(user_id)
    
    @classmethod
    async def get_user_login(cls, user_data: UserLogin) -> User:
        return await cls.verify_user_and_password(user_data)
   
    @classmethod
    async def delete_user(cls, user_id: UUID) -> User:
        return await UserRepository.delete_user(user_id)
    
    @classmethod
    async def update_user(cls, user: User) -> User:
        try:
            return await UserRepository.update_user(user)
        except IntegrityError as e:
            raise DatabaseIntegrityException(str(e))
        
    #Falta preguntar si se bloquea el event loop cuando se ejecuta el .verify
    @classmethod
    async def patch_user_password(cls, user_id: UUID, user_data: UserPassword) -> User:
        
        #Ir por el user para traer su contraseña
        user = await UserRepository.get_user(user_id)
        
        # Verificar la contraseña que nos manda con la de la bd
        if not cls.pwd_context.verify(user_data.passwordActual, user.password):
            raise InvalidCredentialsException("Las credenciales proporcionadas no coinciden.")
        
        #Hasheamos la contraseña nueva.
        hashed_password = cls.hash_password(user_data.passwordNuevo)
        
        #Creamos la nueva data
        user_data_new = UserPassword(
            passwordActual = user.password,
            passwordNuevo = hashed_password
        )
        
        #Si todo esta bien entonces continuamos a cambiar la contraseña.
        return await UserRepository.patch_user_password(user_id, user_data_new)
    
    @classmethod
    async def patch_user(cls, user_id: UUID, user_patch: UserPatch) -> User:
        try:
            return await UserRepository.patch_user(user_id, user_patch)
        except IntegrityError as e:
            raise DatabaseIntegrityException(str(e))