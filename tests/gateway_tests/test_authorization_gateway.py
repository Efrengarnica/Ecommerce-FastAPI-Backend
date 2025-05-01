# tests/gateway/test_authorization_gateway.py
import pytest
import jwt
from uuid import uuid4
from fastapi import HTTPException

from gateway.authorization import AuthorizationGateway
from gateway.user import UserGateway
from schemas.user import UserLogin
from models.user import User
from settings.base import JWT_SECRET_KEY


@pytest.mark.asyncio
async def test_token_success(mocker):
    """Test successful token generation."""
    # 1) Preparamos los datos de login y el usuario fake que devolverá el verify
    credentials = UserLogin(email="u@x.com", password="pw")
    fake_user = User(
        id=uuid4(),
        name="U",
        email=credentials.email,
        age=None,
        password="hashed_pw",
    )

    # 2) Stubeamos el verify_user_and_password para que devuelva nuestro fake_user
    mocker.patch.object(
        UserGateway,
        "verify_user_and_password",
        new=mocker.AsyncMock(return_value=fake_user),
    )

    # 3) Llamamos al método token()
    token_str = await AuthorizationGateway.token(credentials)
    
    #Se verifica que regrese un string
    assert isinstance(token_str, str)

    # 4) Decodificamos el JWT para verificar su contenido
    payload = jwt.decode(
    token_str,
    JWT_SECRET_KEY,
    algorithms=["HS256"],
    options={"verify_exp": False}
)


    # Se verifica que los campos que pusimos están.
    assert payload["id"] == str(fake_user.id)
    assert payload["email"] == fake_user.email
    # Expiración debe estar según token_expiration_time
    assert payload["exp"] == AuthorizationGateway.token_expiration_time

    # 5) Verificamos que el verify fue llamado con los mismos credentials
    UserGateway.verify_user_and_password.assert_awaited_once_with(credentials)
    #AuthorizationGateway._create_token.assert_called_once()
    
@pytest.mark.asyncio
async def test_token_invalid_credentials(mocker):
    """Test token generation with invalid credentials."""
    # Si la verificación falla lanzando HTTPException, token() debe propagarla
    credentials = UserLogin(email="bad@x.com", password="wrong")
    mocker.patch.object(
        UserGateway,
        "verify_user_and_password",
        new=mocker.AsyncMock(side_effect=HTTPException(status_code=401, detail="bad creds")),
    )

    with pytest.raises(HTTPException) as exc:
        await AuthorizationGateway.token(credentials)
    assert exc.value.status_code == 401
    assert "bad creds" in exc.value.detail
    
def test_create_token_directly():
    """Test token creation without async."""
    # Podemos probar _create_token sin async
    data = {"id": "123", "email": "a@b.com"}
    token_str = AuthorizationGateway._create_token(data.copy())
    payload = jwt.decode(token_str, JWT_SECRET_KEY, algorithms=["HS256"], options={"verify_exp": False})
    # Verificamos que haya preservado id y email y agregado exp
    assert payload["id"] == "123"
    assert payload["email"] == "a@b.com"
    assert payload["exp"] == AuthorizationGateway.token_expiration_time