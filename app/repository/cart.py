from sqlmodel import select
from uuid import UUID
from fastapi import HTTPException
from app.models.cart import Cart, CartItem
from app.schemas.cart import CartItemPatch
from app.models.user import User
from app.models.product import Product
from sqlalchemy.orm import selectinload
from app.database import get_session

#Los repository son los que se conectan mediante una session a la base de datos SQLITE, DEJA RECUERDO DE DONDE VIENE SQLLITE
#En este repository esta el de Cart y CartItem, los hice aqui mismo, solo tener cuidado de no usar los mismos nombres en las funciones
#ya que estan en la misma clase, ademas cuidar las rutas que se ocupan, para CartItem use otras.
class CartRepository:
    
    #Repository de Cart
    @staticmethod
    def create_cart(cart: Cart) -> Cart:
        with get_session() as session:
            # Validar si el cart ya está registrado
            existing_cart = session.get(Cart, cart.id)
            if existing_cart:
                raise HTTPException(status_code = 400, detail = "Cart already registered")
            # Validar que el usuario exista
            existing_user = session.get(User, cart.user_id)
            if not existing_user:
                raise HTTPException(status_code = 404, detail = "User not found")
            session.add(cart)
            session.commit()
            session.refresh(cart)
            # Cargar la relación 'items' mediante eager loading después del commit
            stmt = select(Cart).options(selectinload(Cart.items)).where(Cart.id == cart.id)
            cart_all = session.exec(stmt).one_or_none()
            return cart_all

    @staticmethod
    def get_carts() -> list[Cart]:
        with get_session() as session:
            stmt = select(Cart).options(selectinload(Cart.items))
            carts = session.exec(stmt).all()
            return carts
    
    @staticmethod
    def get_cart(cart_id: UUID) -> Cart:
        with get_session() as session:
            existing_cart = session.get(Cart, cart_id)
            #Este es el otro apartado que hay que agregar para que se muestren los Items en el carrito, al parecer como solo existe
            #una relacion "items" y no es un atributo entonces FastAPI no se siente en la necesidad de cargar las relaciones
            #entonces haces esto para que las cargue, al parecer debe de estar una sessionactiva para que funcione
            #Recuerda que tambien tienes que agregar cosas en el Model y en el Controller
            #option le dice que no sera una consukta ordinaria
            #selectinload le dice que si encuentra la relacion Cart.items la traiga junto con la consulta
            # CUANDO HACES UNA CONSULTA Y ESTA PRESENTA RELACIONES LAS RELCIONES NO VIENEN EN LA CONSULTA POR DEFECTO 
            # DEBES DE DECIRLE QUE LAS TRAIGA DE MANERA EXPLICITA.
            
            #Verifica que exista el carrito en la base de datos
            if not existing_cart:
                raise HTTPException(status_code=404, detail="Cart not found")
            stmt = select(Cart).options(selectinload(Cart.items)).where(Cart.id == cart_id)
            cart = session.exec(stmt).one_or_none()
            return cart
    
    @staticmethod
    def delete_cart(cart_id: UUID) -> Cart:
        with get_session() as session:
            existing_cart = session.get(Cart, cart_id)
            if not existing_cart:
                raise HTTPException(status_code = 404, detail = "Cart not found")
            stmt = select(Cart).options(selectinload(Cart.items)).where(Cart.id == cart_id)
            cart = session.exec(stmt).one_or_none()
            session.delete(existing_cart)
            session.commit()
            return cart
        #A mi entendimiento parece ser que el put y el patch no seran necesarios ya que no me interesa cambiar nada del carrito en si.

    # Repository de CartItem (producto dentro del carrito)
    @staticmethod
    def add_item_to_cart(cart_item: CartItem) -> CartItem:
        with get_session() as session:
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
            session.refresh(cart_item)
            return cart_item
    
    @staticmethod
    def delete_cart_item(cart_item_id: UUID) -> CartItem:
        with get_session() as session:
            item_cart = session.get(CartItem, cart_item_id)
            if not item_cart:
                raise HTTPException(status_code = 404, detail = "Cart item not found")
            session.delete(item_cart)
            session.commit()
            return item_cart
    
    @staticmethod
    def patch_cart_item(cart_item_id: UUID, cart_item_patch: CartItemPatch) -> CartItem:
        with get_session() as session:
            cart_item_to_update = session.get(CartItem, cart_item_id)
            #Validar que el CartItem exista
            if cart_item_to_update is None:
                raise HTTPException(status_code = 404, detail = "CartItem not found")
            cart_item_to_update.quantity = cart_item_patch.quantity
            session.commit()
            session.refresh(cart_item_to_update)
            return cart_item_to_update