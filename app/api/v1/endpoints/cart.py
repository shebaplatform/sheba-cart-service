from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud import cart as crud_cart
from app.crud import cart_item as crud_cart_item
from app.crud import cart_item as crud_item
from app.schemas.cart import CartCreate, CartOut, CartUpdate
from app.schemas.cart_item import CartItemCreate, CartItemOut, CartItemUpdate

router = APIRouter()


@router.post("/", response_model=CartOut)
def create_cart(cart_in: CartCreate, db: Session = Depends(get_db)):
    return crud_cart.create_cart(db, cart_in)


@router.get("/", response_model=List[CartOut])
def list_carts(customer_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    return crud_cart.get_carts(db, customer_id=customer_id)


@router.get("/{cart_id}", response_model=CartOut)
def get_cart(cart_id: UUID, db: Session = Depends(get_db)):
    cart = crud_cart.get_cart(db, cart_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart


@router.delete("/{cart_id}")
def delete_cart(cart_id: UUID, db: Session = Depends(get_db)):
    cart = crud_cart.delete_cart(db, cart_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return {"detail": "Cart deleted"}


@router.post("/{cart_id}/items")
def add_cart_item(cart_id: UUID, item: CartItemCreate, db: Session = Depends(get_db)):
    return crud_item.create_cart_item(db, cart_id, item)


@router.patch("/{cart_id}", response_model=CartOut)
def update_cart(cart_id: UUID, cart_in: CartUpdate, db: Session = Depends(get_db)):
    return crud_cart.update_cart(db, cart_id, cart_in)


@router.patch("/{cart_id}/items/{cart_item_id}", response_model=CartItemOut)
def update_cart_item(
    cart_id: UUID,
    cart_item_id: UUID,
    item_in: CartItemUpdate,
    db: Session = Depends(get_db),
):
    # Ensure the cart ID matches the cart item being updated
    return crud_cart_item.update_cart_item(db, cart_id, cart_item_id, item_in)


@router.delete("/{cart_id}/items/{cart_item_id}", status_code=204)
def delete_cart_item(cart_id: UUID, cart_item_id: UUID, db: Session = Depends(get_db)):
    success = crud_cart_item.delete_cart_item(db, cart_id, cart_item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Cart item not found or mismatch.")
