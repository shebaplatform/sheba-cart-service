import enum
from datetime import date, datetime, time
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, field_validator


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
    options: Optional[List[int]]
    status: Optional[CartItemStatusEnum] = CartItemStatusEnum.pending

    @field_validator("status")
    @classmethod
    def status_must_be_pending(cls, v):
        if v != "pending":
            raise ValueError("Only carts with status 'pending' can be created.")
        return v


class CartItemOut(CartItemCreate):
    id: UUID
    cart_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
