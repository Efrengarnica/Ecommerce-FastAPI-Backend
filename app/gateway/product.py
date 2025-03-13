from fastapi import HTTPException
from app.models.product import Product, ProductPatch
from sqlmodel import Session
from app.repository.product import ProductRepository

class ProductGateway:
    
    @classmethod
    def create_product(cls, product: Product, session: Session) -> Product:
        return ProductRepository.create_product(product, session)

    @classmethod
    def get_products(cls, session: Session) -> list[Product]:
        return ProductRepository.get_products(session)
    
    @classmethod
    def get_product(cls, product_id: int, session: Session) -> Product:
        return ProductRepository.get_product(product_id, session)
    
    @classmethod
    def delete_product(cls, product_id: int, session: Session) -> Product:
        return ProductRepository.delete_product(product_id, session)

    @classmethod
    def update_product(cls, product_id: int, product: Product, session: Session) -> Product:
        if product_id != product.id:
            raise HTTPException(status_code = 400, detail = "Product ID does not match")
        return ProductRepository.update_product(product_id, product, session)
    
    @classmethod
    def patch_product(cls, product_id: int, product_patch: ProductPatch, session: Session) -> Product:
        return ProductRepository.patch_product(product_id, product_patch, session)