from typing import Annotated, Sequence

import sqlalchemy
from fastapi import Depends, HTTPException, APIRouter
from app.utils import auth
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from app.core.settings.db import db

from ..models.user import UserModel
from ..schemas.user import UserResponseSchema, UserCreateSchema, UserPartialUpdateSchema
from app.utils.encrypt import hash_password

SessionDepend = Annotated[AsyncSession, Depends(db.get_session)]

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    path="/",
    response_model=UserResponseSchema,
    status_code=status.HTTP_201_CREATED,
    tags=["Users"]
)
async def create_user(user: UserCreateSchema, session: SessionDepend):
    hashed_pass = hash_password(user.password)

    new_user = UserModel(
        email=user.email,
        hashed_password=hashed_pass,
        first_name=user.first_name,
        last_name=user.last_name,
        phone_number=user.phone_number,
        is_active=user.is_active,
    )

    if user.created_at:
        new_user.created_at = user.created_at

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


@router.get(
    path="/",
    response_model=list[UserResponseSchema],
)
async def get_users(session: SessionDepend) -> Sequence[UserModel]:
    query = sqlalchemy.select(UserModel)
    result = await session.execute(query)
    users = result.scalars().all()
    return users


@router.get(
    path="/{user_id}",
    response_model=UserResponseSchema,
)
async def get_user(user_id: int, session: SessionDepend):
    result = await session.execute(sqlalchemy.select(UserModel).where(UserModel.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put(
    path="/{user_id}",
    response_model=UserResponseSchema,
)
async def update_user(user_id: int, user: UserCreateSchema, session: SessionDepend):
    result = await session.execute(sqlalchemy.select(UserModel).where(UserModel.id == user_id))
    existing_user = result.scalars().first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    user_data = user.model_dump(exclude_unset=True)

    if 'password' in user_data:
        raw_password = user_data.pop('password')
        existing_user.hashed_password = hash_password(raw_password)

    for field, value in user_data.items():
        setattr(existing_user, field, value)

    session.add(existing_user)
    await session.commit()
    await session.refresh(existing_user)
    return existing_user


@router.patch(
    path="/{user_id}",
    response_model=UserResponseSchema,
)
async def partial_update_user(user_id: int, user: UserPartialUpdateSchema, session: SessionDepend):
    result = await session.execute(sqlalchemy.select(UserModel).where(UserModel.id == user_id))
    existing_user = result.scalars().first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    user_data = user.model_dump(exclude_unset=True)

    for field, value in user_data.items():
        setattr(existing_user, field, value)

    session.add(existing_user)
    await session.commit()
    await session.refresh(existing_user)
    return existing_user


@router.delete(
    path="/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(auth.access_token_required)],
)
async def delete_user(user_id: int, session: SessionDepend):
    result = await session.execute(sqlalchemy.select(UserModel).where(UserModel.id == user_id))
    existing_user = result.scalars().first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    await session.delete(existing_user)
    await session.commit()
    return None