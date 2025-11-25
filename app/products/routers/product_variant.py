from typing import Annotated, Sequence

import sqlalchemy
from fastapi import Depends, HTTPException, APIRouter
from app.utils import auth
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from app.core.settings.db import db

from ..models.product_variant import ProductVariantModel
from ..schemas.product_variant import ProductVariantResponseSchema, ProductVariantCreateSchema, \
    ProductVariantPartialUpdateSchema

SessionDepend = Annotated[AsyncSession, Depends(db.get_session)]

router = APIRouter(prefix="/product_variants", tags=["product_variants"])


@router.post(
    path="/",
    response_model=ProductVariantResponseSchema,
    status_code=status.HTTP_201_CREATED,
    tags=["Product Variant"]
)
async def create_product_variant(variant: ProductVariantCreateSchema, session: SessionDepend):
    new_variant = ProductVariantModel(
        product_id=variant.product_id,
        size_id=variant.size_id,
        color_id=variant.color_id,
        stock_quantity=variant.stock_quantity,
    )
    session.add(new_variant)
    await session.commit()
    await session.refresh(new_variant)
    return new_variant


@router.get(
    path="/",
    response_model=list[ProductVariantResponseSchema],
)
async def get_product_variants(session: SessionDepend) -> Sequence[ProductVariantModel]:
    query = sqlalchemy.select(ProductVariantModel)
    result = await session.execute(query)
    variants = result.scalars().all()
    return variants


@router.get(
    path="/{variant_id}",
    response_model=ProductVariantResponseSchema,
)
async def get_product_variant(variant_id: int, session: SessionDepend):
    result = await session.execute(sqlalchemy.select(ProductVariantModel).where(ProductVariantModel.id == variant_id))
    variant = result.scalars().first()
    if not variant:
        raise HTTPException(status_code=404, detail="Product variant not found")
    return variant


@router.put(
    path="/{variant_id}",
    response_model=ProductVariantResponseSchema,
)
async def update_product_variant(variant_id: int, variant: ProductVariantCreateSchema, session: SessionDepend):
    result = await session.execute(sqlalchemy.select(ProductVariantModel).where(ProductVariantModel.id == variant_id))
    existing_variant = result.scalars().first()
    if not existing_variant:
        raise HTTPException(status_code=404, detail="Product variant not found")
    for field, value in variant.model_dump(exclude_unset=True).items():
        setattr(existing_variant, field, value)
    session.add(existing_variant)

    await session.commit()
    await session.refresh(existing_variant)
    return existing_variant


@router.patch(
    path="/{variant_id}",
    response_model=ProductVariantResponseSchema,
)
async def partial_update_product_variant(variant_id: int, variant: ProductVariantPartialUpdateSchema,
                                         session: SessionDepend):
    result = await session.execute(sqlalchemy.select(ProductVariantModel).where(ProductVariantModel.id == variant_id))
    existing_variant = result.scalars().first()
    if not existing_variant:
        raise HTTPException(status_code=404, detail="Product variant not found")
    for field, value in variant.model_dump(exclude_unset=True).items():
        setattr(existing_variant, field, value)
    session.add(existing_variant)

    await session.commit()
    await session.refresh(existing_variant)
    return existing_variant


@router.delete(
    path="/{variant_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(auth.access_token_required)],
)
async def delete_product_variant(variant_id: int, session: SessionDepend):
    result = await session.execute(sqlalchemy.select(ProductVariantModel).where(ProductVariantModel.id == variant_id))
    existing_variant = result.scalars().first()
    if not existing_variant:
        raise HTTPException(status_code=404, detail="Product variant not found")
    await session.delete(existing_variant)
    await session.commit()
    return None
