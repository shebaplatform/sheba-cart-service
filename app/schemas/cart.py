from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from decimal import Decimal
from datetime import datetime
from .cart_item import CartItemOut
import enum

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
    session_id: Optional[str]
    name: Optional[str]
    address: Optional[str]
    address_id: Optional[int]
    mobile: Optional[str]
    payment_method: Optional[PaymentMethodEnum]
    status: Optional[CartStatusEnum] = CartStatusEnum.pending
    total: Optional[Decimal]

class CartOut(CartCreate):
    id: UUID
    created_at: datetime
    updated_at: datetime
    items: List[CartItemOut] = []

    class Config:
        orm_mode = True
