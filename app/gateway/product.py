from sqlite3 import IntegrityError
from fastapi import UploadFile
from models.product import Product
from schemas.product import ProductCreate, ProductPatch, ProductPut
from repository.product import ProductRepository
from exceptions.exceptions import (CloudinaryUploadException, DatabaseIntegrityException, InternalServerErrorException)
from services.cloudinary_service import upload_image_to_cloudinary

class ProductGateway:
    
    @classmethod
    def create_product(cls, product_create: ProductCreate, file: UploadFile) -> Product:
        try:
            # Subir la imagen y obtener la URL
            image_url = upload_image_to_cloudinary(file.file)
            if not image_url : 
                raise CloudinaryUploadException("No se pudo subir la imagen a Cloudinary")
            product_dict = product_create.model_dump()
            product_dict["image"] = image_url
            # Crear la entidad Product
            product_entity = Product(**product_dict)
            return ProductRepository.create_product(product_entity)
        except IntegrityError as e:
            raise DatabaseIntegrityException(str(e))
    
    @classmethod
    def get_products_hombre(cls) -> list[Product]:
        try:
            return ProductRepository.get_products_hombre()
        except Exception as e:
            raise InternalServerErrorException(str(e))
        
    @classmethod
    def get_products_mujer(cls) -> list[Product]:
        try:
            return ProductRepository.get_products_mujer()
        except Exception as e:
            raise InternalServerErrorException(str(e))
        
    @classmethod
    def search_products_men(cls, search: str) -> list[Product]:
        try:
            return ProductRepository.search_products_men(search)
        except Exception as e:
            raise InternalServerErrorException(str(e))
        
    @classmethod
    def search_products_women(cls, search: str) -> list[Product]:
        try:
            return ProductRepository.search_products_women(search)
        except Exception as e:
            raise InternalServerErrorException(str(e))
       
    @classmethod
    def get_product(cls, product_id: int) -> Product:
        return ProductRepository.get_product(product_id)
      
    @classmethod
    def delete_product(cls, product_id: int) -> Product:
        return ProductRepository.delete_product(product_id)
       
    @classmethod
    def update_product(cls, product_update: ProductPut, file: UploadFile) -> Product:
        try:
            image_url = upload_image_to_cloudinary(file.file)
            if not image_url : 
                raise CloudinaryUploadException("No se pudo subir la imagen a Cloudinary")
            product_dict = product_update.model_dump()
            product_dict["image"] = image_url
            product_entity = Product(**product_dict)
            return ProductRepository.update_product(product_entity)
        except IntegrityError as e:
            raise DatabaseIntegrityException(str(e))
    
    @classmethod
    def patch_product(cls, product_id: int, product_patch: ProductPatch) -> Product:
        try:
            return ProductRepository.patch_product(product_id, product_patch)
        except IntegrityError as e:
            raise DatabaseIntegrityException(str(e))
        
    @classmethod
    def patch_product_image(cls, product_id: int, file: UploadFile) -> Product:
            try:
                image_url = upload_image_to_cloudinary(file.file)
                if not image_url : 
                    raise CloudinaryUploadException("No se pudo subir la imagen a Cloudinary")
                return ProductRepository.patch_product_image(product_id, image_url)
            except IntegrityError as e:
                raise DatabaseIntegrityException(str(e))