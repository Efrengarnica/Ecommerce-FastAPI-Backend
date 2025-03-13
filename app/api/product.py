from fastapi import APIRouter, Request, Depends
from app.models.product import Product, ProductPatch
from app.gateway.product import ProductGateway
from sqlmodel import Session
from app.database import get_session

router = APIRouter()

@router.post("/", response_model = Product)
def create_product(product: Product, session: Session = Depends(get_session)) -> Product:
    return ProductGateway.create_product(product, session)

@router.get("/")
def get_products(session: Session = Depends(get_session)) -> list[Product]:
    return ProductGateway.get_products(session)

@router.get("/{product_id}")
def get_product(product_id: int, session: Session = Depends(get_session)) -> Product:
    return ProductGateway.get_product(product_id, session)

@router.delete("/{product_id}")
def delete_product(product_id: int, session: Session = Depends(get_session)) -> Product:
    return ProductGateway.delete_product(product_id, session)

@router.put("/{product_id}")
def update_product(product_id: int, product: Product, session: Session = Depends(get_session)) -> Product:
    return ProductGateway.update_product(product_id, product, session)

@router.patch("/{product_id}")
async def patch_product(request: Request, product_id: int, session: Session = Depends(get_session)) -> Product:
    data = await request.json()
    return ProductGateway.patch_product(product_id, ProductPatch(**data), session)