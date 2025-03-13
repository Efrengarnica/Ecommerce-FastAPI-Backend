#Aqui esta la app principal de FastAPI, tengo que importar los routers de todos los controllers para que se asocien a esta app
from fastapi import FastAPI
from app.api.user import router as user_router
from app.api.product import router as product_router
from app.api.cart import router as cart_router

#App principal de FASTAPI
app = FastAPI()

#Routers que se incluyen en la app
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(product_router, prefix="/products", tags=["products"])
app.include_router(cart_router, prefix="/carts", tags=["carts"])