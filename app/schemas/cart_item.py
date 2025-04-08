import enum
from datetime import date, datetime, time
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class CartItemStatusEnum(str, enum.Enum):
    pending = "pending"
    confirmed = "confirmed"

class CartItemCreate(BaseModel):
    service_id: int
    category_id: int
    partner_id: int
    quantity: int
    price: Decimal
    schedule_date: date
    schedule_time: time
    sales_channel: Optional[str]
    options: Optional[List[str]]
    status: Optional[CartItemStatusEnum] = CartItemStatusEnum.pending

class CartItemOut(CartItemCreate):
    id: UUID
    cart_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
