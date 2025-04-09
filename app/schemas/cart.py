import enum
from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, field_validator

from app.schemas.cart_item import CartItemCreate

from .cart_item import CartItemOut


class PaymentMethodEnum(str, enum.Enum):
    cod = "cod"
    online = "online"
    wallet = "wallet"
    bkash = "bkash"
    cbl = "cbl"
    partner_wallet = "partner_wallet"
    bondhu_balance = "bondhu_balance"


class CartStatusEnum(str, enum.Enum):
    pending = "pending"
    confirmed = "confirmed"


class CartCreate(BaseModel):
    customer_id: Optional[int]
    name: Optional[str]
    address: Optional[str]
    address_id: Optional[int]
    mobile: Optional[str]
    payment_method: Optional[PaymentMethodEnum]
    status: Optional[CartStatusEnum] = CartStatusEnum.pending
    cart_items: List[CartItemCreate]

    @field_validator("status")
    @classmethod
    def status_must_be_pending(cls, v):
        if v != "pending":
            raise ValueError("Only carts with status 'pending' can be created.")
        return v


class CartOut(CartCreate):
    id: UUID
    created_at: datetime
    updated_at: datetime
    items: List[CartItemOut] = []

    class Config:
        orm_mode = True
