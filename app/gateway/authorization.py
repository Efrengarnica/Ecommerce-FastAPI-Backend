import jwt #Recordar que aunque no este disponible aquí en tu contenedor si está intalado.
 
from fastapi import HTTPException

from settings.base import JWT_SECRET_KEY  #Esto es cuando queremos usar una varible de ambiente la traemos de base.py

from gateway.user import UserGateway

from schemas.user import UserLogin

##Importante hacer asyn para no bloquear el event loop.

##Además de faltar lo de arriba se tiene que hacer un metodo para verificar el token, con un verify y la firma secreta.

# Esta clase me tiene que ayudar a generar los tokens.
class AuthorizationGateway:
    # Define el tiempo que durará el token.
    token_expiration_time = 3600  # 1 hour
    secret_key = JWT_SECRET_KEY # Generate using 'openssl rand -hex 32', recuerda que se genera por consola, ya viene intalado.

    @classmethod
    async def token(cls, user_data:UserLogin) -> str:
        """
        Login the user and return a JWT token.
        """
        #Aqui ya se verifica si existe y si las credenciales son coreectas y lanza sus excepciones correspondientes.
        user = await UserGateway.verify_user_and_password(user_data)
        data = {
            "id": str(user.id),  #Se trasnforma el UUID ya que la libreria que crea el token no sabe como transformar el UUID, lo hacemos nosotros.
            "email": user.email,
        }
        token = cls._create_token(data)
        return token

    @classmethod
    def _create_token(cls, data: dict) -> str: #Al parecer jwt es tan rápido que no necesita ser asyn.
        """
        Create a JWT token.
        data example:
        {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "email": "some@example.com
        }
        """
        data["exp"] = cls.token_expiration_time
        token = jwt.encode(
            data,
            cls.secret_key,
            algorithm="HS256",
        )
        return token