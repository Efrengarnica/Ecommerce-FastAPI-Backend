from sqlmodel import SQLModel, Field

""" Se supone que SQLModel ya trae BaseModel y además esto hace que mi modelo sea una entidad """
class Product(SQLModel, table = True): #Table True hace que sea una tabla en mi base de datos
    id: int = Field(default = None, primary_key = True)
    name: str = Field(index = True, unique = True, min_length = 3)
    price: float = Field(ge = 0, description = "Price in MXN")  # Precio no negativo
    category: str = Field(
        index = True,
        description = "Product category (e.g., women, men)"
    )

# Esto lo ocupo para poder hacer el patch
class ProductPatch(SQLModel):
    name: str | None = Field(default = None, min_length = 3, description = "Product name")
    price: float | None = Field(default = None, ge = 0, description = "Price in MXN")
    category: str | None = Field(default = None, description = "Product category (e.g., women, men)")