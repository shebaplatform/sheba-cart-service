from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.cart_item import CartItem
from app.schemas.cart_item import CartItemCreate
from uuid import uuid4

def create_cart_item(db: Session, cart_id, item_in: CartItemCreate):
    db_item = CartItem(**item_in.model_dump(), cart_id=cart_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def upsert_cart_item(db: Session, cart_id, item_in: CartItemCreate) -> float:
    """Insert or update a CartItem, return total_price added to cart total."""

    options = sorted(item_in.options) if item_in.options else []
    total_price = item_in.price * item_in.quantity

    item = CartItem(
        id=uuid4(),
        cart_id=cart_id,
        service_id=item_in.service_id,
        category_id=item_in.category_id,
        partner_id=item_in.partner_id,
        quantity=item_in.quantity,
        price=item_in.price,
        total_price=total_price,
        schedule_date=item_in.schedule_date,
        schedule_time=item_in.schedule_time,
        sales_channel=item_in.sales_channel,
        options=options,
        status=item_in.status,
    )

    db.add(item)
   
    print("🚀 Inserting new cart item")
    try:
        db.flush()
    except IntegrityError as e:
        print("⚠️ IntegrityError caught:", e)
        db.rollback()
        existing_item = db.query(CartItem).filter_by(
            cart_id=cart_id,
            service_id=item_in.service_id,
            category_id=item_in.category_id,
            partner_id=item_in.partner_id,
            schedule_date=item_in.schedule_date,
            schedule_time=item_in.schedule_time,
            options=options
        ).first()

        if existing_item:
            existing_item.quantity += item_in.quantity
            existing_item.total_price += total_price
            db.add(existing_item)
            db.flush()
        else:
            raise

    return total_price
