from typing import Annotated, Sequence

import sqlalchemy
from fastapi import Depends, HTTPException, APIRouter
from app.utils import auth
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from app.core.settings.db import db

from ..models.order_item import OrderItemModel
from ..schemas.order_item import OrderItemResponseSchema, OrderItemCreateSchema, OrderItemPartialUpdateSchema

SessionDepend = Annotated[AsyncSession, Depends(db.get_session)]

router = APIRouter(prefix="/order_items", tags=["order_items"])


@router.post(
    path="/",
    response_model=OrderItemResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_order_item(order_item: OrderItemCreateSchema, session: SessionDepend):
    new_order_item = OrderItemModel(
        order_id=order_item.order_id,
        product_variant_id=order_item.product_variant_id,
        quantity=order_item.quantity,
        price_at_order=order_item.price_at_order,
    )
    session.add(new_order_item)
    await session.commit()
    await session.refresh(new_order_item)
    return new_order_item


@router.get(
    path="/",
    response_model=list[OrderItemResponseSchema],
)
async def get_order_items(session: SessionDepend) -> Sequence[OrderItemModel]:
    query = sqlalchemy.select(OrderItemModel)
    result = await session.execute(query)
    order_items = result.scalars().all()
    return order_items


@router.get(
    path="/{order_item_id}",
    response_model=OrderItemResponseSchema,
)
async def get_order_item(order_item_id: int, session: SessionDepend):
    result = await session.execute(sqlalchemy.select(OrderItemModel).where(OrderItemModel.id == order_item_id))
    order_item = result.scalars().first()
    if not order_item:
        raise HTTPException(status_code=404, detail="Order item not found")
    return order_item


@router.put(
    path="/{order_item_id}",
    response_model=OrderItemResponseSchema,
)
async def update_order_item(order_item_id: int, order_item: OrderItemCreateSchema, session: SessionDepend):
    result = await session.execute(sqlalchemy.select(OrderItemModel).where(OrderItemModel.id == order_item_id))
    existing_order_item = result.scalars().first()
    if not existing_order_item:
        raise HTTPException(status_code=404, detail="Order item not found")
    for field, value in order_item.model_dump(exclude_unset=True).items():
        setattr(existing_order_item, field, value)
    session.add(existing_order_item)

    await session.commit()
    await session.refresh(existing_order_item)
    return existing_order_item


@router.patch(
    path="/{order_item_id}",
    response_model=OrderItemResponseSchema,
)
async def partial_update_order_item(order_item_id: int, order_item: OrderItemPartialUpdateSchema,
                                    session: SessionDepend):
    result = await session.execute(sqlalchemy.select(OrderItemModel).where(OrderItemModel.id == order_item_id))
    existing_order_item = result.scalars().first()
    if not existing_order_item:
        raise HTTPException(status_code=404, detail="Order item not found")
    for field, value in order_item.model_dump(exclude_unset=True).items():
        setattr(existing_order_item, field, value)
    session.add(existing_order_item)

    await session.commit()
    await session.refresh(existing_order_item)
    return existing_order_item


@router.delete(
    path="/{order_item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(auth.access_token_required)],
)
async def delete_order_item(order_item_id: int, session: SessionDepend):
    result = await session.execute(sqlalchemy.select(OrderItemModel).where(OrderItemModel.id == order_item_id))
    existing_order_item = result.scalars().first()
    if not existing_order_item:
        raise HTTPException(status_code=404, detail="Order item not found")
    await session.delete(existing_order_item)
    await session.commit()
    return None
