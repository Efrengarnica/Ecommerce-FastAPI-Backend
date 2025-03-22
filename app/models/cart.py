from sqlmodel import SQLModel, Field, Relationship
from typing import List
from uuid import UUID, uuid4

""" Pude haber separado cada clase pero al parecer no es tan necesario aquí
    las lineas de items, en Cart, y cart, en CartItem, son una manera de acceder 
    a los datos de cada entidad usando la otra entidad.
    En realidad no afecta en nada a la base de datos.
"""

# Modelo para Cart
""" En realidad me ayuda a crear una cart pero NO puedo usar Cart ya que es una entidad, table = True, entonces
    tengo que ocupar CartCreate(SQLModel) ya que esto sin table = true puede convertir datos como cadenas a 
    datos complejos como UUID.
"""
class CartCreate(SQLModel):
    user_id: UUID  # Pydantic convierte el string a UUID si tiene formato válido
    
# Cart hereda de CartCreate, entonces Cart tambien es SQLModel, cuando creo una instancia de Cart tambien puedo pasar user_id.
class Cart(CartCreate, table = True):
    id: UUID = Field(default_factory = uuid4, primary_key = True)
    user_id: UUID = Field(foreign_key = "user.id")
    #Esto conecta la entidad CartItem con mi Cart pero solo me trae los cartItem que estan asociados a mi Cart por el cart_id,foreign_key en CartItem.
    items: List["CartItem"] = Relationship(back_populates = "cart")


#Modelo para CartItem
#Lo mismo que arriba, hago esto para que pueda en mi solicitud agregar una cadena de texto y pueda convertirla exitosamente a UUID
class CartItemCreate(SQLModel):
    cart_id: UUID
    product_id: int

class CartItem(CartItemCreate, table = True):
    id: UUID = Field(default_factory = uuid4, primary_key = True)  # ID único del ítem en el carrito
    cart_id: UUID = Field(foreign_key = "cart.id")  # Relación con el carrito
    product_id: int = Field(foreign_key = "product.id")  # Relación con el producto
    quantity: int = Field(default = 1, gt = 0)  # Cantidad mínima de 1 y mayor que cero
    cart: "Cart" = Relationship(back_populates = "items")  # Relación inversa con el carrito

#Esta se crea para poder realizar con exito el patch    
class CartItemPatch(SQLModel):
    quantity: int = Field(ge = 0)
    
""" Mira cuando FastApi regresas un Objeto que es una entidad si esa entidad es sencilla y no tiene relaciones 
    complicadas como una lista de objetos de otra entidad entonces puede trasnformar esa entidad a formato Json sin problemas 
    Pero cuando hay una relacion complicada como en el caso del cart TU debes de decirle a fastApi como convertir 
    eso en un formato json aceptable, es por eso que ocupamos lo de abajo, el decir orm_mode = True le dice a FastApi 
    Que antes de transofrmar a json debes de considerar que los objetos son de esa manera
    Al final todo es igual solo que el formato de salida debe de ser CartResponse para que fastApi sepa como manejar la conversion.
"""
# Esta parte es para que cuando hago una peticion get me devuelva los items asociados a mi carrito
# Este modelo me permite que aparezcan en la solicitud en formato JSON los items, recordar que aprte de esto se necesita lo de Controller y lo de Repositoy.
class CartItemResponse(SQLModel): #BaseModel
    id: UUID
    cart_id: UUID
    product_id: int  
    quantity: int
    class Config:
        orm_mode = True    ##No es necesario

class CartResponse(SQLModel): #BaseModel
    id: UUID
    user_id: UUID
    items: List[CartItemResponse] = []
    class Config:
        orm_mode = True # Esto hace que la lista de items haga esto "Oye, estos no son diccionarios normales, sino objetos ORM. Por favor, convierte sus atributos en JSON."