from sqlite3 import IntegrityError
from uuid import UUID
from models.user import User
from schemas.user import UserLogin, UserPatch
from repository.user import UserRepository
from exceptions.exceptions import (DatabaseIntegrityException, InternalServerErrorException)

class UserGateway:
    
    @classmethod
    async def create_user(cls, user: User) -> User:
        try:
            return await UserRepository.create_user(user)
        except IntegrityError as e:
            raise DatabaseIntegrityException(str(e))
        
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
        return await UserRepository.get_user_login(user_data)
   
    @classmethod
    async def delete_user(cls, user_id: UUID) -> User:
        return await UserRepository.delete_user(user_id)
    
    @classmethod
    async def update_user(cls, user: User) -> User:
        try:
            return await UserRepository.update_user(user)
        except IntegrityError as e:
            raise DatabaseIntegrityException(str(e))

    @classmethod
    async def patch_user(cls, user_id: UUID, user_patch: UserPatch) -> User:
        try:
            return await UserRepository.patch_user(user_id, user_patch)
        except IntegrityError as e:
            raise DatabaseIntegrityException(str(e))