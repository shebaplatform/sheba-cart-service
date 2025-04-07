from sqlalchemy import Column, String, Integer, Date, Time, Numeric, Enum, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum
from app.db.base import Base
from datetime import datetime, timezone

class CartItemStatusEnum(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"

class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cart_id = Column(UUID(as_uuid=True), ForeignKey("carts.id"))
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
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    cart = relationship("Cart", back_populates="items")
