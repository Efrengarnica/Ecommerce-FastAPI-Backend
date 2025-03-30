from uuid import UUID
from fastapi import HTTPException
from app.models.cart import Cart, CartItem, CartItemPatch
from app.repository.cart import CartRepository

class CartGateway:
    
    @classmethod
    def create_cart(cls, cart: Cart) -> Cart:
        return CartRepository.create_cart(cart)

    @classmethod
    def get_carts(cls) -> list[Cart]:
        return CartRepository.get_carts()
    
    @classmethod
    def get_cart(cls, cart_id: UUID) -> Cart:
        return CartRepository.get_cart(cart_id)
    
    @classmethod
    def delete_cart(cls, cart_id: UUID) -> Cart:
        return CartRepository.delete_cart(cart_id)
    
    # Métodos para los items del carrito (CartItem)
    @classmethod
    def add_item_to_cart(cls, cart_id: UUID, cart_item: CartItem) -> CartItem:
        if cart_id != cart_item.cart_id:
            raise HTTPException(status_code=400, detail="Cart ID does not match")
        return CartRepository.add_item_to_cart(cart_id, cart_item)
       
    @classmethod
    def delete_cart_item(cls, cart_item_id: UUID) -> CartItem:
        return CartRepository.delete_cart_item(cart_item_id)

    @classmethod
    def patch_cart_item(cls, cart_item_id: UUID, cart_item_patch: CartItemPatch) -> CartItem:
        return CartRepository.patch_cart_item(cart_item_id, cart_item_patch) 