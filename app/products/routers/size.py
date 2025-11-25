from typing import Annotated, Sequence

import sqlalchemy
from fastapi import Depends, HTTPException, APIRouter
from app.utils import auth
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from app.core.settings.db import db

from ..models.size import SizeModel
from ..schemas.size import SizeResponseSchema, SizeCreateSchema, SizePartialUpdateSchema

SessionDepend = Annotated[AsyncSession, Depends(db.get_session)]

router = APIRouter(prefix="/sizes", tags=["sizes"])

@router.post(
    path="/",
    response_model=SizeResponseSchema,
    status_code=status.HTTP_201_CREATED,
    tags=["Size"]
)
async def create_size(size: SizeCreateSchema, session: SessionDepend):
    new_size = SizeModel(
        label=size.label,
    )
    session.add(new_size)
    await session.commit()
    await session.refresh(new_size)
    return new_size

@router.get(
    path="/",
    response_model=list[SizeResponseSchema],
)
async def get_sizes(session: SessionDepend) -> Sequence[SizeModel]:
    query = sqlalchemy.select(SizeModel)
    result = await session.execute(query)
    sizes = result.scalars().all()
    return sizes

@router.get(
    path="/{size_id}",
    response_model=SizeResponseSchema,
)
async def get_size(size_id: int, session: SessionDepend):
    result = await session.execute(sqlalchemy.select(SizeModel).where(SizeModel.id == size_id))
    size = result.scalars().first()
    if not size:
        raise HTTPException(status_code=404, detail="Size not found")
    return size

@router.put(
    path="/{size_id}",
    response_model=SizeResponseSchema,
)
async def update_size(size_id: int, size: SizeCreateSchema, session: SessionDepend):
    result = await session.execute(sqlalchemy.select(SizeModel).where(SizeModel.id == size_id))
    existing_size = result.scalars().first()
    if not existing_size:
        raise HTTPException(status_code=404, detail="Size not found")
    for field, value in size.model_dump(exclude_unset=True).items():
        setattr(existing_size, field, value)
    session.add(existing_size)

    await session.commit()
    await session.refresh(existing_size)
    return existing_size

@router.patch(
    path="/{size_id}",
    response_model=SizeResponseSchema,
)
async def partial_update_size(size_id: int, size: SizePartialUpdateSchema, session: SessionDepend):
    result = await session.execute(sqlalchemy.select(SizeModel).where(SizeModel.id == size_id))
    existing_size = result.scalars().first()
    if not existing_size:
        raise HTTPException(status_code=404, detail="Size not found")
    for field, value in size.model_dump(exclude_unset=True).items():
        setattr(existing_size, field, value)
    session.add(existing_size)

    await session.commit()
    await session.refresh(existing_size)
    return existing_size

@router.delete(
    path="/{size_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(auth.access_token_required)],
)
async def delete_size(size_id: int, session: SessionDepend):
    result = await session.execute(sqlalchemy.select(SizeModel).where(SizeModel.id == size_id))
    existing_size = result.scalars().first()
    if not existing_size:
        raise HTTPException(status_code=404, detail="Size not found")
    await session.delete(existing_size)
    await session.commit()
    return None