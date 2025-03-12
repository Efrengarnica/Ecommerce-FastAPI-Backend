from sqlmodel import SQLModel, Field, Relationship
from typing import List
from uuid import UUID, uuid4

""" Pude haber separado cada clase pero al parecer no es tan necesario aquí
    las lineas de items y cart son una mandera de acceder a los datos de cada entidad usando la otra entidad.
    En realidad no afecta en nada a la base de datos.
"""

class Cart(SQLModel, table=True):  # Modelo que representa el carrito
    id: UUID = Field(default_factory=uuid4, primary_key=True)  # ID único del carrito
    user_id: UUID = Field(foreign_key="user.id")  # Relación con el usuario
    
    items: List["CartItem"] = Relationship(back_populates="cart")  # Relación con los productos dentro del carrito

class CartItem(SQLModel, table=True):  # Modelo que representa los productos en el carrito
    id: UUID = Field(default_factory=uuid4, primary_key=True)  # ID único del ítem en el carrito
    cart_id: UUID = Field(foreign_key="cart.id")  # Relación con el carrito
    product_id: UUID = Field(foreign_key="product.id")  # Relación con el producto
    quantity: int = Field(default=1, gt=0)  # Cantidad mínima de 1 y mayor que cero

    cart: "Cart" = Relationship(back_populates="items")  # Relación inversa con el carrito