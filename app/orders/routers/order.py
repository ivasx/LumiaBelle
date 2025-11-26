from typing import Annotated, Sequence

import sqlalchemy
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from app.core.settings.db import db
from fastapi import APIRouter
from app.utils import auth
from ..models.order import OrderModel
from ..schemas.order import OrderResponseSchema, OrderCreateSchema, OrderPartialUpdateSchema

SessionDepend = Annotated[AsyncSession, Depends(db.get_session)]

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post(
    path="/",
    response_model=OrderResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_order(order: OrderCreateSchema, session: SessionDepend):
    new_order = OrderModel(
        user_id=order.user_id,
        address_id=order.address_id,
        total_amount=order.total_amount,
        status=order.status,
    )
    session.add(new_order)
    await session.commit()
    await session.refresh(new_order)
    return new_order

@router.get(
    path="/",
    response_model=list[OrderResponseSchema],
)
async def get_orders(session: SessionDepend) -> Sequence[OrderModel]:
    query = sqlalchemy.select(OrderModel)
    result = await session.execute(query)
    orders = result.scalars().all()
    return orders

@router.get(
    path="/{order_id}",
    response_model=OrderResponseSchema,
)
async def get_order(order_id: int, session: SessionDepend):
    result = await session.execute(sqlalchemy.select(OrderModel).where(OrderModel.id == order_id))
    order = result.scalars().first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.put(
    path="/{order_id}",
    response_model=OrderResponseSchema,
)
async def update_order(order_id: int, order: OrderCreateSchema, session: SessionDepend):
    result = await session.execute(sqlalchemy.select(OrderModel).where(OrderModel.id == order_id))
    existing_order = result.scalars().first()
    if not existing_order:
        raise HTTPException(status_code=404, detail="Order not found")
    for field, value in order.model_dump(exclude_unset=True).items():
        setattr(existing_order, field, value)
    session.add(existing_order)

    await session.commit()
    await session.refresh(existing_order)
    return existing_order

@router.patch(
    path="/{order_id}",
    response_model=OrderResponseSchema,
)
async def partial_update_order(order_id: int, order: OrderPartialUpdateSchema, session: SessionDepend):
    result = await session.execute(sqlalchemy.select(OrderModel).where(OrderModel.id == order_id))
    existing_order = result.scalars().first()
    if not existing_order:
        raise HTTPException(status_code=404, detail="Order not found")
    for field, value in order.model_dump(exclude_unset=True).items():
        setattr(existing_order, field, value)
    session.add(existing_order)

    await session.commit()
    await session.refresh(existing_order)
    return existing_order

@router.delete(
    path="/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(auth.access_token_required)],
)
async def delete_order(order_id: int, session: SessionDepend):
    result = await session.execute(sqlalchemy.select(OrderModel).where(OrderModel.id == order_id))
    existing_order = result.scalars().first()
    if not existing_order:
        raise HTTPException(status_code=404, detail="Order not found")
    await session.delete(existing_order)
    await session.commit()
    return None