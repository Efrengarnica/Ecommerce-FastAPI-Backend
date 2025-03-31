from sqlite3 import IntegrityError
from fastapi import HTTPException
from app.models.product import Product
from app.schemas.product import ProductPatch
from app.repository.product import ProductRepository
from app.exceptions.exceptions import (DatabaseIntegrityException, InternalServerErrorException)

class ProductGateway:
    
    @classmethod
    def create_product(cls, product: Product) -> Product:
        try:
            return ProductRepository.create_product(product)
        except IntegrityError as e:
            raise DatabaseIntegrityException(str(e))
    
    @classmethod
    def get_products(cls) -> list[Product]:
        try:
            return ProductRepository.get_products()
        except Exception as e:
            raise InternalServerErrorException(str(e))
    
    @classmethod
    def get_product(cls, product_id: int) -> Product:
        return ProductRepository.get_product(product_id)
      
    @classmethod
    def delete_product(cls, product_id: int) -> Product:
        return ProductRepository.delete_product(product_id)
       
    @classmethod
    def update_product(cls, product: Product) -> Product:
        try:
            return ProductRepository.update_product(product)
        except IntegrityError as e:
            raise DatabaseIntegrityException(str(e))
    
    @classmethod
    def patch_product(cls, product_id: int, product_patch: ProductPatch) -> Product:
        try:
            return ProductRepository.patch_product(product_id, product_patch)
        except IntegrityError as e:
            raise DatabaseIntegrityException(str(e))