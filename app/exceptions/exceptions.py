from uuid import UUID

class UserNotFoundException(Exception):
    def __init__(self, user_id: UUID):
        self.user_id = user_id
        self.message = f"User with ID {user_id} not found."
        super().__init__(self.message)

class EmailAlreadyRegisteredException(Exception):
    def __init__(self, email: str):
        self.email = email
        self.message = f"Email {email} already registered."
        super().__init__(self.message)

class ProductNotFoundException(Exception):
    def __init__(self, product_id: int):
        self.product_id = product_id
        self.message = f"Product with ID {product_id} not found."
        super().__init__(self.message)

class ProductNameAlreadyExistsException(Exception):
    def __init__(self, product_name: str):
        self.product_name = product_name
        self.message = f"Product name '{product_name}' already exists."
        super().__init__(self.message)

class CartNotFoundException(Exception):
    def __init__(self, cart_id: UUID):
        self.cart_id = cart_id
        self.message = f"Cart with ID {cart_id} not found."
        super().__init__(self.message)

class CartAlreadyRegisteredException(Exception):
    def __init__(self, cart_id: UUID):
        self.cart_id = cart_id
        self.message = f"Cart with ID {cart_id} already registered."
        super().__init__(self.message)

class CartItemNotFoundException(Exception):
    def __init__(self, cart_item_id: UUID):
        self.cart_item_id = cart_item_id
        self.message = f"Cart item with ID {cart_item_id} not found."
        super().__init__(self.message)

class CartItemAlreadyRegisteredException(Exception):
    def __init__(self, cart_item_id: UUID):
        self.cart_item_id = cart_item_id
        self.message = f"Cart item with ID {cart_item_id} already registered."
        super().__init__(self.message)

class DatabaseIntegrityException(Exception):
    def __init__(self, detail: str):
        self.detail = detail
        self.message = f"Database integrity error: {detail}"
        super().__init__(self.message)

class InternalServerErrorException(Exception):
    def __init__(self, detail: str = "Internal server error"):
        self.detail = detail
        self.message = detail
        super().__init__(self.message)