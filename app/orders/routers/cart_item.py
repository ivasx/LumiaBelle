from typing import Annotated, Sequence

import sqlalchemy
from fastapi import Depends, HTTPException, APIRouter
from app.utils import auth
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from app.core.settings.db import db

from ..models.cart_item import CartItemModel
from ..schemas.cart_item import CartItemResponseSchema, CartItemCreateSchema, CartItemPartialUpdateSchema

SessionDepend = Annotated[AsyncSession, Depends(db.get_session)]

router = APIRouter(prefix="/cart_item", tags=["cart_items"])


@router.post(
    path="/{cart_id}",
    response_model=CartItemResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_cart_item(cart_id: int, cart_item: CartItemCreateSchema, session: SessionDepend):
    new_cart_item = CartItemModel(
        cart_id=cart_id,
        product_variant_id=cart_item.product_variant_id,
        quantity=cart_item.quantity,
    )
    session.add(new_cart_item)
    await session.commit()
    await session.refresh(new_cart_item)
    return new_cart_item


@router.get(
    path="/{cart_id}/items",
    response_model=list[CartItemResponseSchema],
)
async def get_cart_items(cart_id: int, session: SessionDepend) -> Sequence[CartItemModel]:
    query = sqlalchemy.select(CartItemModel).where(CartItemModel.cart_id == cart_id)
    result = await session.execute(query)
    cart_items = result.scalars().all()
    return cart_items


@router.get(
    path="/{cart_id}/items/{cart_item_id}",
    response_model=CartItemResponseSchema,
)
async def get_cart_item(cart_id: int, cart_item_id: int, session: SessionDepend):
    result = await session.execute(
        sqlalchemy.select(CartItemModel)
        .where(CartItemModel.id == cart_item_id)
        .where(CartItemModel.cart_id == cart_id)
    )
    cart_item = result.scalars().first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return cart_item


@router.put(
    path="/{cart_id}/items/{cart_item_id}",
    response_model=CartItemResponseSchema,
)
async def update_cart_item(cart_id: int, cart_item_id: int, cart_item: CartItemCreateSchema, session: SessionDepend):
    result = await session.execute(
        sqlalchemy.select(CartItemModel)
        .where(CartItemModel.id == cart_item_id)
        .where(CartItemModel.cart_id == cart_id)
    )
    existing_cart_item = result.scalars().first()
    if not existing_cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    for field, value in cart_item.model_dump(exclude_unset=True).items():
        setattr(existing_cart_item, field, value)

    existing_cart_item.cart_id = cart_id

    session.add(existing_cart_item)
    await session.commit()
    await session.refresh(existing_cart_item)
    return existing_cart_item


@router.patch(
    path="/{cart_id}/items/{cart_item_id}",
    response_model=CartItemResponseSchema,
)
async def partial_update_cart_item(cart_id: int, cart_item_id: int, cart_item: CartItemPartialUpdateSchema,
                                   session: SessionDepend):
    result = await session.execute(
        sqlalchemy.select(CartItemModel)
        .where(CartItemModel.id == cart_item_id)
        .where(CartItemModel.cart_id == cart_id)
    )
    existing_cart_item = result.scalars().first()
    if not existing_cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    for field, value in cart_item.model_dump(exclude_unset=True).items():
        setattr(existing_cart_item, field, value)

    session.add(existing_cart_item)

    await session.commit()
    await session.refresh(existing_cart_item)
    return existing_cart_item


@router.delete(
    path="/{cart_id}/items/{cart_item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(auth.access_token_required)],
)
async def delete_cart_item(cart_id: int, cart_item_id: int, session: SessionDepend):
    result = await session.execute(
        sqlalchemy.select(CartItemModel)
        .where(CartItemModel.id == cart_item_id)
        .where(CartItemModel.cart_id == cart_id)
    )
    existing_cart_item = result.scalars().first()
    if not existing_cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    await session.delete(existing_cart_item)
    await session.commit()
    return None