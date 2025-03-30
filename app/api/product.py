from fastapi import APIRouter, Request
from app.models.product import Product, ProductPatch
from app.gateway.product import ProductGateway

router = APIRouter()

@router.post("/", response_model = Product)
def create_product(product: Product) -> Product:
    return ProductGateway.create_product(product)

@router.get("/")
def get_products() -> list[Product]:
    return ProductGateway.get_products()

@router.get("/{product_id}")
def get_product(product_id: int) -> Product:
    return ProductGateway.get_product(product_id)

@router.delete("/{product_id}")
def delete_product(product_id: int) -> Product:
    return ProductGateway.delete_product(product_id)

@router.put("/{product_id}")
def update_product(product_id: int, product: Product) -> Product:
    return ProductGateway.update_product(product_id, product)

@router.patch("/{product_id}")
async def patch_product(request: Request, product_id: int) -> Product:
    data = await request.json()
    return ProductGateway.patch_product(product_id, ProductPatch(**data))