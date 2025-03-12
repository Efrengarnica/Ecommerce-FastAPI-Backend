from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse, PlainTextResponse, HTMLResponse
from app.gateway.user import UserGateway
from app.models.user import User, UserPatch
from sqlmodel import Session
from app.database import get_session
from uuid import UUID
from typing import List
from app.models.cart import Cart, CartItem, CartCreate, CartItemCreate, CartResponse, CartItemPatch
from app.gateway.cart import CartGateway


#Importante ya que tengo distintas entidades entonces tengo que tener endpoints distintos
router = APIRouter()

# Endpoints para la entidad Cart

@router.post("/", response_model=Cart)
def create_cart(cart_data: CartCreate, session: Session = Depends(get_session)) -> Cart:
    # Aquí, cart_data.user_id ya es un UUID, gracias a la validación de Pydantic.
    cart = Cart(user_id=cart_data.user_id)
    return CartGateway.create_cart(cart, session)

@router.get("/")
def get_carts(session: Session = Depends(get_session)) -> List[Cart]:
    return CartGateway.get_carts(session)

@router.get("/{cart_id}", response_model=CartResponse)
def get_cart(cart_id: UUID, session: Session = Depends(get_session)) -> Cart:
    return CartGateway.get_cart(cart_id, session)

@router.delete("/{cart_id}")
def delete_cart(cart_id: UUID, session: Session = Depends(get_session)) -> Cart:
    return CartGateway.delete_cart(cart_id, session)


# Endpoints para la entidad CartItem

@router.post("/{cart_id}/items/", response_model=CartItem)
def add_item_to_cart(cart_id: UUID, cart_item_create: CartItemCreate, session: Session = Depends(get_session)) -> CartItem:
    cart_item = CartItem(cart_id= cart_item_create.cart_id, product_id= cart_item_create.product_id)
    return CartGateway.add_item_to_cart(cart_id, cart_item, session)
  

@router.delete("/{cart_id}/items/{cart_item_id}/")
def delete_cart_item(cart_id: UUID, cart_item_id: UUID, session: Session = Depends(get_session)) -> CartItem:
    return CartGateway.delete_cart_item(cart_item_id, session)


@router.patch("/{cart_id}/items/{cart_item_id}/")
async def patch_cart_item(cart_id: UUID, cart_item_id: UUID, request: Request , session: Session = Depends(get_session)) -> CartItem:
    data = await request.json()
    return CartGateway.patch_cart_item(cart_item_id, CartItemPatch(**data), session)
    
    
