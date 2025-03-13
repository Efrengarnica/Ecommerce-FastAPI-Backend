from sqlmodel import Session, select
from uuid import UUID
from fastapi import HTTPException
from app.models.cart import Cart, CartItem, CartItemPatch
from app.models.user import User
from app.models.product import Product
from sqlalchemy.orm import selectinload

#Los repository son los que se conectan mediante una session a la base de datos SQLITE, DEJA RECUERDO DE DONDE VIENE SQLLITE
#En este repository esta el de Cart y CartItem, los hice aqui mismo, solo tener cuidado de no usar los mismos nombres en las funciones
#ya que estan en la misma clase, ademas cuidar las rutas que se ocupan, para CartItem use otras.
class CartRepository:
    
    #Repository de Cart
    @staticmethod
    def create_cart(cart: Cart, session: Session) -> Cart:
        # Validar si el cart ya está registrado
        existing_cart = session.get(Cart, cart.id)
        if existing_cart:
            raise HTTPException(status_code = 400, detail = "Cart already registered")
         # Validar que el usuario exista
        existing_user = session.get(User, cart.user_id)
        if not existing_user:
            raise HTTPException(status_code = 404, detail = "User not found")
        #Agregar a la base de datos y guardar los cambios
        #Algo interesante es que cuando hacer .add(cart) FastAPI sabe que como cart es una instancia de Cart entonces lo agrega a esa entidad
        session.add(cart)
        session.commit()
        return cart

    @staticmethod
    def get_carts(session: Session) -> list[Cart]:
        return session.exec(select(Cart)).all()
    
    @staticmethod
    def get_cart(cart_id: UUID, session: Session) -> Cart:
        #Este es el otro apartado que hay que agregar para que se muestren los Items en el carrito, al parecer como solo existe
        #una relacion "items" y no es un atributo entonces FastAPI no se siente en la necesidad de cargar las relaciones
        #entonces haces esto para que las cargue, al parecer debe de estar una sessionactiva para que funcione
        #Recuerda que tambien tienes que agregar cosas en el Model y en el Controller
        stmt = select(Cart).options(selectinload(Cart.items)).where(Cart.id == cart_id)
        cart = session.exec(stmt).one_or_none()
        #Verifica que exista el carrito en la base de datos
        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")
        return cart
    
    @staticmethod
    def delete_cart(cart_id: UUID, session: Session) -> Cart:
        cart = session.get(Cart, cart_id)
        if not cart:
            raise HTTPException(status_code = 404, detail = "Cart not found")
        session.delete(cart)
        session.commit()
        return cart
    #A mi entendimiento parece ser que el put y el patch no seran necesarios ya que no me interesa cambiar nada del carrito en si.


    # Repository de CartItem (producto dentro del carrito)
    @staticmethod
    def add_item_to_cart(cart_id: UUID, cart_item: CartItem, session: Session) -> CartItem:
        existing_cart_item = session.get(CartItem, cart_item.id)
        #Validar si el cartItem existe en la base de datos
        if existing_cart_item:
            raise HTTPException(status_code = 400, detail = "CartItem already registered")
        # Validar que el carrito exista
        existing_cart = session.get(Cart, cart_item.cart_id)
        if not existing_cart:
            raise HTTPException(status_code = 404, detail = "Cart not found")
        # Validar que el producto exista
        existing_product = session.get(Product, cart_item.product_id)
        if not existing_product:
            raise HTTPException(status_code = 404, detail = "Product not found")
        session.add(cart_item)
        session.commit()
        return cart_item
    
    @staticmethod
    def delete_cart_item(cart_item_id: UUID, session: Session) -> CartItem:
        item_cart = session.get(CartItem, cart_item_id)
        if not item_cart:
            raise HTTPException(status_code = 404, detail = "Cart item not found")
        session.delete(item_cart)
        session.commit()
        return item_cart
    
    @staticmethod
    def patch_cart_item(cart_item_id: UUID, cart_item_patch: CartItemPatch, session: Session) -> CartItem:
        cart_item_to_update = session.get(CartItem, cart_item_id)
        #Validar que el CartItem exista
        if cart_item_to_update is None:
            raise HTTPException(status_code = 404, detail = "CartItem not found")
        cart_item_to_update.quantity = cart_item_patch.quantity
        session.commit()
        session.refresh(cart_item_to_update)
        return cart_item_to_update