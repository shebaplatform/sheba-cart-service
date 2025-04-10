# app/schemas/cart_checkout.py

from typing import List, Optional
from pydantic import BaseModel
from datetime import date

class CartCheckoutRequest(BaseModel):
    name: str
    date: date
    remember_token: str
    portal_name: str
    version_code: str
    user_agent: str
    custom_headers: str
    platform_name: str
    lat: str
    lng: str

class CartCheckoutResponse(BaseModel):
    cart_id: str
    orders: List[dict]
