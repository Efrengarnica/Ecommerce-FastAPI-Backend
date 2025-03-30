from fastapi import HTTPException
from app.models.product import Product, ProductPatch
from app.repository.product import ProductRepository

class ProductGateway:
    
    @classmethod
    def create_product(cls, product: Product) -> Product:
        return ProductRepository.create_product(product)

    @classmethod
    def get_products(cls) -> list[Product]:
        return ProductRepository.get_products()
    
    @classmethod
    def get_product(cls, product_id: int) -> Product:
        return ProductRepository.get_product(product_id)
    
    @classmethod
    def delete_product(cls, product_id: int) -> Product:
        return ProductRepository.delete_product(product_id)

    @classmethod
    def update_product(cls, product_id: int, product: Product) -> Product:
        if product_id != product.id:
            raise HTTPException(status_code = 400, detail = "Product ID does not match")
        return ProductRepository.update_product(product_id, product)
    
    @classmethod
    def patch_product(cls, product_id: int, product_patch: ProductPatch) -> Product:
        return ProductRepository.patch_product(product_id, product_patch)