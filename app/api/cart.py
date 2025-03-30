from fastapi import APIRouter, Request
from uuid import UUID
from typing import List
from app.models.cart import Cart, CartItem, CartCreate, CartItemCreate, CartResponse, CartItemPatch
from app.gateway.cart import CartGateway

#Importante ya que tengo distintas entidades entonces tengo que tener endpoints distintos.
#Esto conecta los controllers con la app prinicpal de FastApi
router = APIRouter()

# Endpoints para Cart
@router.post("/", response_model = Cart)
def create_cart(cart_data: CartCreate) -> Cart:
    cart = Cart(user_id = cart_data.user_id)
    return CartGateway.create_cart(cart)

@router.get("/")
def get_carts() -> List[Cart]:
    return CartGateway.get_carts()

#CartResponse me ayuda que se puedan mostrar los items, además debes de agregarle algo al repository para que funcione y tambien en el model.
@router.get("/{cart_id}", response_model = CartResponse)
def get_cart(cart_id: UUID) -> Cart:
    return CartGateway.get_cart(cart_id)

@router.delete("/{cart_id}")
def delete_cart(cart_id: UUID) -> Cart:
    return CartGateway.delete_cart(cart_id)

# Endpoints para CartItem
""" Recuerda, aqui ya no lo aplique pero debes de saber que cuando le pasas un modelo SQLModel con table = True 
    habrá veces que FastApi intente transformar datos complejos como uuid, en la solicitud, y le salga bien antes de hacer la instancia de User
    pero habra veces que cree user sin hacer las debidas conversiones y eso te marcara error, lo mejor es hacer tus entidades y 
    crear otra clase con los mismos tipos de datos que tus entidades para que esas solo ocupen SQLMODEL y si verifique y convierta todo de 
    manera correcta.
    Aqui en este POST lo aplique así.
"""
@router.post("/{cart_id}/items/", response_model = CartItem)
def add_item_to_cart(cart_id: UUID, cart_item_create: CartItemCreate) -> CartItem:
    cart_item = CartItem(cart_id = cart_item_create.cart_id, product_id = cart_item_create.product_id)
    return CartGateway.add_item_to_cart(cart_id, cart_item)
  
@router.delete("/{cart_id}/items/{cart_item_id}")
def delete_cart_item(cart_id: UUID, cart_item_id: UUID) -> CartItem:
    return CartGateway.delete_cart_item(cart_item_id)

@router.patch("/{cart_id}/items/{cart_item_id}")
async def patch_cart_item(cart_id: UUID, cart_item_id: UUID, request: Request ) -> CartItem:
    data = await request.json()
    return CartGateway.patch_cart_item(cart_item_id, CartItemPatch(**data))