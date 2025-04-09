from uuid import UUID, uuid4

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.cart_item import CartItem
from app.schemas.cart_item import CartItemCreate, CartItemStatusEnum, CartItemUpdate


def create_cart_item(db: Session, cart_id, item_in: CartItemCreate):
    db_item = CartItem(**item_in.model_dump(), cart_id=cart_id)

    try:
        db.add(db_item)
        db.commit()  # Moved into try block (not outside flush)
        db.refresh(db_item)
    except IntegrityError as e:
        db.rollback()

        if "uq_cart_item_composite_key" in str(e.orig):
            raise HTTPException(
                status_code=409,
                detail="This cart item already exists with the same cart, service, category, partner, schedule, and options.",
            )
        raise HTTPException(status_code=500, detail="Unexpected database error.")

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
        # status=item_in.status,
    )

    db.add(item)

    print("🚀 Inserting new cart item")
    try:
        db.flush()
    except IntegrityError as e:

        db.rollback()
        existing_item = (
            db.query(CartItem)
            .filter_by(
                cart_id=cart_id,
                service_id=item_in.service_id,
                category_id=item_in.category_id,
                partner_id=item_in.partner_id,
                schedule_date=item_in.schedule_date,
                schedule_time=item_in.schedule_time,
                options=options,
            )
            .first()
        )

        if existing_item:
            existing_item.quantity += item_in.quantity
            existing_item.total_price += total_price
            db.add(existing_item)
            db.flush()
        else:
            raise

    return total_price


def update_cart_item(
    db: Session, cart_id: UUID, cart_item_id: UUID, item_in: CartItemUpdate
):
    cart_item = db.query(CartItem).filter(CartItem.id == cart_item_id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart Item not found")

    # Ensure the cart ID matches the one in the cart item
    if cart_item.cart_id != cart_id:
        raise HTTPException(
            status_code=400, detail="Cart ID does not match the cart item"
        )

    # Check if status is 'pending' before allowing update
    if cart_item.status != CartItemStatusEnum.pending:
        raise HTTPException(
            status_code=400, detail="Only pending cart items can be updated"
        )

    for field, value in item_in.model_dump(exclude_unset=True).items():
        setattr(cart_item, field, value)

    # Recalculate total price (optional, if needed based on price and quantity)
    cart_item.total_price = cart_item.quantity * cart_item.price

    db.commit()
    db.refresh(cart_item)
    return cart_item


def delete_cart_item(db: Session, cart_id: UUID, cart_item_id: UUID) -> bool:
    cart_item = (
        db.query(CartItem)
        .filter(CartItem.id == cart_item_id, CartItem.cart_id == cart_id)
        .first()
    )

    if not cart_item:
        return False

    # Only allow deleting if status is 'pending'
    if cart_item.status != CartItemStatusEnum.pending:
        return False

    db.delete(cart_item)
    db.commit()
    return True
