from fastapi import APIRouter

from app.users.routers import user, user_address, cart
from app.orders.routers import order, order_item, cart_item
from app.products.routers import product, category, product_variant, size, color

api_router = APIRouter()

# Users
api_router.include_router(user.router)
api_router.include_router(user_address.router)
api_router.include_router(cart.router)

# Orders & Cart Items
api_router.include_router(order.router)
api_router.include_router(order_item.router)
api_router.include_router(cart_item.router)

# Products
api_router.include_router(product.router)
api_router.include_router(category.router)
api_router.include_router(product_variant.router)
api_router.include_router(size.router)
api_router.include_router(color.router)