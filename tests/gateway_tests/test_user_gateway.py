# tests/gateway/test_user_gateway.py
import pytest
from uuid import uuid4
from sqlite3 import IntegrityError
from unittest.mock import AsyncMock  #Para poder usar el mocker de pytest.
from unittest.mock import ANY #Para poder omitir el id en el test.

from models.user import User
from schemas.user import UserCreate, UserLogin, UserPassword, UserPatch
from gateway.user import UserGateway
from repository.user import UserRepository
from exceptions.exceptions import (
    DatabaseIntegrityException,
    InternalServerErrorException,
    InvalidCredentialsException,
)

@pytest.mark.asyncio
async def test_hash_and_verify_password_roundtrip():
    """Test that hashing and verifying a password works correctly."""
    plain = "mi_secreto"
    hashed = await UserGateway.hash_password(plain)
    assert isinstance(hashed, str)
    assert await UserGateway.verify_password(plain, hashed)
    
@pytest.mark.asyncio
async def test_create_user_success(mocker):
    """Test that creating a user works correctly."""
    payload = UserCreate(name="Ana", email="ana@example.com", age=25, password="pw")
    fake_user = User(id=uuid4(), name=payload.name, email=payload.email, age=payload.age, password="hashed_pw")

    # Stub hash_password
    mocker.patch.object(
        UserGateway,
        "hash_password",
        new=AsyncMock(return_value="hashed_pw"),
    )
    # Stub repositorio
    mocker.patch.object(
        UserRepository,
        "create_user",
        new=AsyncMock(return_value=fake_user),
    )

    created = await UserGateway.create_user(payload)
    assert created is fake_user
    UserGateway.hash_password.assert_called_once_with(payload.password)
    UserRepository.create_user.assert_called_once_with(
        User(
            id=ANY,  #Necesito esto ya que en gateway se crea un id distinto al que definí en fake_user.
            name=payload.name,
            email=payload.email,
            age=payload.age,
            password="hashed_pw"
        )
    )
    
@pytest.mark.asyncio
async def test_create_user_integrity_error(mocker):
    """Test that creating a user with an existing id."""
    payload = UserCreate(name="Ana", email="dup@example.com", age=25, password="pw")

    mocker.patch.object(
        UserGateway,
        "hash_password",
        new=AsyncMock(return_value="hashed_pw"),
    )
    mocker.patch.object(
        UserRepository,
        "create_user",
        new=AsyncMock(side_effect=IntegrityError("unique violation", None, None)),
    )

    with pytest.raises(DatabaseIntegrityException) as exc:
        await UserGateway.create_user(payload)
        
    assert "unique violation" in str(exc.value)
    
    UserGateway.hash_password.assert_called_once()
    UserRepository.create_user.assert_called_once()
    
@pytest.mark.asyncio
async def test_verify_user_and_password_success(mocker):
    """Test that verifying a user and password works correctly."""
    credentials = UserLogin(email="u@example.com", password="pw")
    fake_user = User(id=uuid4(), name="U", email=credentials.email, password="hashed_pw")

    mocker.patch.object(
        UserRepository,
        "get_user_login",
        new=AsyncMock(return_value=fake_user),
    )
    mocker.patch.object(
        UserGateway,
        "verify_password",
        new=AsyncMock(return_value=True),
    )

    result = await UserGateway.verify_user_and_password(credentials)
    assert result is fake_user
    UserRepository.get_user_login.assert_called_once_with(credentials)
    UserGateway.verify_password.assert_called_once_with(credentials.password, fake_user.password)
    
@pytest.mark.asyncio
async def test_verify_user_and_password_fail(mocker):
    """Test that verifying a user and password fails with invalid credentials."""
    credentials = UserLogin(email="u@example.com", password="pw")
    fake_user = User(id=uuid4(), name="U", email=credentials.email, age=None, password="hashed_pw")

    mocker.patch.object(
        UserRepository,
        "get_user_login",
        new=AsyncMock(return_value=fake_user),
    )
    mocker.patch.object(
        UserGateway,
        "verify_password",
        new=AsyncMock(return_value=False),
    )

    with pytest.raises(InvalidCredentialsException):
        await UserGateway.verify_user_and_password(credentials)
    
