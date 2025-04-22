from sqlite3 import IntegrityError
from fastapi import UploadFile
from models.product import Product
from schemas.product import ProductCreate, ProductPatch, ProductPut
from repository.product import ProductRepository
from exceptions.exceptions import (CloudinaryUploadException, DatabaseIntegrityException, InternalServerErrorException)
from services.cloudinary_service import upload_image_to_cloudinary
from starlette.concurrency import run_in_threadpool


class ProductGateway:
    
    @classmethod
    async def create_product(cls, product_create: ProductCreate, file: UploadFile) -> Product:
        try:
            # Subir la imagen y obtener la URL
            #image_url = upload_image_to_cloudinary(file.file)
            #Esto es necesario ya que la funcion para subir la imagen
            #a cloudianry es sincrona entonces al usar esto no bloqueamos el evento principal.
            image_url = await run_in_threadpool(upload_image_to_cloudinary, file.file)
            if not image_url : 
                raise CloudinaryUploadException("No se pudo subir la imagen a Cloudinary")
            product_dict = product_create.model_dump()
            product_dict["image"] = image_url
            # Crear la entidad Product
            product_entity = Product(**product_dict)
            return await ProductRepository.create_product(product_entity)
        except IntegrityError as e:
            raise DatabaseIntegrityException(str(e))
    
    @classmethod
    async def get_products_hombre(cls) -> list[Product]:
        try:
            return await ProductRepository.get_products_hombre()
        except Exception as e:
            raise InternalServerErrorException(str(e))
        
    @classmethod
    async def get_products_mujer(cls) -> list[Product]:
        try:
            return await ProductRepository.get_products_mujer()
        except Exception as e:
            raise InternalServerErrorException(str(e))
        
    @classmethod
    async def search_products_men(cls, search: str) -> list[Product]:
        try:
            return await ProductRepository.search_products_men(search)
        except Exception as e:
            raise InternalServerErrorException(str(e))
        
    @classmethod
    async def search_products_women(cls, search: str) -> list[Product]:
        try:
            return await ProductRepository.search_products_women(search)
        except Exception as e:
            raise InternalServerErrorException(str(e))
       
    @classmethod
    async def get_product(cls, product_id: int) -> Product:
        return await ProductRepository.get_product(product_id)
      
    @classmethod
    async def delete_product(cls, product_id: int) -> Product:
        return await ProductRepository.delete_product(product_id)
       
    @classmethod
    async def update_product(cls, product_update: ProductPut, file: UploadFile) -> Product:
        try:
            #image_url = upload_image_to_cloudinary(file.file)
            image_url = await run_in_threadpool(upload_image_to_cloudinary, file.file)
            if not image_url : 
                raise CloudinaryUploadException("No se pudo subir la imagen a Cloudinary")
            product_dict = product_update.model_dump()
            product_dict["image"] = image_url
            product_entity = Product(**product_dict)
            return await ProductRepository.update_product(product_entity)
        except IntegrityError as e:
            raise DatabaseIntegrityException(str(e))
    
    @classmethod
    async def patch_product(cls, product_id: int, product_patch: ProductPatch) -> Product:
        try:
            return await ProductRepository.patch_product(product_id, product_patch)
        except IntegrityError as e:
            raise DatabaseIntegrityException(str(e))
        
    @classmethod
    async def patch_product_image(cls, product_id: int, file: UploadFile) -> Product:
            try:
                #image_url = upload_image_to_cloudinary(file.file)
                image_url = await run_in_threadpool(upload_image_to_cloudinary, file.file)
                if not image_url : 
                    raise CloudinaryUploadException("No se pudo subir la imagen a Cloudinary")
                return await ProductRepository.patch_product_image(product_id, image_url)
            except IntegrityError as e:
                raise DatabaseIntegrityException(str(e))