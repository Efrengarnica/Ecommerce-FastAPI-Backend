from sqlmodel import select
from app.models.product import Product 
from app.schemas.product import ProductPatch
from fastapi import HTTPException
from app.database import get_session

class ProductRepository:
    
    @staticmethod
    def create_product(product: Product) -> Product:
        with get_session() as session:
            query = select(Product).where(Product.name == product.name)
            existing_product = session.exec(query).first()
            #Validar que el nombre no este en la base de datos
            if existing_product:
                raise HTTPException(status_code = 400, detail = "Product name already registered")
            # Agregar el nuevo producto
            session.add(product)
            session.commit()
            session.refresh(product)
            return product
    
    @staticmethod
    def get_products() -> list[Product]:
        with get_session() as session:
            query = select(Product)
            all_users = session.exec(query).all()
            return all_users
        
    @staticmethod
    def get_product(product_id: int) -> Product:
        with get_session() as session:
            product = session.get(Product, product_id)
            if product:
                return product
            #Validar que exista el producto
            raise HTTPException(status_code = 404, detail = "Product not found")
        
    @staticmethod
    def delete_product(product_id: int) -> Product:
        with get_session() as session:
            product = session.get(Product, product_id)
            #Validar que exista el producto
            if product is None:
                raise HTTPException(status_code = 404, detail = "Product not found")
            session.delete(product)
            session.commit()
            return product
    
    @staticmethod
    def update_product(product: Product) -> Product:
        with get_session() as session:
            # Buscar el usuario por ID en la base de datos
            product_to_update = session.get(Product, product.id)
            #Validar que exita el producto
            if product_to_update is None:
                raise HTTPException(status_code = 404, detail = "Product not found")
            # Verificar si el nombre del producto ya existe
            existing_product = session.exec(select(Product).where(Product.name == product.name)).first()
            if existing_product and existing_product.id != product.id:  # Verificar si el nombre pertenece a otro producto
                raise HTTPException(status_code = 400, detail = "Product name already exists")
            # Actualizar los campos del usuario
            product_to_update.name = product.name
            product_to_update.price = product.price
            product_to_update.category = product.category
            # Confirmar la actualización en la base de datos
            session.commit()
            # Refrescar el usuario para obtener los datos actualizados
            session.refresh(product_to_update)
            return product_to_update  # Retornar el producto actualizado
        
    @staticmethod
    def patch_product(product_id: int, product_patch: ProductPatch) -> Product:
        with get_session() as session:
            product_to_update = session.get(Product, product_id)
            #Validar que exita el producto
            if product_to_update is None:
                raise HTTPException(status_code = 404, detail = "Product not found")
            #Validar que en la solicitud vaya el campo name, es decir que no sea None
            if product_patch.name:
                # Verificar si el nombre del producto ya existe
                existing_product = session.exec(select(Product).where(Product.name == product_patch.name)).first()
                if existing_product and existing_product.id != product_id:  # Verificar si el nombre pertenece a otro producto
                    raise HTTPException(status_code = 400, detail = "Product name already exists")
            # Actualizar solo los campos proporcionados en user_patch
            #Cuando usas or en python aqui indica que si hay 2 true se queda con el primero
            product_to_update.name = product_patch.name or product_to_update.name
            product_to_update.price = product_patch.price or product_to_update.price
            product_to_update.category = product_patch.category or product_to_update.category
            session.commit()
            session.refresh(product_to_update)
            return product_to_update  