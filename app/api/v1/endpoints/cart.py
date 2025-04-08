from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.schemas.cart import CartCreate, CartOut
from app.schemas.cart_item import CartItemCreate
from app.crud import cart as crud_cart, cart_item as crud_item
from app.api.deps import get_db

router = APIRouter()

@router.post("/", response_model=CartOut)
def create_cart(cart_in: CartCreate, db: Session = Depends(get_db)):
    return crud_cart.create_cart(db, cart_in)

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
