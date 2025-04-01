from fastapi import APIRouter,Depends, File, Form, Request, UploadFile

from app.models.product import Product
from app.schemas.product import ProductPatch, ProductCreate, ProductPut, ProductResponse
from app.gateway.product import ProductGateway

router = APIRouter()
    
@router.post("/", response_model = ProductResponse)
async def create_product(name: str = Form(...), price: float = Form(...), category: str = Form(...),  file: UploadFile = File(...)) -> ProductResponse:
    product_create = ProductCreate(name=name, price=price, category=category)
    created_product = ProductGateway.create_product(product_create, file)
    return ProductResponse.model_validate(created_product)


@router.get("/", response_model = list[ProductResponse])
def get_products() -> list[ProductResponse]:
    products = ProductGateway.get_products()
    return [ProductResponse.model_validate(product) for product in products]

@router.get("/{product_id}", response_model = ProductResponse)
def get_product(product_id: int) -> ProductResponse:
    created_product = ProductGateway.get_product(product_id)
    return ProductResponse.model_validate(created_product)

@router.delete("/{product_id}", response_model = ProductResponse)
def delete_product(product_id: int) -> ProductResponse:
    delete_product = ProductGateway.delete_product(product_id)
    return ProductResponse.model_validate(delete_product)

@router.put("/", response_model = ProductResponse)
def update_product(id:int=Form(...), name: str = Form(...), price: float = Form(...), category: str = Form(...), file: UploadFile = File(...)) -> ProductResponse:
    product_put = ProductPut(id=id, name=name, price=price, category=category)
    created_product = ProductGateway.update_product(product_put, file)
    return ProductResponse.model_validate(created_product)

@router.patch("/{product_id}", response_model = ProductResponse)
async def patch_product(request: Request, product_id: int) -> ProductResponse:
    data = await request.json()
    created_product = ProductGateway.patch_product(product_id, ProductPatch(**data))
    return ProductResponse.model_validate(created_product)

@router.patch("/{product_id}/image", response_model=ProductResponse)
def patch_product_image(product_id: int, file: UploadFile = File(...)) -> ProductResponse:
    created_product = ProductGateway.patch_product_image(product_id, file)
    return ProductResponse.model_validate(created_product)