@pytest.mark.asyncio
async def test_get_users_success(mocker):
    """Test that getting users works correctly."""
    u1 = User(id=uuid4(), name="A", email="a@b.com", age=None, password="x")
    u2 = User(id=uuid4(), name="B", email="b@c.com", age=None, password="y")

    mocker.patch.object(
        UserRepository,
        "get_users",
        new=AsyncMock(return_value=[u1, u2]),
    )

    users = await UserGateway.get_users()
    assert users == [u1, u2]
    UserRepository.get_users.assert_called_once()
    
@pytest.mark.asyncio
async def test_get_users_internal_error(mocker):
    """ Test that getting users raises an internal server error."""
    mocker.patch.object(
        UserRepository,
        "get_users",
        new=AsyncMock(side_effect=RuntimeError("boom")),
    )

    with pytest.raises(InternalServerErrorException) as exc:
        await UserGateway.get_users()
    assert "boom" in str(exc.value)

@pytest.mark.asyncio
async def test_passthrough_methods(mocker):
    """Test that passthrough methods call the repository methods correctly."""
    # get_user, delete_user, update_user, patch_user
    methods = ["get_user", "delete_user", "update_user", "patch_user"]
    for method in methods:
        fake = object()
        mocker.patch.object(
            UserRepository,
            method,
            new=AsyncMock(return_value=fake),
        )
        gw_method = getattr(UserGateway, method)
        if method == "patch_user":
            result = await gw_method(uuid4(), UserPatch(name="X"))
        else:
            result = await gw_method(uuid4())
        assert result is fake
        getattr(UserRepository, method).assert_called_once()
    
@pytest.mark.asyncio
async def test_get_user_login(mocker):
    """Test that get_user_login calls the repository method correctly."""
    
    fake = object()
    mocker.patch.object(
        UserRepository,
        "get_user_login",
        new=AsyncMock(return_value=fake),
    )
    mocker.patch.object(
        UserGateway,
        "verify_user_and_password",
        new=AsyncMock(return_value=fake),
    )
    mocker.patch.object(
        UserGateway,
        "verify_password",
        new=AsyncMock(return_value=False),
    )
    
    result = await UserGateway.get_user_login(UserLogin(email="x@x.com", password="pw"))
    assert result is fake
    
    UserGateway.verify_user_and_password.assert_called_once()
   
@pytest.mark.asyncio
async def test_patch_user_password_flow(mocker):
    """Test that patching a user's password works correctly."""
    uid = uuid4()
    fake_user = User(id=uid, name="U", email="u@x.com", age=None, password="old_hashed")

    mocker.patch.object(
        UserRepository,
        "get_user",
        new=AsyncMock(return_value=fake_user),
    )
    mocker.patch.object(
        UserGateway,
        "verify_password",
        new=AsyncMock(return_value=True),
    )
    mocker.patch.object(
        UserGateway,
        "hash_password",
        new=AsyncMock(return_value="new_hashed"),
    )
    updated = User(id=uid, name="U", email="u@x.com", age=None, password="new_hashed")
    mocker.patch.object(
        UserRepository,
        "patch_user_password",
        new=AsyncMock(return_value=updated),
    )

    result = await UserGateway.patch_user_password(
        uid,
        UserPassword(passwordActual="old", passwordNuevo="new")
    )
    assert result is updated
    
    UserRepository.patch_user_password.assert_called_once()

@pytest.mark.asyncio
async def test_patch_user_password_invalid_current(mocker):
    """Test that patching a user's password fails with invalid current password."""
    uid = uuid4()
    fake_user = User(id=uid, name="U", email="u@x.com", age=None, password="hashed_old")

    mocker.patch.object(
        UserRepository,
        "get_user",
        new=AsyncMock(return_value=fake_user),
    )
    mocker.patch.object(
        UserGateway,
        "verify_password",
        new=AsyncMock(return_value=False),
    )

    with pytest.raises(InvalidCredentialsException):
        await UserGateway.patch_user_password(
            uid,
            UserPassword(passwordActual="wrong", passwordNuevo="new")
        )