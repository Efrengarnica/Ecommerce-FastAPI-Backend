from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship
from typing import List
from uuid import UUID, uuid4
from models.product import Product
    
class Cart(SQLModel, table = True):
    id: UUID = Field(default_factory = uuid4, primary_key = True)
    user_id: UUID = Field(foreign_key = "user.id")
    #Esto conecta la entidad CartItem con mi Cart pero solo me trae los cartItem que estan asociados a mi Cart por el cart_id,foreign_key en CartItem.
    items: List["CartItem"] = Relationship(back_populates = "cart")

class CartItem(SQLModel, table = True):
    id: UUID = Field(default_factory = uuid4, primary_key = True)  # ID único del ítem en el carrito
    cart_id: UUID = Field(foreign_key = "cart.id")  # Relación con el carrito
    product_id: int = Field(foreign_key = "product.id")  # Relación con el producto
    quantity: int = Field(default = 1, ge = 0)  # Cantidad mínima de 1 y mayor o igual que cero
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    cart: "Cart" = Relationship(back_populates = "items")  # Relación inversa con el carrito
    product: Product = Relationship()  # Agregamos la relación con el producto