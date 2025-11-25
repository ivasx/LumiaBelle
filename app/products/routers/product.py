from typing import Annotated, Sequence

import sqlalchemy
from fastapi import Depends, HTTPException, APIRouter
from app.utils import auth
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from app.core.settings.db import db

from ..models.product import ProductModel
from ..schemas.product import ProductResponseSchema, ProductCreateSchema, ProductPartialUpdateSchema

SessionDepend = Annotated[AsyncSession, Depends(db.get_session)]

router = APIRouter(prefix="/products", tags=["products"])


@router.post(
    path="/",
    response_model=ProductResponseSchema,
    status_code=status.HTTP_201_CREATED,
    tags=["Product"]
)
async def create_product(product: ProductCreateSchema, session: SessionDepend):
    new_product = ProductModel(
        title=product.title,
        description=product.description,
        price=product.price,
        category_id=product.category_id,
    )
    session.add(new_product)
    try:
        await session.commit()
        await session.refresh(new_product)
    except sqlalchemy.exc.IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=400, detail="Invalid category_id or database constraint violated.")

    return new_product


@router.get(
    path="/",
    response_model=list[ProductResponseSchema],
)
async def get_products(session: SessionDepend) -> Sequence[ProductModel]:
    query = sqlalchemy.select(ProductModel)
    result = await session.execute(query)
    products = result.scalars().all()
    return products


@router.get(
    path="/{product_id}",
    response_model=ProductResponseSchema,
)
async def get_product(product_id: int, session: SessionDepend):
    result = await session.execute(sqlalchemy.select(ProductModel).where(ProductModel.id == product_id))
    product = result.scalars().first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put(
    path="/{product_id}",
    response_model=ProductResponseSchema,
)
async def update_product(product_id: int, product: ProductCreateSchema, session: SessionDepend):
    result = await session.execute(sqlalchemy.select(ProductModel).where(ProductModel.id == product_id))
    existing_product = result.scalars().first()
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")
    for field, value in product.model_dump(exclude_unset=True).items():
        setattr(existing_product, field, value)

    try:
        session.add(existing_product)
        await session.commit()
        await session.refresh(existing_product)
    except sqlalchemy.exc.IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=400, detail="Update failed due to database constraints.")

    return existing_product


@router.patch(
    path="/{product_id}",
    response_model=ProductResponseSchema,
)
async def partial_update_product(product_id: int, product: ProductPartialUpdateSchema, session: SessionDepend):
    result = await session.execute(sqlalchemy.select(ProductModel).where(ProductModel.id == product_id))
    existing_product = result.scalars().first()
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")
    for field, value in product.model_dump(exclude_unset=True).items():
        setattr(existing_product, field, value)

    try:
        session.add(existing_product)
        await session.commit()
        await session.refresh(existing_product)
    except sqlalchemy.exc.IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=400, detail="Update failed due to database constraints.")

    return existing_product


@router.delete(
    path="/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(auth.access_token_required)],
)
async def delete_product(product_id: int, session: SessionDepend):
    result = await session.execute(sqlalchemy.select(ProductModel).where(ProductModel.id == product_id))
    existing_product = result.scalars().first()
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")
    await session.delete(existing_product)
    await session.commit()
    return None