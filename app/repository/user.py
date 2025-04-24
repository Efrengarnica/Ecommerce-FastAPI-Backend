from fastapi import HTTPException
from sqlmodel import Session, select
from models.cart import Cart
from models.user import User
from schemas.user import UserLogin, UserPassword, UserPatch
from uuid import UUID
from database import get_session
from exceptions.exceptions import (CartAlreadyRegisteredException, EmailAlreadyRegisteredException, InvalidCredentialsException, UserNotFoundException)

class UserRepository:
    
    @staticmethod
    async def create_user(user: User) -> User:
        async with get_session() as session:  # AsyncSession
            # 1. Comprobamos si ya existe
            stmt = select(User).where(User.email == user.email)
            result = await session.execute(stmt)
            existing_user = result.scalars().first()
            if existing_user:
                raise EmailAlreadyRegisteredException(user.email)
            # 2. Insertamos
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user
    
    #Me sirve al momento de registrar un usuario y poder estar atento a los 2 tipos de error, el error al crear un usuario y al crear un cart
    #si llegara a usar los 2 por separados podria llegar a crearse un user sin cart, es por eso que ocupo esto.
    @staticmethod
    async def create_user_and_cart(user: User) -> User:
        async with get_session() as session:
            
            # Apartado que verifica lo del User
            
            #Verifico que no haya un user con ese email.
            stmt = select(User).where(User.email == user.email)
            result = await session.execute(stmt)
            existing_user = result.scalars().first()
            if existing_user:
                raise EmailAlreadyRegisteredException(user.email)
            
            #Apartado que verifica lo de Cart
            
            #Verifico que no exista otro cart asociado a ese id.
            stmt = select(Cart).where(Cart.user_id == user.id)
            result = await session.execute(stmt)
            existing_cart = result.scalars().first()
            if existing_cart:
                raise CartAlreadyRegisteredException(existing_cart.id, user.id)

            #Una vez verificado se agrega el user y el cart
            new_cart = Cart(user_id = user.id)
            session.add(user)
            await session.commit()
            await session.refresh(user)
            session.add(new_cart)
            await session.commit()
            await session.refresh(new_cart)
            
            return user
            
    @staticmethod
    async def get_users() -> list[User]:
        async with get_session() as session:
            # Ejecutar y devolver lista de Users
            result = await session.execute(select(User))
            return result.scalars().all()

    @staticmethod
    async def get_user(user_id: UUID) -> User:
        async with get_session() as session:
            stmt = select(User).where(User.id == user_id)
            result = await session.execute(stmt)
            user = result.scalars().first()
            if not user:
                raise UserNotFoundException(user_id)
            return user
    
    @staticmethod
    async def get_user_login(user_data: UserLogin) -> User:
        async with get_session() as session:
            stmt = select(User).where(User.email == user_data.email)
            result = await session.execute(stmt)
            user = result.scalars().first()

            if not user:
                raise HTTPException(status_code=404, detail="No hay usuario registrado con ese email.")
            #if user.password != user_data.password:
             #   raise InvalidCredentialsException("Las credenciales proporcionadas no coinciden.")
            return user
    
    @staticmethod
    async def delete_user(user_id: UUID) -> User:
        async with get_session() as session:
            user = await session.get(User, user_id)
            if not user:
                raise UserNotFoundException(user_id)
            await session.delete(user)
            await session.commit()
            return user
        
    @staticmethod
    async def update_user(user: User) -> User:
        async with get_session() as session:
            # Buscamos la entidad existente
            existing = await session.get(User, user.id)
            if not existing:
                raise UserNotFoundException(user.id)

            # Sobrescribimos campos
            existing.name = user.name
            existing.email = user.email
            existing.age = user.age
            existing.password = user.password

            await session.commit()
            await session.refresh(existing)
            return existing
        
    @staticmethod
    async def patch_user_password(user_id: UUID, user_data: UserPassword) -> User:
        async with get_session() as session:
            #No se verifica que exista ya que ya se verifica en la capa de gateway cuando se consigue por get_user
            user = await session.get(User, user_id)
            user.password = user_data.passwordNuevo
            await session.commit()
            await session.refresh(user)
            return user
            
    @staticmethod
    async def patch_user(user_id: UUID, user_patch: UserPatch) -> User:
        async with get_session() as session:
            existing = await session.get(User, user_id)
            if not existing:
                raise UserNotFoundException(user_id)

            # Si cambian el email, validamos unicidad
            if user_patch.email:
                stmt = select(User).where(User.email == user_patch.email)
                result = await session.execute(stmt)
                conflict = result.scalars().first()
                if conflict and conflict.id != user_id:
                    raise EmailAlreadyRegisteredException(user_patch.email)

            # Actualizamos solo los campos proporcionados
            if user_patch.name is not None:
                existing.name = user_patch.name
            if user_patch.email is not None:
                existing.email = user_patch.email
            if user_patch.age is not None:
                existing.age = user_patch.age
            if user_patch.password is not None:
                existing.password = user_patch.password

            await session.commit()
            await session.refresh(existing)
            return existing
    
    """ 
        Cosas que puedo llegar a hacer son session
        ✔ Obtener datos (get, all, filter, first)
        ✔ Insertar datos (add, add_all)
        ✔ Actualizar registros (update)
        ✔ Eliminar registros (delete)
        ✔ Consultas avanzadas (count, order_by, join)
        ✔ Manejo de transacciones (rollback) """