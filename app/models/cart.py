from sqlalchemy import Column, String, Integer, DateTime, Numeric, Enum, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid
import enum
from app.db.base import Base

class PaymentMethodEnum(str, enum.Enum):
    COD = "cod"
    ONLINE = "online"
    WALLET = "wallet"
    BKASH = "bkash"
    CBL = "cbl"
    PARTNER_WALLET = "partner_wallet"
    BONDHU_BALANCE = "bondhu_balance"

class CartStatusEnum(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"

class Cart(Base):
    __tablename__ = "carts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(Integer)
    name = Column(String)
    address = Column(String)
    address_id = Column(Integer, nullable=True)
    mobile = Column(String)
    payment_method = Column(Enum(PaymentMethodEnum), nullable=True)
    status = Column(Enum(CartStatusEnum), default=CartStatusEnum.PENDING)
    total = Column(Numeric(10, 2), default=0)

    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    cart_items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("customer_id", "status", name="uq_customer_status"),
    )
