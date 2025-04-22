from sqlmodel import select
from models.product import Product 
from schemas.product import ProductPatch
from database import get_session
from exceptions.exceptions import (ProductNameAlreadyExistsException, ProductNotFoundException)

class ProductRepository:
    
    @staticmethod
    async def create_product(product: Product) -> Product:
        async with get_session() as session:
            # 1. Validar unicidad de nombre
            stmt = select(Product).where(Product.name == product.name)
            result = await session.execute(stmt)
            existing = result.scalars().first()
            if existing:
                raise ProductNameAlreadyExistsException(product.name)

            # 2. Insertar
            session.add(product)
            await session.commit()
            await session.refresh(product)
            return product
    
    @staticmethod
    async def get_products_hombre() -> list[Product]:
        async with get_session() as session:
            stmt = select(Product).where(Product.category == "Hombre")
            result = await session.execute(stmt)
            return result.scalars().all()

    @staticmethod
    async def get_products_mujer() -> list[Product]:
        async with get_session() as session:
            stmt = select(Product).where(Product.category == "Mujer")
            result = await session.execute(stmt)
            return result.scalars().all()
    
    @staticmethod
    async def search_products_men(search: str) -> list[Product]:
        async with get_session() as session:
            stmt = select(Product).where(Product.category == "Hombre")
            if search and search.strip():
                stmt = stmt.where(Product.name.ilike(f"%{search}%"))
            result = await session.execute(stmt)
            return result.scalars().all()
        
    @staticmethod
    async def search_products_women(search: str) -> list[Product]:
        async with get_session() as session:
            stmt = select(Product).where(Product.category == "Mujer")
            if search and search.strip():
                stmt = stmt.where(Product.name.ilike(f"%{search}%"))
            result = await session.execute(stmt)
            return result.scalars().all()
        
    @staticmethod
    async def get_product(product_id: int) -> Product:
        async with get_session() as session:
            product = await session.get(Product, product_id)
            if not product:
                raise ProductNotFoundException(product_id)
            return product
        
    @staticmethod
    async def delete_product(product_id: int) -> Product:
        async with get_session() as session:
            product = await session.get(Product, product_id)
            if not product:
                raise ProductNotFoundException(product_id)
            await session.delete(product)
            await session.commit()
            return product
    
    @staticmethod
    async def update_product(product: Product) -> Product:
        async with get_session() as session:
            existing = await session.get(Product, product.id)
            if not existing:
                raise ProductNotFoundException(product.id)

            # Validar nombre duplicado
            stmt = select(Product).where(Product.name == product.name)
            result = await session.execute(stmt)
            conflict = result.scalars().first()
            if conflict and conflict.id != product.id:
                raise ProductNameAlreadyExistsException(product.name)

            # Sobrescribir campos
            existing.name = product.name
            existing.price = product.price
            existing.category = product.category
            existing.image = product.image

            await session.commit()
            await session.refresh(existing)
            return existing
        
    @staticmethod
    async def patch_product(product_id: int, product_patch: ProductPatch) -> Product:
        async with get_session() as session:
            existing = await session.get(Product, product_id)
            if not existing:
                raise ProductNotFoundException(product_id)

            # Si cambian el nombre, validar unicidad
            if product_patch.name is not None:
                stmt = select(Product).where(Product.name == product_patch.name)
                result = await session.execute(stmt)
                conflict = result.scalars().first()
                if conflict and conflict.id != product_id:
                    raise ProductNameAlreadyExistsException(product_patch.name)

            # Actualizar solo campos no-None
            if product_patch.name is not None:
                existing.name = product_patch.name
            if product_patch.price is not None:
                existing.price = product_patch.price
            if product_patch.category is not None:
                existing.category = product_patch.category

            await session.commit()
            await session.refresh(existing)
            return existing
        
    @staticmethod
    async def patch_product_image(product_id: int, image_url: str) -> Product:
        async with get_session() as session:
            existing = await session.get(Product, product_id)
            if not existing:
                raise ProductNotFoundException(product_id)

            existing.image = image_url or existing.image
            await session.commit()
            await session.refresh(existing)
            return existing