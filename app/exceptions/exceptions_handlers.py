from fastapi import Request
from fastapi.responses import JSONResponse
from .exceptions import (UserNotFoundException, EmailAlreadyRegisteredException, ProductNotFoundException, ProductNameAlreadyExistsException, CartNotFoundException, CartAlreadyRegisteredException, CartItemNotFoundException, CartItemAlreadyRegisteredException, DatabaseIntegrityException, InternalServerErrorException )

async def user_not_found_handler(request: Request, exc: UserNotFoundException):
    return JSONResponse(status_code=404, content={"detail": exc.message})

async def email_already_registered_handler(request: Request, exc: EmailAlreadyRegisteredException):
    return JSONResponse(status_code=400, content={"detail": exc.message})

async def product_not_found_handler(request: Request, exc: ProductNotFoundException):
    return JSONResponse(status_code=404, content={"detail": exc.message})

async def product_name_already_exists_handler(request: Request, exc: ProductNameAlreadyExistsException):
    return JSONResponse(status_code=400, content={"detail": exc.message})

async def cart_not_found_handler(request: Request, exc: CartNotFoundException):
    return JSONResponse(status_code=404, content={"detail": exc.message})

async def cart_already_registered_handler(request: Request, exc: CartAlreadyRegisteredException):
    return JSONResponse(status_code=400, content={"detail": exc.message})

async def cart_item_not_found_handler(request: Request, exc: CartItemNotFoundException):
    return JSONResponse(status_code=404, content={"detail": exc.message})

async def cart_item_already_registered_handler(request: Request, exc: CartItemAlreadyRegisteredException):
    return JSONResponse(status_code=400, content={"detail": exc.message})

async def database_integrity_exception_handler(request: Request, exc: DatabaseIntegrityException):
    return JSONResponse(status_code=500, content={"detail": exc.message})

async def internal_server_error_exception_handler(request: Request, exc: InternalServerErrorException):
    return JSONResponse(status_code=500, content={"detail": exc.message})