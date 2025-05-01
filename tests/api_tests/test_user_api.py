# tests/api/test_user_api.py  PYTHONPATH=$(pwd)/app pytest tests/api_tests/test_user_api.py
from pydantic import BaseModel
import pytest
from uuid import uuid4
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport # Sirve para hacer peticiones asíncronas
import pytest_asyncio

from models.user import User
from schemas.user import (
    UserCreate, UserResponse, UserLogin,
    UserPut, UserPassword, UserPatch
)
from api.user import router  # Aquí importamos el router de la API de nosotros.
from gateway.user import UserGateway
from gateway.authorization import AuthorizationGateway

# Montar aplicación y cliente asíncrono
app = FastAPI()
app.include_router(router, prefix="/users")  # Aquí incluimos el router de la API de nosotros.
# Esto es para que el cliente haga peticiones asíncronas a nuestra app.  

@pytest_asyncio.fixture
async def async_client():
    transport = ASGITransport(app=app) #Sirve para que el cliente haga peticiones asíncronas a la app.
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

# Fixture auto-applied para evitar llamadas reales a gateways
@pytest.fixture(autouse=True)
def no_http_requests(mocker):
    mocker.patch.object(UserGateway, "create_user", new=mocker.AsyncMock())
    mocker.patch.object(UserGateway, "create_user_and_cart", new=mocker.AsyncMock())
    mocker.patch.object(UserGateway, "get_users", new=mocker.AsyncMock())
    mocker.patch.object(UserGateway, "get_user", new=mocker.AsyncMock())
    mocker.patch.object(UserGateway, "get_user_login", new=mocker.AsyncMock())
    mocker.patch.object(UserGateway, "delete_user", new=mocker.AsyncMock())
    mocker.patch.object(UserGateway, "update_user", new=mocker.AsyncMock())
    mocker.patch.object(UserGateway, "patch_user_password", new=mocker.AsyncMock())
    mocker.patch.object(UserGateway, "patch_user", new=mocker.AsyncMock())
    mocker.patch.object(AuthorizationGateway, "token", new=mocker.AsyncMock())

@pytest.mark.asyncio
@pytest.mark.parametrize("endpoint,payload,method_name,stub_return,expected_body", [
    (
        "/",
        {"name": "Test", "email": "t@example.com", "age": 30, "password": "pw"},
        "create_user",
        User(id=uuid4(), name="Test", email="t@example.com", age=30, password="pw"),
        lambda u: {"id": str(u.id), "name": u.name, "email": u.email, "age": u.age, "role": u.role.value}
    ),
    (
        "/andCart",
        {"name": "Test2", "email": "t2@example.com", "age": 25, "password": "pw2"},
        "create_user_and_cart",
        User(id=uuid4(), name="Test2", email="t2@example.com", age=25, password="pw2"),
        lambda u: {"id": str(u.id), "name": u.name, "email": u.email, "age": u.age, "role": u.role.value}
    ),
])
async def test_post_create_user_variants(async_client, mocker, endpoint, payload, method_name, stub_return, expected_body):
    """Test to create a user and a user with cart."""
    # stubear método async con return_value
    getattr(UserGateway, method_name).return_value = stub_return #Me regresa un user fake.

    response = await async_client.post(f"/users{endpoint}", json=payload)
    assert response.status_code == 200
    assert response.json() == expected_body(stub_return)

    # validar llamada con el modelo serializado
    getattr(UserGateway, method_name).assert_awaited_once_with(
        UserCreate(**payload)
    )
    
@pytest.mark.asyncio
async def test_get_users(async_client):
    """Test to get all users."""
    u1 = User(id=uuid4(), name="A", email="a@b.com", age=None, password="x")
    u2 = User(id=uuid4(), name="B", email="b@c.com", age=None, password="y")
    UserGateway.get_users.return_value = [u1, u2]

    response = await async_client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert {item["email"] for item in data} == {u1.email, u2.email}
    UserGateway.get_users.assert_awaited_once()

@pytest.mark.asyncio
async def test_get_user(async_client):
    """Test to get a user by ID."""
    uid = uuid4()
    expected = User(id=uid, name="C", email="c@d.com", age=40, password="p")
    UserGateway.get_user.return_value = expected

    response = await async_client.get(f"/users/{uid}")
    assert response.status_code == 200
    assert response.json()["id"] == str(uid)
    UserGateway.get_user.assert_awaited_once_with(uid)

@pytest.mark.asyncio
@pytest.mark.parametrize("route,payload,stub_name,expected", [
    ("/login", {"email": "u@x.com", "password": "pw"}, "get_user_login", User(id=uuid4(), name="U", email="u@x.com", age=None, password="pw")),
    ("/login/token", {"email": "u@x.com", "password": "pw"}, "token", {"access_token":"abc123"}),
])
async def test_login_routes(async_client, route, payload, stub_name, expected):
    """Test to login a user and get a token."""
    target = AuthorizationGateway if stub_name == "token" else UserGateway
    getattr(target, stub_name).return_value = expected

    response = await async_client.post(f"/users{route}", json=payload)
    assert response.status_code == 200
    body = response.json()
    if isinstance(expected, BaseModel):
        # Convertimos UUIDs y excluimos campos no devueltos, como 'password', exluimos el password por que mi endpoint no lo devuelve.
        expected_body = expected.model_dump(mode="json", exclude={"password"})
    else:
        expected_body = expected

    assert body == expected_body
    
    getattr(target, stub_name).assert_awaited_once_with(
        UserLogin(**payload)
    )
    
@pytest.mark.asyncio
@pytest.mark.parametrize("method,route,stub_name,body", [
    ("delete", "/users/{}".format(uuid4()), "delete_user", None),
    ("put",    "/users/", "update_user", UserPut(id=uuid4(), name="X", email="e@e.com", age=20, password="pw").model_dump(mode="json") ),
    ("patch",  "/users/{}/changePassword".format(uuid4()), "patch_user_password", {"passwordActual":"o","passwordNuevo":"n"} ),
    ("patch",  "/users/{}".format(uuid4()), "patch_user", {"email":"nuevoEmail@gamil.com"} )
])
async def test_modify_routes(async_client, method, route, stub_name, body):
    """Test to delete, update and patch a user."""
    result = User(id=uuid4(), name="Z", email="z@z.com", age=99, password="p")
    getattr(UserGateway, stub_name).return_value = result

    client_call = getattr(async_client, method)
    if body is None:
        response = await client_call(route)
    else:
        response = await client_call(route, json=body)

    assert response.status_code == 200
    assert response.json()["email"] == result.email
    getattr(UserGateway, stub_name).assert_awaited_once()