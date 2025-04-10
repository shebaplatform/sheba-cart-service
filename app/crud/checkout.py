# app/crud/crud_cart.py

import httpx
from fastapi import HTTPException
from app.schemas.cart_checkout import CartCheckoutRequest
from app.crud.cart import get_cart

async def checkout_cart(db, cart_id: str, checkout_data: CartCheckoutRequest):
    cart = get_cart(db, cart_id)  # Make sure cart exists
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    orders = []  # Store responses or order IDs
    for item in cart.cart_items:
        body = {
            "name": checkout_data.name,
            "date": checkout_data.date,
            "remember_token": checkout_data.remember_token,
            "services": [{
                "id": item.service_id,
                "option": item.options or [],
                "quantity": item.quantity
            }],
            "address": cart.address,
            "mobile": cart.mobile,
            "payment_method": cart.payment_method,
            "time": f"{item.schedule_time.strftime('%H:%M:%S')}-{item.schedule_time.strftime('%H:%M:%S')}",
            "sales_channel": item.sales_channel,
            "address_id": cart.address_id,
        }

        headers = {
            "portal-name": checkout_data.portal_name,
            "user-id": str(cart.customer_id),
            "version-code": checkout_data.version_code,
            "user-agent": checkout_data.user_agent,
            "custom-headers": checkout_data.custom_headers,
            "platform-name": checkout_data.platform_name,
            "lat": checkout_data.lat,
            "lng": checkout_data.lng,
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient() as client:
            response = client.post("https://api.dev-sheba.xyz/v3/customers/188526/orders", json=body, headers=headers)
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="Order API call failed")
            orders.append(response.json())

    return {"cart_id": cart_id, "orders": orders}
