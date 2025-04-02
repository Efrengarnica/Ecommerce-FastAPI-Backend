from sqlmodel import Session, select
from app.models.user import User
from app.schemas.user import UserPatch
from uuid import UUID
from app.database import get_session
from app.exceptions.exceptions import (EmailAlreadyRegisteredException, UserNotFoundException)

class UserRepository:
    
    @staticmethod
    def create_user(user: User) -> User:
        with get_session() as session:
            statement = select(User).where(User.email == user.email)
            existing_user = session.exec(statement).first()
            # Validación de si el email ya está registrado
            if existing_user:
                raise EmailAlreadyRegisteredException(user.email)
            # Agregar el nuevo usuario
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
    
    @staticmethod
    def get_users() -> list[User]:
        with get_session() as session:
            query = select(User)
            all_users = session.exec(select(User)).all()
            return all_users

    @staticmethod
    def get_user(user_id: UUID) -> User:
        with get_session() as session:
            query = select(User).where(User.id == user_id)
            user = session.exec(query).first()
            if user:
                return user
            #Verificar que el usuario exista
            raise UserNotFoundException(user_id)
    
    @staticmethod
    def delete_user(user_id: UUID) -> User:
        with get_session() as session:
            user = session.get(User, user_id)
            #Verificar que el usuario exista
            if user is None:
                raise UserNotFoundException(user_id)
            session.delete(user)
            session.commit()
            return user

    @staticmethod
    def update_user(user: User) -> User:
        with get_session() as session:
            # Buscar el usuario por ID en la base de datos
            user_to_update = session.get(User, user.id)
            #Verificar que el usuario existe
            if user_to_update is None:
                raise UserNotFoundException(user.id)
            # Actualizar los campos del usuario
            user_to_update.name = user.name
            user_to_update.email = user.email
            user_to_update.age = user.age
            user_to_update.password = user.password 
            # Confirmar la actualización en la base de datos
            session.commit()
            # Refrescar el usuario para obtener los datos actualizados
            session.refresh(user_to_update)
            return user_to_update
    
    @staticmethod
    def patch_user(user_id: UUID, user_patch: UserPatch) -> User:
        with get_session() as session:
            user_to_update = session.get(User, user_id)
            #Verificar que el usuario exista
            if user_to_update is None:
                raise UserNotFoundException(user_id)
            # Verificar si el email que se quiere asignar ya está en uso
            if user_patch.email:
                existing_user = session.exec(select(User).where(User.email == user_patch.email)).first()
                if existing_user and existing_user.id != user_id:  # Verificar si el email pertenece a otro usuario
                    raise EmailAlreadyRegisteredException(user_patch.email)
            # Actualizar solo los campos proporcionados en user_patch
            #Cuando usas or en python aqui indica que si hay 2 true se queda con el primero
            user_to_update.name = user_patch.name or user_to_update.name
            user_to_update.email = user_patch.email or user_to_update.email
            user_to_update.age = user_patch.age or user_to_update.age
            user_to_update.password = user_patch.password or user_to_update.password
            session.commit()
            session.refresh(user_to_update)
            return user_to_update
    
    """ 
        Cosas que puedo llegar a hacer son session
        ✔ Obtener datos (get, all, filter, first)
        ✔ Insertar datos (add, add_all)
        ✔ Actualizar registros (update)
        ✔ Eliminar registros (delete)
        ✔ Consultas avanzadas (count, order_by, join)
        ✔ Manejo de transacciones (rollback) """