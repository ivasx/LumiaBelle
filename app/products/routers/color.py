from typing import Annotated, Sequence

import sqlalchemy
from fastapi import Depends, HTTPException, APIRouter
from app.utils import auth
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from app.core.settings.db import db

from ..models.color import ColorModel
from ..schemas.color import ColorResponseSchema, ColorCreateSchema, ColorPartialUpdateSchema

SessionDepend = Annotated[AsyncSession, Depends(db.get_session)]

router = APIRouter(prefix="/colors", tags=["colors"])


@router.post(
    path="/",
    response_model=ColorResponseSchema,
    status_code=status.HTTP_201_CREATED,
    tags=["Color"]
)
async def create_color(color: ColorCreateSchema, session: SessionDepend):
    new_color = ColorModel(
        name=color.name,
        hex_code=color.hex_code,
    )
    session.add(new_color)
    await session.commit()
    await session.refresh(new_color)
    return new_color


@router.get(
    path="/",
    response_model=list[ColorResponseSchema],
)
async def get_colors(session: SessionDepend) -> Sequence[ColorModel]:
    query = sqlalchemy.select(ColorModel)
    result = await session.execute(query)
    colors = result.scalars().all()
    return colors


@router.get(
    path="/{color_id}",
    response_model=ColorResponseSchema,
)
async def get_color(color_id: int, session: SessionDepend):
    result = await session.execute(sqlalchemy.select(ColorModel).where(ColorModel.id == color_id))
    color = result.scalars().first()
    if not color:
        raise HTTPException(status_code=404, detail="Color not found")
    return color


@router.put(
    path="/{color_id}",
    response_model=ColorResponseSchema,
)
async def update_color(color_id: int, color: ColorCreateSchema, session: SessionDepend):
    result = await session.execute(sqlalchemy.select(ColorModel).where(ColorModel.id == color_id))
    existing_color = result.scalars().first()
    if not existing_color:
        raise HTTPException(status_code=404, detail="Color not found")
    for field, value in color.model_dump(exclude_unset=True).items():
        setattr(existing_color, field, value)
    session.add(existing_color)

    await session.commit()
    await session.refresh(existing_color)
    return existing_color


@router.patch(
    path="/{color_id}",
    response_model=ColorResponseSchema,
)
async def partial_update_color(color_id: int, color: ColorPartialUpdateSchema, session: SessionDepend):
    result = await session.execute(sqlalchemy.select(ColorModel).where(ColorModel.id == color_id))
    existing_color = result.scalars().first()
    if not existing_color:
        raise HTTPException(status_code=404, detail="Color not found")
    for field, value in color.model_dump(exclude_unset=True).items():
        setattr(existing_color, field, value)
    session.add(existing_color)

    await session.commit()
    await session.refresh(existing_color)
    return existing_color


@router.delete(
    path="/{color_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(auth.access_token_required)],
)
async def delete_color(color_id: int, session: SessionDepend):
    result = await session.execute(sqlalchemy.select(ColorModel).where(ColorModel.id == color_id))
    existing_color = result.scalars().first()
    if not existing_color:
        raise HTTPException(status_code=404, detail="Color not found")
    await session.delete(existing_color)
    await session.commit()
    return None
