#Aqui esta la app principal de FastAPI, tengo que importar los routers de todos los controllers para que se asocien a esta app
from fastapi import FastAPI
from app.api.user import router as user_router
from app.api.product import router as product_router
from app.api.cart import router as cart_router
from app.exceptions.exceptions import(CartAlreadyRegisteredException, CartItemAlreadyRegisteredException, CartItemNotFoundException, CartNotFoundException, DatabaseIntegrityException, EmailAlreadyRegisteredException, InternalServerErrorException, ProductNameAlreadyExistsException, ProductNotFoundException, UserNotFoundException)
from app.exceptions.exceptions_handlers import (cart_already_registered_handler, cart_item_already_registered_handler, cart_item_not_found_handler, cart_not_found_handler, database_integrity_exception_handler, email_already_registered_handler, internal_server_error_exception_handler, product_name_already_exists_handler, product_not_found_handler, user_not_found_handler)
#App principal de FASTAPI
app = FastAPI()

#Routers que se incluyen en la app
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(product_router, prefix="/products", tags=["products"])
app.include_router(cart_router, prefix="/carts", tags=["carts"])

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