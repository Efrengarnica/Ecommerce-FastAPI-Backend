from fastapi import FastAPI
from app.api.user import router as user_router
from app.api.product import router as product_router


app = FastAPI()

app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(product_router, prefix="/products", tags=["products"])
