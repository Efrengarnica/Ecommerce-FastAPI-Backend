import pytest
from uuid import uuid4
from fastapi import HTTPException
from repository.user import UserRepository
from sqlmodel import select
from models.user import User
from models.cart import Cart
from schemas.user import UserLogin, UserPassword, UserPatch
from exceptions.exceptions import (
    EmailAlreadyRegisteredException,
    UserNotFoundException
)

# PYTHONPATH=$(pwd)/app pytest tests/repository_tests/test_user_repository.py, con esto se ejecuta.

"""Cada prueba guarda las cosas en la BD y no se borran los datos hasta que el test termine."""

@pytest.mark.asyncio(loop_scope="session")
async def test_create_user_success(async_session):
    """ Test para crear un usuario exitosamente. """
    user = User(name="Test", email="test@example.com", password="pw")
    created = await UserRepository.create_user(user)
    assert created.id == user.id
    assert created.email == "test@example.com"
    assert created.name == "Test"
    assert created.password == "pw"

@pytest.mark.asyncio(loop_scope="session")
async def test_create_user_duplicate_email(async_session):
    """ Test que me ayuda a verificar que no se pueda crear un usuario con el mismo email. """
    user1 = User(name="Usuario A", email="dup@example.com", password="pw")
    await UserRepository.create_user(user1)
    user2 = User(name="Usuario B", email="dup@example.com", password="pw2")
    with pytest.raises(EmailAlreadyRegisteredException):
        await UserRepository.create_user(user2)
        
@pytest.mark.asyncio(loop_scope="session")
async def test_get_users(async_session):
    """ Test para obtener todos los usuarios. """
    u1 = User(name="U1", email="u1@example.com", password="pw")
    u2 = User(name="U2", email="u2@example.com", password="pw2")
    await UserRepository.create_user(u1)
    await UserRepository.create_user(u2)
    all_users = await UserRepository.get_users()
    emails = {u.email for u in all_users}
    assert {"u1@example.com", "u2@example.com"} <= emails #Como los datos anteriores de los otros tests existen en la bd deberé de preguntar
    #si los que agregué estan contenidos en la bd.

@pytest.mark.asyncio(loop_scope="session")
async def test_get_user(async_session):
    """ Test para obtener un usuario por su id. """
    user = User(name="U3", email="nuevo@gmail.com", password="pw")
    await UserRepository.create_user(user)
    fetched = await UserRepository.get_user(user.id)
    assert fetched.email == user.email
    assert fetched.name == user.name
    
@pytest.mark.asyncio(loop_scope="session")
async def test_get_user_not_found(async_session):
    """ Test para obtener un usuario que no existe. """
    with pytest.raises(UserNotFoundException):
        await UserRepository.get_user(uuid4())
        
@pytest.mark.asyncio(loop_scope="session")
async def test_get_user_login(async_session):
    """ Test para obtener un usuario, pero de Login. """
    data = UserLogin(email="nuevo@gmail.com", password="pw")
    fetched = await UserRepository.get_user_login(data)
    assert fetched.email == data.email
    assert fetched.password == data.password   
        
@pytest.mark.asyncio(loop_scope="session")
async def test_get_user_login_not_found(async_session):
    """ Test para obtener un usuario que no existe, pero de Login. """
    data = UserLogin(email="none@example.com", password="pw")
    with pytest.raises(HTTPException):
        await UserRepository.get_user_login(data)

@pytest.mark.asyncio(loop_scope="session")
async def test_delete_user_and_not_found(async_session):
    """ Test para eliminar un usuario y verificar que no existe. """
    user = User(name="Del", email="del@example.com", password="pw")
    await UserRepository.create_user(user)

    deleted = await UserRepository.delete_user(user.id)
    assert deleted.id == user.id

    with pytest.raises(UserNotFoundException):
        await UserRepository.delete_user(user.id)
    
@pytest.mark.asyncio(loop_scope="session")
async def test_update_user(async_session):
    """ Test para actualizar un usuario, con todo y excepcion. """
    user = User(name="Up", email="up@example.com", password="pw")
    await UserRepository.create_user(user)
    user.name = "Up2"
    updated = await UserRepository.update_user(user)
    assert updated.name == "Up2"
    
    await UserRepository.delete_user(user.id)
    with pytest.raises(UserNotFoundException):
        await UserRepository.update_user(user)
        
@pytest.mark.asyncio(loop_scope="session")
async def test_patch_user_password(async_session):
    """ Test para parchear la contraseña de un usuario. """
    user = User(name="PW", email="pw@example.com", password="oldpw")
    await UserRepository.create_user(user)

    patched = await UserRepository.patch_user_password(
        user.id,
        UserPassword(passwordActual = "oldpw", passwordNuevo="newpw")
    )
    assert patched.password == "newpw"
    
@pytest.mark.asyncio(loop_scope="session")
async def test_patch_user(async_session):
    """ Test para parchear un usuario. """
    user = User(name="P11", email="random@gmail.com", password="pw")
    await UserRepository.create_user(user)
    patched = await UserRepository.patch_user(
        user.id,
        UserPatch(name="P12", email="random2@gmail.com")
    )
    assert patched.name == "P12"
    assert patched.email == "random2@gmail.com"
    
@pytest.mark.asyncio(loop_scope="session")
async def test_patch_user_not_found(async_session):
    """ Test para parchear un usuario que no existe. """
    with pytest.raises(UserNotFoundException):
        await UserRepository.patch_user(
            uuid4(),
            UserPatch(email = "oldpw")
        )    
        
@pytest.mark.asyncio(loop_scope="session")
async def test_patch_user_and_conflict(async_session):
    """ Test para parchear un usuario, pero con conflicto de email. """
    # Creamos dos users
    u1 = User(name="E1", email="e1@example.com", password="pw")
    u2 = User(name="E2", email="e2@example.com", password="pw")
    await UserRepository.create_user(u1)
    await UserRepository.create_user(u2)

    # Intentamos parchear u1 con el email de u2 → debe fallar
    with pytest.raises(EmailAlreadyRegisteredException):
        await UserRepository.patch_user(u1.id, UserPatch(email=u2.email))
                
@pytest.mark.asyncio(loop_scope="session")
async def test_create_user_and_cart_success(async_session):
    """Test para verificar que se creó un user and cart de manera exitosa."""
    user = User(name="C", email="c@example.com", password="pw")
    created = await UserRepository.create_user_and_cart(user)
    assert created.id == user.id

    # Verificamos que el cart se creó
    carts = (await async_session.execute(
        select(Cart).where(Cart.user_id == user.id)
    )).scalars().all()
    assert len(carts) == 1
    assert carts[0].user_id == user.id
                
@pytest.mark.asyncio(loop_scope="session")
async def test_create_user_duplicate(async_session):
    """Test para verificar que no se cree un user and cart duplicado."""
    user = User(name="D", email="dttt@example.com", password="pw")
    # primer insert crea user + cart
    await UserRepository.create_user_and_cart(user)
    # el segundo debe fallar por CartAlreadyRegisteredException
    with pytest.raises(EmailAlreadyRegisteredException):
        await UserRepository.create_user_and_cart(user)