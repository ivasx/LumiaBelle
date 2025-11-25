from typing import Annotated, Sequence

import sqlalchemy
from fastapi import Depends, HTTPException, APIRouter
from app.utils import auth
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from app.core.settings.db import db

from ..models.cart import CartModel
from ..schemas.cart import CartResponseSchema, CartCreateSchema, CartPartialUpdateSchema

SessionDepend = Annotated[AsyncSession, Depends(db.get_session)]

router = APIRouter(prefix="/carts", tags=["carts"])


@router.post(
    path="/",
    response_model=CartResponseSchema,
    status_code=status.HTTP_201_CREATED,
    tags=["Cart"]
)
async def create_cart(cart: CartCreateSchema, session: SessionDepend):
    new_cart = CartModel(
        user_id=cart.user_id,
    )
    session.add(new_cart)
    await session.commit()
    await session.refresh(new_cart)
    return new_cart


@router.get(
    path="/",
    response_model=list[CartResponseSchema],
)
async def get_carts(session: SessionDepend) -> Sequence[CartModel]:
    query = sqlalchemy.select(CartModel)
    result = await session.execute(query)
    carts = result.scalars().all()
    return carts


@router.get(
    path="/{cart_id}",
    response_model=CartResponseSchema,
)
async def get_cart(cart_id: int, session: SessionDepend):
    result = await session.execute(sqlalchemy.select(CartModel).where(CartModel.id == cart_id))
    cart = result.scalars().first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart


@router.put(
    path="/{cart_id}",
    response_model=CartResponseSchema,
)
async def update_cart(cart_id: int, cart: CartCreateSchema, session: SessionDepend):
    result = await session.execute(sqlalchemy.select(CartModel).where(CartModel.id == cart_id))
    existing_cart = result.scalars().first()
    if not existing_cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    for field, value in cart.model_dump(exclude_unset=True).items():
        setattr(existing_cart, field, value)
    session.add(existing_cart)

    await session.commit()
    await session.refresh(existing_cart)
    return existing_cart


@router.patch(
    path="/{cart_id}",
    response_model=CartResponseSchema,
)
async def partial_update_cart(cart_id: int, cart: CartPartialUpdateSchema, session: SessionDepend):
    result = await session.execute(sqlalchemy.select(CartModel).where(CartModel.id == cart_id))
    existing_cart = result.scalars().first()
    if not existing_cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    for field, value in cart.model_dump(exclude_unset=True).items():
        setattr(existing_cart, field, value)
    session.add(existing_cart)

    await session.commit()
    await session.refresh(existing_cart)
    return existing_cart


@router.delete(
    path="/{cart_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(auth.access_token_required)],
)
async def delete_cart(cart_id: int, session: SessionDepend):
    result = await session.execute(sqlalchemy.select(CartModel).where(CartModel.id == cart_id))
    existing_cart = result.scalars().first()
    if not existing_cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    await session.delete(existing_cart)
    await session.commit()
    return None
