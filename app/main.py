#Aqui esta la app principal de FastAPI, tengo que importar los routers de todos los controllers para que se asocien a esta app
from fastapi import FastAPI
from app.api.user import router as user_router
from app.api.product import router as product_router
from app.api.cart import router as cart_router
from app.exceptions.exceptions import(CartAlreadyRegisteredException, CartItemAlreadyRegisteredException, CartItemNotFoundException, CartNotFoundException, CloudinaryUploadException, DatabaseIntegrityException, EmailAlreadyRegisteredException, InternalServerErrorException, ProductNameAlreadyExistsException, ProductNotFoundException, UserNotFoundException)
from app.exceptions.exceptions_handlers import (cart_already_registered_handler, cart_item_already_registered_handler, cart_item_not_found_handler, cart_not_found_handler, cloudinary_upload_exception_handler, database_integrity_exception_handler, email_already_registered_handler, internal_server_error_exception_handler, product_name_already_exists_handler, product_not_found_handler, user_not_found_handler)
#Permisos.
from fastapi.middleware.cors import CORSMiddleware
# pip install cloudinary
import cloudinary
#pip install python-dotenv
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env, no se sube al repo
load_dotenv()

#App principal de FASTAPI
app = FastAPI()

#Routers que se incluyen en la app
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(product_router, prefix="/products", tags=["products"])
app.include_router(cart_router, prefix="/carts", tags=["carts"])

#Necesario para poder hacer las peticiones a la API, estan en el 
#archivo .env y las conseguí registrandome en cloudinary.
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

#Esto es para poder permitir peticiones desde otro servidor, es para conectar
#mi back con mi front me falta implementrarlo.
app.add_middleware(
     CORSMiddleware,
     allow_origins=["http://localhost:5173"],
     allow_credentials=True,
     allow_methods=["*"],
     allow_headers=["*"],
 )

# Registrar los manejadores globales de excepciones personalizadas
app.add_exception_handler(UserNotFoundException, user_not_found_handler)
app.add_exception_handler(EmailAlreadyRegisteredException, email_already_registered_handler)
app.add_exception_handler(ProductNotFoundException, product_not_found_handler)
app.add_exception_handler(ProductNameAlreadyExistsException, product_name_already_exists_handler)
app.add_exception_handler(CartNotFoundException, cart_not_found_handler)
app.add_exception_handler(CartAlreadyRegisteredException, cart_already_registered_handler)
app.add_exception_handler(CartItemNotFoundException, cart_item_not_found_handler)
app.add_exception_handler(CartItemAlreadyRegisteredException, cart_item_already_registered_handler)
app.add_exception_handler(DatabaseIntegrityException, database_integrity_exception_handler)
app.add_exception_handler(InternalServerErrorException, internal_server_error_exception_handler)
app.add_exception_handler(CloudinaryUploadException, cloudinary_upload_exception_handler)