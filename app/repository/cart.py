from fastapi.responses import JSONResponse
from sqlmodel import select
from uuid import UUID
from models.cart import Cart, CartItem
from schemas.cart import CartCreate, CartItemPatch
from models.user import User
from models.product import Product
from sqlalchemy.orm import selectinload
from database import get_session
from exceptions.exceptions import (CartAlreadyRegisteredException, CartItemAlreadyRegisteredException, CartItemNotFoundException, CartNotFoundException, ProductNotFoundException, UserNotFoundException)
from schemas.product import ProductResponse

#Los repository son los que se conectan mediante una session a la base de datos SQLITE, DEJA RECUERDO DE DONDE VIENE SQLLITE
#En este repository esta el de Cart y CartItem, los hice aqui mismo, solo tener cuidado de no usar los mismos nombres en las funciones
#ya que estan en la misma clase, ademas cuidar las rutas que se ocupan, para CartItem use otras.
class CartRepository:
    
    # Repository Cart
    @staticmethod
    async def create_cart(cart_create: CartCreate) -> Cart:
        async with get_session() as session:
            # Verificar existencia de usuario
            user = await session.get(User, cart_create.user_id)
            if not user:
                raise UserNotFoundException(cart_create.user_id)

            # Verificar que el usuario no tenga ya un carrito
            stmt = select(Cart).where(Cart.user_id == cart_create.user_id)
            result = await session.execute(stmt)
            existing_cart = result.scalars().first()
            if existing_cart:
                raise CartAlreadyRegisteredException(existing_cart.id, cart_create.user_id)

            # Crear y persistir nuevo carrito
            new_cart = Cart(user_id=cart_create.user_id)
            session.add(new_cart)
            await session.commit()
            await session.refresh(new_cart)

            # Cargar relaciones items -> product
            stmt = (
                select(Cart)
                .options(
                    selectinload(Cart.items).selectinload(CartItem.product)
                )
                .where(Cart.id == new_cart.id)
            )
            result = await session.execute(stmt)
            cart_all = result.scalars().first()
            return cart_all

    @staticmethod
    async def get_carts() -> list[Cart]:
        async with get_session() as session:
            stmt = (
                select(Cart)
                .options(
                    selectinload(Cart.items).selectinload(CartItem.product)
                )
            )
            result = await session.execute(stmt)
            return result.scalars().all()
        
    @staticmethod
    async def get_cart(user_id: UUID) -> Cart:
        async with get_session() as session:
            stmt = (
                select(Cart)
                .options(
                    selectinload(Cart.items).selectinload(CartItem.product)
                )
                .where(Cart.user_id == user_id)
            )
            result = await session.execute(stmt)
            cart = result.scalars().first()
            if not cart:
                return JSONResponse(status_code=404, content={"detail": f"No exite carrito con el id_user: {user_id}"})

            # Ordenar items por fecha de creación
            cart.items.sort(key=lambda item: item.created_at)
            return cart

    @staticmethod
    async def delete_cart(cart_id: UUID) -> Cart:
        async with get_session() as session:
            cart = await session.get(Cart, cart_id)
            if not cart:
                raise CartNotFoundException(cart_id)

            # Cargar antes de eliminar para devolver al caller
            stmt = (
                select(Cart)
                .options(
                    selectinload(Cart.items).selectinload(CartItem.product)
                )
                .where(Cart.id == cart_id)
            )
            result = await session.execute(stmt)
            full_cart = result.scalars().first()

            await session.delete(cart)
            await session.commit()
            return full_cart
        #A mi entendimiento parece ser que el put y el patch no seran necesarios ya que no me interesa cambiar nada del carrito en si.
        
    @staticmethod
    async def clear_cart_items(cart_id: UUID) -> Cart:
        async with get_session() as session:
            stmt = (
                select(Cart)
                .options(
                    selectinload(Cart.items).selectinload(CartItem.product)
                )
                .where(Cart.id == cart_id)
            )
            result = await session.execute(stmt)
            cart = result.scalars().first()
            if not cart:
                raise CartNotFoundException(cart_id)

            # Eliminar todos los items
            for item in cart.items:
                await session.delete(item)
            await session.commit()

            # Reconsultar carrito actualizado
            result = await session.execute(stmt)
            updated_cart = result.scalars().first()
            return updated_cart


    # --- CartItem repository ---
    @staticmethod
    async def add_item_to_cart(cart_item: CartItem) -> CartItem:
        async with get_session() as session:
            # Validar que no exista ya este cart_item
            existing = await session.get(CartItem, cart_item.id)
            if existing:
                raise CartItemAlreadyRegisteredException(cart_item.id)

            # Validar existencia de carrito y producto
            cart = await session.get(Cart, cart_item.cart_id)
            if not cart:
                raise CartNotFoundException(cart_item.cart_id)
            product = await session.get(Product, cart_item.product_id)
            if not product:
                raise ProductNotFoundException(cart_item.product_id)

            session.add(cart_item)
            await session.commit()
            await session.refresh(cart_item)

            # Cargar relación product
            stmt = (
                select(CartItem)
                .options(selectinload(CartItem.product))
                .where(CartItem.id == cart_item.id)
            )
            result = await session.execute(stmt)
            return result.scalars().first()
    
    @staticmethod   
    async def delete_cart_item(cart_item_id: UUID) -> CartItem:
        async with get_session() as session:
            stmt = (
                select(CartItem)
                .options(selectinload(CartItem.product))
                .where(CartItem.id == cart_item_id)
            )
            result = await session.execute(stmt)
            full_item = result.scalars().first()
            if not full_item:
                raise CartItemNotFoundException(cart_item_id)

            # Guardar datos de respuesta
            response_data = {
                "id": full_item.id,
                "cart_id": full_item.cart_id,
                "product_id": full_item.product_id,
                "quantity": full_item.quantity,
                "product": ProductResponse.model_validate(full_item.product) if full_item.product else None,
            }

            await session.delete(full_item)
            await session.commit()
            return CartItem(**response_data)
    
    @staticmethod
    async def patch_cart_item(cart_item_id: UUID, cart_item_patch: CartItemPatch) -> CartItem:
        async with get_session() as session:
            cart_item = await session.get(CartItem, cart_item_id)
            if not cart_item:
                raise CartItemNotFoundException(cart_item_id)

            # Actualizar cantidad
            cart_item.quantity = cart_item_patch.quantity
            await session.commit()
            await session.refresh(cart_item)

            # Recargar relación product
            stmt = (
                select(CartItem)
                .options(selectinload(CartItem.product))
                .where(CartItem.id == cart_item_id)
            )
            result = await session.execute(stmt)
            return result.scalars().first()