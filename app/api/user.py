from uuid import UUID
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, RedirectResponse, PlainTextResponse, HTMLResponse
from app.gateway.user import UserGateway
from app.models.user import User
from app.schemas.user import UserPatch, UserResponse, UserCreate, UserPut

router = APIRouter()

@router.post("/", response_model = UserResponse)
def create_user(user_create: UserCreate) -> UserResponse:
    user_entity = User(**user_create.model_dump())
    created_user = UserGateway.create_user(user_entity)
    return UserResponse.model_validate(created_user)

@router.get("/", response_model=list[UserResponse])
def get_users() -> list[UserResponse]:
    users = UserGateway.get_users()
    return [UserResponse.model_validate(user) for user in users] 

@router.get("/{user_id}", response_model = UserResponse)
def get_user(user_id: UUID) -> UserResponse:
    created_user = UserGateway.get_user(user_id)
    return UserResponse.model_validate(created_user)

@router.delete("/{user_id}", response_model = UserResponse)
def delete_user(user_id: UUID) -> UserResponse:
    created_user = UserGateway.delete_user(user_id)
    return UserResponse.model_validate(created_user)

@router.put("/", response_model = UserResponse)
def update_user(user_create: UserPut) -> UserResponse:
    user_entity = User(**user_create.model_dump())
    created_user = UserGateway.update_user(user_entity)
    return UserResponse.model_validate(created_user)

@router.patch("/{user_id}")
async def patch_user(request: Request, user_id: UUID) -> UserResponse:
    data = await request.json()
    created_user = UserGateway.patch_user(user_id, UserPatch(**data))
    return UserResponse.model_validate(created_user)
    
@router.get("/html/")
def get_html() -> HTMLResponse:
    return HTMLResponse(content = "<h1>Hello, HTML User!</h1>", status_code = 200)

@router.get("/plain/")
def get_plain() -> PlainTextResponse:
    return PlainTextResponse(content = "Hello, Plain User!", status_code = 200)

@router.get("/redirect/")
def get_redirect() -> RedirectResponse:
    return RedirectResponse(url = "/users/plain/", status_code = 302)

@router.get("/json/")
def get_json() -> JSONResponse:
    return JSONResponse(content={"message": "Hello, JSON User!"}, status_code = 200)