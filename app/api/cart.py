from fastapi import APIRouter, Request
from uuid import UUID
from typing import List
from models.cart import Cart, CartItem
from schemas.cart import CartCreate, CartResponse, CartItemCreate, CartItemResponse, CartItemPatch
from gateway.cart import CartGateway

#Importante ya que tengo distintas entidades entonces tengo que tener endpoints distintos.
#Esto conecta los controllers con la app prinicpal de FastApi
router = APIRouter()

# Endpoints para Cart
@router.post("/", response_model = CartResponse)
async def create_cart(cart_create: CartCreate) -> CartResponse:
    created_cart = await CartGateway.create_cart(cart_create)
    return CartResponse.model_validate(created_cart)

@router.get("/", response_model = list[CartResponse])
async def get_carts() -> List[CartResponse]:
    carts = await CartGateway.get_carts()
    return [CartResponse.model_validate(cart) for cart in carts]

@router.get("/{user_id}", response_model = CartResponse)
async def get_cart(user_id: UUID) -> CartResponse:
    created_cart = await CartGateway.get_cart(user_id)
    return CartResponse.model_validate(created_cart)

@router.delete("/{cart_id}", response_model = CartResponse)
async def delete_cart(cart_id: UUID) -> CartResponse:
    delete_cart = await CartGateway.delete_cart(cart_id)
    return CartResponse.model_validate(delete_cart)

@router.delete("/{cart_id}/clear", response_model = CartResponse)
async def clear_cart_items(cart_id: UUID) -> CartResponse:
    clear_cart = await CartGateway.clear_cart_items(cart_id)
    return CartResponse.model_validate(clear_cart)


# Endpoints para CartItem
""" Recuerda, aqui ya no lo aplique pero debes de saber que cuando le pasas un modelo SQLModel con table = True 
    habrá veces que FastApi intente transformar datos complejos como uuid, en la solicitud, y le salga bien antes de hacer la instancia de User
    pero habra veces que cree user sin hacer las debidas conversiones y eso te marcara error, lo mejor es hacer tus entidades y 
    crear otra clase con los mismos tipos de datos que tus entidades para que esas solo ocupen SQLMODEL y si verifique y convierta todo de 
    manera correcta.
    Aqui en este POST lo aplique así.
"""
@router.post("/items/", response_model = CartItemResponse)
async def add_item_to_cart(cart_item_create: CartItemCreate) -> CartItemResponse:
    cart_item_entity = CartItem(**cart_item_create.model_dump())
    created_cart_item = await CartGateway.add_item_to_cart(cart_item_entity)
    return CartItemResponse.model_validate(created_cart_item)
  
@router.delete("/items/{cart_item_id}", response_model = CartItemResponse)
async def delete_cart_item(cart_item_id: UUID) -> CartItemResponse:
    eliminated_cart_item = await CartGateway.delete_cart_item(cart_item_id)
    return CartItemResponse.model_validate(eliminated_cart_item)

@router.patch("/items/{cart_item_id}", response_model = CartItemResponse)
async def patch_cart_item(cart_item_id: UUID, request: Request ) -> CartItemResponse:
    data = await request.json()
    created_cart_item = await CartGateway.patch_cart_item(cart_item_id, CartItemPatch(**data))
    return CartItemResponse.model_validate(created_cart_item)