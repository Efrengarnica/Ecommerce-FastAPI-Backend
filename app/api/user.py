from uuid import UUID
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, RedirectResponse, PlainTextResponse, HTMLResponse
from app.gateway.user import UserGateway
from app.models.user import User, UserPatch

router = APIRouter()

@router.post("/", response_model = User)
def create_user(user: User) -> User:
    return UserGateway.create_user(user)

@router.get("/")
def get_users() -> list[User]:
    return UserGateway.get_users()

@router.get("/{user_id}")
def get_user(user_id: UUID) -> User:
    return UserGateway.get_user(user_id)

@router.delete("/{user_id}")
def delete_user(user_id: UUID) -> User:
    return UserGateway.delete_user(user_id)

@router.put("/{user_id}")
def update_user(user_id: UUID, user: User) -> User:
    return UserGateway.update_user(user_id, user)

@router.patch("/{user_id}")
async def patch_user(request: Request, user_id: UUID) -> User:
    data = await request.json()
    return UserGateway.patch_user(user_id, UserPatch(**data))
    
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