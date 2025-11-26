from typing import Annotated, Sequence

import sqlalchemy
from fastapi import Depends, HTTPException, APIRouter
from app.utils import auth
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from app.core.settings.db import db

from ..models.user_address import UserAddressModel
from ..schemas.user_address import UserAddressResponseSchema, UserAddressCreateSchema, UserAddressPartialUpdateSchema

SessionDepend = Annotated[AsyncSession, Depends(db.get_session)]

router = APIRouter(prefix="/user_addresses", tags=["user_addresses"])

@router.post(
    path="/",
    response_model=UserAddressResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_user_address(address: UserAddressCreateSchema, session: SessionDepend):
    new_address = UserAddressModel(
        user_id=address.user_id,
        address_line1=address.address_line1,
        city=address.city,
        zip_code=address.zip_code,
        is_default=address.is_default,
    )
    session.add(new_address)
    await session.commit()
    await session.refresh(new_address)
    return new_address

@router.get(
    path="/",
    response_model=list[UserAddressResponseSchema],
)
async def get_user_addresses(session: SessionDepend) -> Sequence[UserAddressModel]:
    query = sqlalchemy.select(UserAddressModel)
    result = await session.execute(query)
    addresses = result.scalars().all()
    return addresses

@router.get(
    path="/{address_id}",
    response_model=UserAddressResponseSchema,
)
async def get_user_address(address_id: int, session: SessionDepend):
    result = await session.execute(sqlalchemy.select(UserAddressModel).where(UserAddressModel.id == address_id))
    address = result.scalars().first()
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    return address

@router.put(
    path="/{address_id}",
    response_model=UserAddressResponseSchema,
)
async def update_user_address(address_id: int, address: UserAddressCreateSchema, session: SessionDepend):
    result = await session.execute(sqlalchemy.select(UserAddressModel).where(UserAddressModel.id == address_id))
    existing_address = result.scalars().first()
    if not existing_address:
        raise HTTPException(status_code=404, detail="Address not found")
    for field, value in address.model_dump(exclude_unset=True).items():
        setattr(existing_address, field, value)
    session.add(existing_address)

    await session.commit()
    await session.refresh(existing_address)
    return existing_address

@router.patch(
    path="/{address_id}",
    response_model=UserAddressResponseSchema,
)
async def partial_update_user_address(address_id: int, address: UserAddressPartialUpdateSchema, session: SessionDepend):
    result = await session.execute(sqlalchemy.select(UserAddressModel).where(UserAddressModel.id == address_id))
    existing_address = result.scalars().first()
    if not existing_address:
        raise HTTPException(status_code=404, detail="Address not found")
    for field, value in address.model_dump(exclude_unset=True).items():
        setattr(existing_address, field, value)
    session.add(existing_address)

    await session.commit()
    await session.refresh(existing_address)
    return existing_address

@router.delete(
    path="/{address_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(auth.access_token_required)],
)
async def delete_user_address(address_id: int, session: SessionDepend):
    result = await session.execute(sqlalchemy.select(UserAddressModel).where(UserAddressModel.id == address_id))
    existing_address = result.scalars().first()
    if not existing_address:
        raise HTTPException(status_code=404, detail="Address not found")
    await session.delete(existing_address)
    await session.commit()
    return None