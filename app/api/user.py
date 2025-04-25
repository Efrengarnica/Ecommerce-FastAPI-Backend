from uuid import UUID
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, RedirectResponse, PlainTextResponse, HTMLResponse
from gateway.user import UserGateway
from gateway.authorization import AuthorizationGateway
from models.user import User
from schemas.user import UserPassword, UserPatch, UserResponse, UserCreate, UserPut, UserLogin

router = APIRouter()

@router.post("/", response_model = UserResponse)
async def create_user(user_create: UserCreate) -> UserResponse:
    #user_entity = User(**user_create.model_dump())
    created_user = await UserGateway.create_user(user_create)
    return UserResponse.model_validate(created_user)

@router.post("/andCart", response_model = UserResponse)
async def create_user_and_cart(user_create: UserCreate) -> UserResponse:
    created_user = await UserGateway.create_user_and_cart(user_create)
    return UserResponse.model_validate(created_user)
    
@router.get("/", response_model=list[UserResponse])
async def get_users() -> list[UserResponse]:
    users = await UserGateway.get_users()
    return [UserResponse.model_validate(user) for user in users] 

@router.get("/{user_id}", response_model = UserResponse)
async def get_user(user_id: UUID) -> UserResponse:
    created_user = await UserGateway.get_user(user_id)
    return UserResponse.model_validate(created_user)

#Cuando usas get no es recomendable a pesar de que quieras conseguir datos
#usarlo para enviar cosas por medio del body, si quieres conseguir algo
#por medio de datos es usar post, para no enviar datos sensibles en la url.
@router.post("/login", response_model = UserResponse)
async def get_user_login(user_data:UserLogin) -> UserResponse:
    created_user = await UserGateway.get_user_login(user_data)
    return UserResponse.model_validate(created_user)

# Aqui no voy a modificar aún mi manera de hacer login hasta que sepa:
# Como implementar de manera completa lo del token, cookie y verificacion del token.
# Por ahora solo me limito a escribir endpoint que remplzara al login de arriba como método de inicio de sesión.
@router.post("/login/token")
async def get_user_login_by_token(user_data:UserLogin):
    """
        Create tokens for authentication
    """
    #Hay 2 maneras si usas cookies, regresar la cookie y el user o solo la cookie, me decanto solo por regresar la cookie y depsues pedir los datos.
    
    #Esta es una manera provisional ya que tendria aqui en este router que implementar la forma de que se envie la cookie con el token.
    # y regrese solo un mensaje de exito o algo así.
    # Está forma es para yo guardar el token como yo decia, pero es vulnerable el token. 
    return await AuthorizationGateway.token(user_data)
    
    

@router.delete("/{user_id}", response_model = UserResponse)
async def delete_user(user_id: UUID) -> UserResponse:
    created_user = await UserGateway.delete_user(user_id)
    return UserResponse.model_validate(created_user)

@router.put("/", response_model = UserResponse)
async def update_user(user_create: UserPut) -> UserResponse:
    user_entity = User(**user_create.model_dump())
    created_user = await UserGateway.update_user(user_entity)
    return UserResponse.model_validate(created_user)

@router.patch("/{user_id}/changePassword", response_model = UserResponse)
async def patch_user_password(user_data: UserPassword, user_id: UUID) -> UserResponse:
    created_user = await UserGateway.patch_user_password(user_id, user_data)
    return UserResponse.model_validate(created_user)

@router.patch("/{user_id}", response_model = UserResponse)
async def patch_user(request: Request, user_id: UUID) -> UserResponse:
    data = await request.json()
    created_user = await UserGateway.patch_user(user_id, UserPatch(**data))
    return UserResponse.model_validate(created_user)
    
@router.get("/html/")
async def get_html() -> HTMLResponse:
    return HTMLResponse(content = "<h1>Hello, HTML User!</h1>", status_code = 200)

@router.get("/plain/")
async def get_plain() -> PlainTextResponse:
    return PlainTextResponse(content = "Hello, Plain User!", status_code = 200)

@router.get("/redirect/")
async def get_redirect() -> RedirectResponse:
    return RedirectResponse(url = "/users/plain/", status_code = 302)

@router.get("/json/")
async def get_json() -> JSONResponse:
    return JSONResponse(content={"message": "Hello, JSON User!"}, status_code = 200)