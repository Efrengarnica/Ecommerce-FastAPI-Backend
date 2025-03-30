from uuid import UUID
from fastapi import HTTPException
from app.models.user import User,UserPatch
from app.repository.user import UserRepository

class UserGateway:
    
    @classmethod
    def create_user(cls, user: User) -> User:
        return UserRepository.create_user(user)
    
    @classmethod
    def get_users(cls) -> list[User]:
        return UserRepository.get_users()
    
    @classmethod
    def get_user(cls, user_id: UUID) -> User:
        return UserRepository.get_user(user_id)
        
    @classmethod
    def delete_user(cls, user_id: UUID) -> User:
        return UserRepository.delete_user(user_id)
    
    @classmethod
    def update_user(cls, user_id: UUID, user: User) -> User:
        if user_id != UUID(user.id):
            raise HTTPException(status_code = 400, detail = "User ID does not match")
        return UserRepository.update_user(user_id, user)

    @classmethod
    def patch_user(cls, user_id: UUID, user_patch: UserPatch) -> User:
        return UserRepository.patch_user(user_id, user_patch)