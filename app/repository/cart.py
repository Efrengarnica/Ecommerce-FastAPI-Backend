from sqlmodel import select
from uuid import UUID
from app.models.cart import Cart, CartItem
from app.schemas.cart import CartItemPatch
from app.models.user import User
from app.models.product import Product
from sqlalchemy.orm import selectinload
from app.database import get_session
from app.exceptions.exceptions import (CartAlreadyRegisteredException, CartItemAlreadyRegisteredException, CartItemNotFoundException, CartNotFoundException, ProductNotFoundException, UserNotFoundException)
from app.schemas.product import ProductResponse

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
                raise CartAlreadyRegisteredException(cart.id)
            # Validar que el usuario exista
            existing_user = session.get(User, cart.user_id)
            if not existing_user:
                raise UserNotFoundException(cart.user_id)
            session.add(cart)
            session.commit()
            session.refresh(cart)
            # Cargar la relación 'items' y la relación 'product' de cada item de forma ansiosa
            stmt = select(Cart).options(
                selectinload(Cart.items).selectinload(CartItem.product)
            ).where(Cart.id == cart.id)
            cart_all = session.exec(stmt).one_or_none()
            return cart_all

    @staticmethod
    def get_carts() -> list[Cart]:
        with get_session() as session:
            stmt = select(Cart).options(selectinload(Cart.items).selectinload(CartItem.product))
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
                raise CartNotFoundException(cart_id)
            stmt = select(Cart).options(selectinload(Cart.items).selectinload(CartItem.product)).where(Cart.id == cart_id)
            cart = session.exec(stmt).one_or_none()
            return cart
    
    @staticmethod
    def delete_cart(cart_id: UUID) -> Cart:
        with get_session() as session:
            existing_cart = session.get(Cart, cart_id)
            if not existing_cart:
                raise CartNotFoundException(cart_id)
            stmt = select(Cart).options(selectinload(Cart.items).selectinload(CartItem.product)).where(Cart.id == cart_id)
            cart = session.exec(stmt).one_or_none()
            session.delete(existing_cart)
            session.commit()
            return cart
        #A mi entendimiento parece ser que el put y el patch no seran necesarios ya que no me interesa cambiar nada del carrito en si.
        
    @staticmethod
    def clear_cart_items(cart_id: UUID) -> Cart:
        with get_session() as session:
            cart = session.exec(
                select(Cart)
                .options(selectinload(Cart.items).selectinload(CartItem.product))
                .where(Cart.id == cart_id)
                ).first()
            if not cart:
                raise CartNotFoundException(cart_id)
            # Eliminamos todos los items del carrito
            for item in cart.items:
                session.delete(item)
            session.commit()
            # Reconsultamos el carrito para obtener el estado actualizado
            updated_cart = session.exec(
                select(Cart)
                .options(selectinload(Cart.items).selectinload(CartItem.product))
                .where(Cart.id == cart_id)
            ).first()
            return updated_cart


    # Repository de CartItem (producto dentro del carrito)
    @staticmethod
    def add_item_to_cart(cart_item: CartItem) -> CartItem:
        with get_session() as session:
            existing_cart_item = session.get(CartItem, cart_item.id)
            #Validar si el cartItem existe en la base de datos
            if existing_cart_item:
                raise CartItemAlreadyRegisteredException(cart_item.id)
            # Validar que el carrito exista
            existing_cart = session.get(Cart, cart_item.cart_id)
            if not existing_cart:
                raise CartNotFoundException(cart_item.cart_id)
            # Validar que el producto exista
            existing_product = session.get(Product, cart_item.product_id)
            if not existing_product:
                raise ProductNotFoundException(cart_item.product_id)
            session.add(cart_item)
            session.commit()
            session.refresh(cart_item)
             # En lugar de usar session.refresh, hacemos una consulta que cargue la relación 'product'
            stmt = select(CartItem).options(selectinload(CartItem.product)).where(CartItem.id == cart_item.id)
            full_cart_item = session.exec(stmt).one_or_none()
            return full_cart_item
    
    @staticmethod
    def delete_cart_item(cart_item_id: UUID) -> CartItem:
        with get_session() as session:
            stmt = select(CartItem).options(selectinload(CartItem.product)).where(CartItem.id == cart_item_id)
            full_cart_item = session.exec(stmt).one_or_none()
            if not full_cart_item:
                raise CartItemNotFoundException(cart_item_id)
            session.delete(full_cart_item)
            session.commit()
            # Construye un diccionario con los datos necesarios
            response_data = {
                "id": full_cart_item.id,
                "cart_id": full_cart_item.cart_id,
                "product_id": full_cart_item.product_id,
                "quantity": full_cart_item.quantity,
                "product": ProductResponse.model_validate(full_cart_item.product) if full_cart_item.product else None
            }
            return CartItem(**response_data)
    
    @staticmethod
    def patch_cart_item(cart_item_id: UUID, cart_item_patch: CartItemPatch) -> CartItem:
        with get_session() as session:
            cart_item_to_update = session.get(CartItem, cart_item_id)
            #Validar que el CartItem exista
            if cart_item_to_update is None:
                raise CartItemNotFoundException(cart_item_id)
            cart_item_to_update.quantity = cart_item_patch.quantity
            session.commit()
            session.refresh(cart_item_to_update)
            stmt = select(CartItem).options(selectinload(CartItem.product)).where(CartItem.id == cart_item_id)
            full_cart_item = session.exec(stmt).one_or_none()
            return full_cart_item