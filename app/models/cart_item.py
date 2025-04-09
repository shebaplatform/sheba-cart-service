import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Time,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class CartItemStatusEnum(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"


class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cart_id = Column(
        UUID(as_uuid=True), ForeignKey("carts.id", ondelete="CASCADE"), nullable=False
    )
    service_id = Column(Integer)
    category_id = Column(Integer)
    partner_id = Column(Integer)
    quantity = Column(Integer, default=1)
    price = Column(Numeric(10, 2))
    total_price = Column(Numeric(10, 2))
    schedule_date = Column(Date)
    schedule_time = Column(Time)
    sales_channel = Column(String)
    options = Column(ARRAY(String))
    status = Column(Enum(CartItemStatusEnum), default=CartItemStatusEnum.PENDING)

    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )

    cart = relationship("Cart", back_populates="cart_items")

    __table_args__ = (
        UniqueConstraint(
            "cart_id",
            "service_id",
            "category_id",
            "partner_id",
            "schedule_date",
            "schedule_time",
            "options",
            name="uq_cart_item_composite_key",
        ),
    )
