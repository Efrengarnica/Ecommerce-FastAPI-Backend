from typing import List
from uuid import UUID
from pydantic import BaseModel, Field

from schemas.product import ProductResponse

class CartCreate(BaseModel):
    user_id: UUID
    
class CartItemResponse(BaseModel): 
    id: UUID
    cart_id: UUID
    product_id: int  
    quantity: int
    product: ProductResponse | None = None  
    model_config = {
        "from_attributes": True,  
    }
    
class CartResponse(BaseModel): 
    id: UUID
    user_id: UUID
    items: List[CartItemResponse] = []
    model_config = {
        "from_attributes": True,  
    }
    
class CartItemCreate(BaseModel):
    cart_id: UUID
    product_id: int = Field(gt=0)
    quantity: int = Field(default = 1, ge = 0)

class CartItemPatch(BaseModel):
    quantity: int = Field(ge=0)