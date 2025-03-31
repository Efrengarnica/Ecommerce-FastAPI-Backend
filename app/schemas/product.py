from pydantic import BaseModel, Field

#Para la creación del producto.
class ProductCreate(BaseModel):
    name: str = Field(min_length = 3, description = "Product name")
    price: float = Field(ge = 0, description = "Price in MXN")
    category: str = Field(description = "Product category (e.g., women, men)")
    
#Para la respuesta del producto.
class ProductResponse(BaseModel):
    id:int
    name: str 
    price: float 
    category: str
    
    model_config = {
        "from_attributes": True,  
    }

#Esto lo ocupo para hacer el put
class ProductPut(BaseModel):
    id:int = Field(gt=0)
    name: str = Field(min_length = 3, description = "Product name")
    price: float = Field(ge = 0, description = "Price in MXN")
    category: str = Field(description = "Product category (e.g., women, men)")

# Esto lo ocupo para poder hacer el patch
class ProductPatch(BaseModel):
    name: str | None = Field(default = None, min_length = 3, description = "Product name")
    price: float | None = Field(default = None, ge = 0, description = "Price in MXN")
    category: str | None = Field(default = None, description = "Product category (e.g., women, men)")