from fastapi import APIRouter

from .endpoints import cart

api_router = APIRouter()
api_router.include_router(cart.router, prefix="/carts", tags=["Carts"])
