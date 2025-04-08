from sqlmodel import select
from models.product import Product 
from schemas.product import ProductPatch
from database import get_session
from exceptions.exceptions import (ProductNameAlreadyExistsException, ProductNotFoundException)

class ProductRepository:
    
    @staticmethod
    def create_product(product: Product) -> Product:
        with get_session() as session:
            query = select(Product).where(Product.name == product.name)
            existing_product = session.exec(query).first()
            #Validar que el nombre no este en la base de datos
            if existing_product:
                raise ProductNameAlreadyExistsException(product.name)
            # Agregar el nuevo producto
            session.add(product)
            session.commit()
            session.refresh(product)
            return product
    
    @staticmethod
    def get_products_hombre() -> list[Product]:
        with get_session() as session:
            query = select(Product).where(Product.category == "Hombre")
            all_products  = session.exec(query).all()
            return all_products 
        
    @staticmethod
    def get_products_mujer() -> list[Product]:
        with get_session() as session:
            query = select(Product).where(Product.category == "Mujer")
            all_products  = session.exec(query).all()
            return all_products 
        
    @staticmethod
    def search_products_men(search: str) -> list[Product]:
          with get_session() as session:  
            query = select(Product).filter(Product.category == "Hombre")
            if search and search.strip():
                query = query.filter(Product.name.ilike(f"%{search}%"))
            #Como exec, peero sin metadatos?
            result = session.scalars(query).all()
            return result
        
    @staticmethod
    def search_products_women(search: str) -> list[Product]:
        with get_session() as session:  
            query = select(Product).filter(Product.category == "Mujer")
            if search and search.strip():
                query = query.filter(Product.name.ilike(f"%{search}%"))
            #Como exec, peero sin metadatos?
            result = session.scalars(query).all()
            return result
            
    @staticmethod
    def get_product(product_id: int) -> Product:
        with get_session() as session:
            product = session.get(Product, product_id)
            if product:
                return product
            #Validar que exista el producto
            raise ProductNotFoundException(product_id)
        
    @staticmethod
    def delete_product(product_id: int) -> Product:
        with get_session() as session:
            product = session.get(Product, product_id)
            #Validar que exista el producto
            if product is None:
                raise ProductNotFoundException(product_id)
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
                raise ProductNotFoundException(product.id)
            # Verificar si el nombre del producto ya existe
            existing_product = session.exec(select(Product).where(Product.name == product.name)).first()
            if existing_product and existing_product.id != product.id:  # Verificar si el nombre pertenece a otro producto
                raise ProductNameAlreadyExistsException(product.name)
            # Actualizar los campos del usuario
            product_to_update.name = product.name
            product_to_update.price = product.price
            product_to_update.category = product.category
            product_to_update.image = product.image
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
                raise ProductNotFoundException(product_id)
            #Validar que en la solicitud vaya el campo name, es decir que no sea None
            if product_patch.name:
                # Verificar si el nombre del producto ya existe
                existing_product = session.exec(select(Product).where(Product.name == product_patch.name)).first()
                if existing_product and existing_product.id != product_id:  # Verificar si el nombre pertenece a otro producto
                    raise ProductNameAlreadyExistsException(product_patch.name)
            # Actualizar solo los campos proporcionados en user_patch
            #Cuando usas or en python aqui indica que si hay 2 true se queda con el primero
            product_to_update.name = product_patch.name or product_to_update.name
            product_to_update.price = product_patch.price or product_to_update.price
            product_to_update.category = product_patch.category or product_to_update.category
            session.commit()
            session.refresh(product_to_update)
            return product_to_update  
                
    @staticmethod
    def patch_product_image(product_id: int, image_url: str) -> Product:
        with get_session() as session:
            product_to_update = session.get(Product, product_id)
            if product_to_update is None:
                raise ProductNotFoundException(product_id)
            product_to_update.image = image_url or product_to_update.image
            session.commit()
            session.refresh(product_to_update)
            return product_to_update