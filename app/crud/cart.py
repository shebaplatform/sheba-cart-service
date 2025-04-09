from uuid import uuid4

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.crud import cart_item as crud_cart_item
from app.models.cart import Cart
from app.schemas.cart import CartCreate, CartUpdate


def create_cart(db: Session, cart_in: CartCreate) -> Cart:
    # Create cart
    cart = Cart(
        id=uuid4(),
        customer_id=cart_in.customer_id,
        name=cart_in.name,
        address=cart_in.address,
        address_id=cart_in.address_id,
        mobile=cart_in.mobile,
        payment_method=cart_in.payment_method,
        total=0,
    )
    db.add(cart)

    try:
        db.flush()
    except IntegrityError as e:
        db.rollback()
        if "uq_customer_status" in str(e.orig):
            raise HTTPException(
                status_code=409, detail="Cart already exists for this customer."
            )
        raise HTTPException(
            status_code=500, detail="An unexpected database error occurred."
        )

    # Create related cart items
    total_amount = 0
    for item in cart_in.cart_items:
        added_total = crud_cart_item.upsert_cart_item(db, cart.id, item)
        total_amount += added_total

    cart.total = total_amount

    db.commit()
    db.refresh(cart)
    return cart


def get_cart(db: Session, cart_id):
    return db.query(Cart).filter(Cart.id == cart_id).first()


def delete_cart(db: Session, cart_id):
    cart = get_cart(db, cart_id)
    if cart:
        db.delete(cart)
        db.commit()
    return cart


def update_cart(db: Session, cart_id, cart_in: CartUpdate):
    cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    for field, value in cart_in.model_dump(exclude_unset=True).items():
        if field != "cart_items":
            setattr(cart, field, value)

    db.commit()
    db.refresh(cart)
    return cart
