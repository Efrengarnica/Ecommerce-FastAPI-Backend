from sqlmodel import SQLModel, Field

""" Se supone que SQLModel ya trae BaseModel y además esto hace que mi modelo sea una entidad """
class Product(SQLModel, table = True): #Table True hace que sea una tabla en mi base de datos
    id: int | None = Field(
        default=None, 
        primary_key=True, 
        sa_column_kwargs={"autoincrement": True}  
    )
    name: str = Field(index = True, unique = True, min_length = 3)
    price: float = Field(ge = 0, description = "Price in MXN")  # Precio no negativo
    category: str = Field(
        index = True,
        description = "Product category (e.g., women, men)"
    )
    image:str