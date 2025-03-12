from uuid import UUID
from sqlmodel import Session
from fastapi import HTTPException
from app.models.cart import Cart, CartItem, CartItemPatch
from app.repository.cart import CartRepository

class CartGateway:
    @classmethod
    def create_cart(cls, cart: Cart, session: Session) -> Cart:
        return CartRepository.create_cart(cart, session)

    @classmethod
    def get_carts(cls, session: Session) -> list[Cart]:
        return CartRepository.get_carts(session)
    
    @classmethod
    def get_cart(cls, cart_id: UUID, session: Session) -> Cart:
        return CartRepository.get_cart(cart_id, session)
    
    @classmethod
    def delete_cart(cls, cart_id: UUID, session: Session) -> Cart:
        return CartRepository.delete_cart(cart_id, session)
    
    # Métodos para los items del carrito (CartItem)
    @classmethod
    def add_item_to_cart(cls, cart_id: UUID, cart_item: CartItem, session: Session) -> CartItem:
        if cart_id != cart_item.cart_id:
            raise HTTPException(status_code=400, detail="Cart ID does not match")
        return CartRepository.add_item_to_cart(cart_id, cart_item, session)
       

    @classmethod
    def delete_cart_item(cls, cart_item_id: UUID, session: Session) -> CartItem:
        return CartRepository.delete_cart_item(cart_item_id, session)

    @classmethod
    def patch_cart_item(cls, cart_item_id: UUID, cart_item_patch:CartItemPatch, session: Session) -> CartItem:
        return CartRepository.patch_cart_item(cart_item_id, cart_item_patch, session) 