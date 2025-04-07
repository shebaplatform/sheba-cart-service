from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import date, time, datetime
from decimal import Decimal
import enum

class CartItemStatusEnum(str, enum.Enum):
    pending = "pending"
    confirmed = "confirmed"

class CartItemCreate(BaseModel):
    service_id: int
    category_id: int
    partner_id: int
    quantity: int
    price: Decimal
    total_price: Decimal
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
