from sqlite3 import IntegrityError
from uuid import UUID
from models.cart import Cart, CartItem
from schemas.cart import CartCreate, CartItemPatch
from repository.cart import CartRepository
from exceptions.exceptions import (DatabaseIntegrityException, InternalServerErrorException)

class CartGateway:
    
    @classmethod
    def create_cart(cls, cart_create: CartCreate) -> Cart:
        try:
            return CartRepository.create_cart(cart_create)
        except IntegrityError as e:
            raise DatabaseIntegrityException(str(e))

    @classmethod
    def get_carts(cls) -> list[Cart]:
        try:
            return CartRepository.get_carts()
        except Exception as e:
            raise InternalServerErrorException(str(e))
    
    @classmethod
    def get_cart(cls, user_id: UUID) -> Cart:
        return CartRepository.get_cart(user_id)
     
    @classmethod
    def delete_cart(cls, cart_id: UUID) -> Cart:
        return CartRepository.delete_cart(cart_id)
    
    @classmethod
    def clear_cart_items(cls, cart_id: UUID) -> Cart:
        return CartRepository.clear_cart_items(cart_id)
     
    
    # Métodos para los items del carrito (CartItem)
    @classmethod
    def add_item_to_cart(cls, cart_item: CartItem) -> CartItem:
        try:
            return CartRepository.add_item_to_cart(cart_item)
        except IntegrityError as e:
            raise DatabaseIntegrityException(str(e))
        
    @classmethod
    def delete_cart_item(cls, cart_item_id: UUID) -> CartItem:
        return CartRepository.delete_cart_item(cart_item_id)

    @classmethod
    def patch_cart_item(cls, cart_item_id: UUID, cart_item_patch: CartItemPatch) -> CartItem:
        try: 
            return CartRepository.patch_cart_item(cart_item_id, cart_item_patch) 
        except IntegrityError as e:
            raise DatabaseIntegrityException(str(e))