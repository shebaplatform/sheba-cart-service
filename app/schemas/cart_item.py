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

    # @field_validator("status")
    # @classmethod
    # def status_must_be_pending(cls, v):
    #     if v != "pending":
    #         raise ValueError("Only carts with status 'pending' can be created.")
    #     return v


class CartItemOut(CartItemCreate):
    id: UUID
    cart_id: UUID
    status: Optional[CartItemStatusEnum] = CartItemStatusEnum.pending
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class CartItemUpdate(BaseModel):
    partner_id: Optional[int]
    quantity: Optional[int]
    price: Optional[Decimal]
    schedule_date: Optional[date]
    schedule_time: Optional[time]
    sales_channel: Optional[str]
