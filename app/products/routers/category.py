from typing import Annotated, Sequence

import sqlalchemy
from fastapi import Depends, HTTPException, APIRouter
from app.utils import auth
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from app.core.settings.db import db

from ..models.category import CategoryModel
from ..schemas.category import CategoryResponseSchema, CategoryCreateSchema, CategoryPartialUpdateSchema

SessionDepend = Annotated[AsyncSession, Depends(db.get_session)]

router = APIRouter(prefix="/categories", tags=["categories"])

@router.post(
    path="/",
    response_model=CategoryResponseSchema,
    status_code=status.HTTP_201_CREATED,

)
async def create_category(category: CategoryCreateSchema, session: SessionDepend):
    new_category = CategoryModel(
        name=category.name,
    )
    session.add(new_category)
    await session.commit()
    await session.refresh(new_category)
    return new_category

@router.get(
    path="/",
    response_model=list[CategoryResponseSchema],
)
async def get_categories(session: SessionDepend) -> Sequence[CategoryModel]:
    query = sqlalchemy.select(CategoryModel)
    result = await session.execute(query)
    categories = result.scalars().all()
    return categories

@router.get(
    path="/{category_id}",
    response_model=CategoryResponseSchema,
)
async def get_category(category_id: int, session: SessionDepend):
    result = await session.execute(sqlalchemy.select(CategoryModel).where(CategoryModel.id == category_id))
    category = result.scalars().first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.put(
    path="/{category_id}",
    response_model=CategoryResponseSchema,
)
async def update_category(category_id: int, category: CategoryCreateSchema, session: SessionDepend):
    result = await session.execute(sqlalchemy.select(CategoryModel).where(CategoryModel.id == category_id))
    existing_category = result.scalars().first()
    if not existing_category:
        raise HTTPException(status_code=404, detail="Category not found")
    for field, value in category.model_dump(exclude_unset=True).items():
        setattr(existing_category, field, value)
    session.add(existing_category)

    await session.commit()
    await session.refresh(existing_category)
    return existing_category

@router.patch(
    path="/{category_id}",
    response_model=CategoryResponseSchema,
)
async def partial_update_category(category_id: int, category: CategoryPartialUpdateSchema, session: SessionDepend):
    result = await session.execute(sqlalchemy.select(CategoryModel).where(CategoryModel.id == category_id))
    existing_category = result.scalars().first()
    if not existing_category:
        raise HTTPException(status_code=404, detail="Category not found")
    for field, value in category.model_dump(exclude_unset=True).items():
        setattr(existing_category, field, value)
    session.add(existing_category)

    await session.commit()
    await session.refresh(existing_category)
    return existing_category

@router.delete(
    path="/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(auth.access_token_required)],
)
async def delete_category(category_id: int, session: SessionDepend):
    result = await session.execute(sqlalchemy.select(CategoryModel).where(CategoryModel.id == category_id))
    existing_category = result.scalars().first()
    if not existing_category:
        raise HTTPException(status_code=404, detail="Category not found")
    await session.delete(existing_category)
    await session.commit()
    return None