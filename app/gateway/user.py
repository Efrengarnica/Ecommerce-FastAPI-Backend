from uuid import UUID
from fastapi import HTTPException
from app.models.user import User,UserPatch
from sqlmodel import Session
# Aqui debe de ir la conexion con el repository
from app.repository.user import UserRepository

class UserGateway:
    
    @classmethod
    def create_user(cls, user: User, session: Session) -> User:
        return UserRepository.create_user(session, user)
    
    @classmethod
    def get_users(cls, session: Session) -> list[User]:
        return UserRepository.get_users(session)
    
    @classmethod
    def get_user(cls, user_id: UUID, session: Session) -> User:
        return UserRepository.get_user(user_id, session)
        
    @classmethod
    def delete_user(cls, user_id: UUID, session: Session) -> User:
        return UserRepository.delete_user(user_id, session)
    
    @classmethod
    def update_user(cls, user_id: UUID, user: User, session: Session) -> User:
        if user_id != UUID(user.id):
            raise HTTPException(status_code=400, detail="User ID does not match")
        return UserRepository.update_user(user_id, user, session)

    @classmethod
    def patch_user(cls, user_id: UUID, user_patch: UserPatch, session: Session) -> User:
        return UserRepository.patch_user(user_id, user_patch, session)
