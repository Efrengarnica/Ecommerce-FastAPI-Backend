from sqlmodel import SQLModel, Field, Relationship
from typing import List
from uuid import UUID, uuid4

""" Pude haber separado cada clase pero al parecer no es tan necesario aquí
    las lineas de items y cart son una mandera de acceder a los datos de cada entidad usando la otra entidad.
    En realidad no afecta en nada a la base de datos.
"""

# Modelo de entrada para validar la solicitud
class CartCreate(SQLModel):
    user_id: UUID  # Pydantic convierte el string a UUID si tiene formato válido

# Modelo que mapea a la base de datos
class Cart(CartCreate, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id")
    items: List["CartItem"] = Relationship(back_populates="cart")

class CartItemCreate(SQLModel):
    cart_id:UUID
    product_id: int

class CartItem(CartItemCreate, table=True):  # Modelo que representa los productos en el carrito
    id: UUID = Field(default_factory=uuid4, primary_key=True)  # ID único del ítem en el carrito
    cart_id: UUID = Field(foreign_key="cart.id")  # Relación con el carrito
    product_id: int = Field(foreign_key="product.id")  # Relación con el producto
    quantity: int = Field(default=1, gt=0)  # Cantidad mínima de 1 y mayor que cero

    cart: "Cart" = Relationship(back_populates="items")  # Relación inversa con el carrito
    
class CartItemPatch(SQLModel):
    quantity: int = Field( ge=0 )
    
    
    
class CartItemResponse(SQLModel):
    id: UUID
    cart_id: UUID
    product_id: int
    quantity: int

    class Config:
        orm_mode = True    
    
class CartResponse(SQLModel):
    id: UUID
    user_id: UUID
    items: List[CartItemResponse] = []

    class Config:
        orm_mode = True
